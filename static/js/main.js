// NEW: Diagnosis panel variables (moved to global scope)
let diagnosisPanelVisible = false;
let currentPatientDiagnosis = null;
let diagnosisAttemptCount = 0;
const maxDiagnosisAttempts = 3;

// Move currentConversationId to global scope for diagnosis functions
let currentConversationId = null;

document.addEventListener('DOMContentLoaded', async () => {
    // Single declaration of shared variables
    let stopVAD = null;        // will hold the cleanup fn
    
    // Audio context for playback - moved up to fix TDZ issue
    let audioContext;
    
    // Audio recording variables - moved up near other declarations
    let mediaRecorder = null;
    let audioChunks = [];
    let isRecording = false;
    let currentSimulation = null;
    let currentVoiceId = 'Fritz-PlayAI'; // Default voice
    // currentConversationId moved to global scope
    let recordedMimeType = '';
    let currentAudioSource = null; // Track current audio source for interruption
    let microphoneSetup = false;

    // NEW: Multi-agent conversation state
    let multiAgentMode = false;
    let activeAgents = [];
    let currentMultiAgentConversationId = null;

    // Form state management for AI case generation
    let formState = {
        selectedSpecialty: null,
        selectedSymptoms: [],
        isLoading: false,
        realTimeValidation: true
    };

    // Wizard state management
    let wizardState = {
        currentStep: 1,
        totalSteps: 4,
        formData: {},
        selectedSpecialty: null,
        selectedSymptoms: []
    };

    // Medical knowledge data - will be populated from backend
    let medicalKnowledge = {
        specialties: {},
        all_symptoms: {}
    };

    // Manual recording variables
    let recordedChunks = [];
    let isManualRecording = false;

    async function initAutoVAD() {
        console.log('initAutoVAD: Starting VAD initialization...');
        
        try {
            // Configure ONNX runtime to avoid threading issues
            if (typeof ort !== 'undefined') {
                ort.env.wasm.wasmPaths = '/static/vad-model/';
                ort.env.wasm.numThreads = 1; // Disable threading to avoid .mjs issues
                ort.env.wasm.simd = true;
                console.log('ONNX Runtime configured with local paths');
            }
            
            console.log('initAutoVAD: Creating MicVAD instance with config:', {
                positiveSpeechThreshold: 0.8,
                negativeSpeechThreshold: 0.5,
                preSpeechPadFrames: 8,
                minSpeechFrames: 3,
                redemptionFrames: 10
            });

            const myvad = await vad.MicVAD.new({
                modelPath: '/static/vad-model/silero_vad_legacy.onnx',
                workletPath: '/static/vad-model/vad.worklet.bundle.min.js', // Fixed path
                positiveSpeechThreshold: 0.8,
                negativeSpeechThreshold: 0.5,
                preSpeechPadFrames: 8,
                minSpeechFrames: 3,
                redemptionFrames: 10,
                // Add ONNX runtime configuration
                ortConfig: (ort) => {
                    ort.env.wasm.wasmPaths = '/static/vad-model/';
                    ort.env.wasm.numThreads = 1; // Disable threading
                    ort.env.wasm.simd = true;
                },

                onSpeechStart: () => {
                    console.log('initAutoVAD: Speech detected, starting recording...');
                    
                    if (currentAudioSource) {
                        console.log('VAD onSpeechStart: Interrupting TTS playback');
                        currentAudioSource.stop();
                        currentAudioSource.onended = null;
                        currentAudioSource = null;
                    }
                    
                    updateStatus("Listening...");
                },

                onSpeechEnd: async (float32Audio) => {
                    console.log(`initAutoVAD: Speech ended, processing audio (${float32Audio.length} samples)`);
                    updateStatus("Processing…");
                    try {
                        const wavBlob = float32ToWav(float32Audio);
                        console.log(`initAutoVAD: Created WAV blob of size ${wavBlob.size} bytes`);
                        await processAudio(wavBlob);
                        updateStatus("Ready");
                    } catch (error) {
                        console.error('initAutoVAD: Error processing audio:', error);
                        updateStatus("Error processing audio");
                    }
                },

                onVADMisfire: () => {
                    console.log('initAutoVAD: VAD misfire detected (false positive)');
                }
            });

            console.log('initAutoVAD: MicVAD instance created successfully');
            console.log('initAutoVAD: Starting VAD...');
            await myvad.start();
            console.log('initAutoVAD: VAD started successfully');
            
            return () => {
                console.log('initAutoVAD: Cleanup function called, destroying VAD');
                myvad.destroy();
            };

        } catch (error) {
            console.error('initAutoVAD: Error during VAD initialization:', error);
            updateStatus("Error initializing voice detection");
            
            // Fallback: show manual recording button
            console.log('Falling back to manual recording mode');
            updateStatus("Voice detection failed - please use manual mode");
            
            // Show manual recording button
            if (manualRecordBtn) {
                manualRecordBtn.style.display = 'inline-block';
                updateStatus("Voice detection failed - use Manual Record button");
            }
            
            throw error;
        }
    }

    // DOM elements
    const autoListenBtn = document.getElementById('autoListenBtn');
    const manualRecordBtn = document.getElementById('manualRecordBtn');
    const statusElement = document.getElementById('status');
    const conversationElement = document.getElementById('conversation');
    const simulationSelect = document.getElementById('simulationSelect');
    const voiceSelect = document.getElementById('voiceSelect');
    const conversationListElement = document.getElementById('conversationList');
    const refreshConversationsBtn = document.getElementById('refreshConversationsBtn');
    const newConversationBtn = document.getElementById('newConversationBtn');
    
    // Custom Patient Form DOM elements
    const customPatientForm = document.getElementById('customPatientForm');
    const customPatientFormFields = document.getElementById('customPatientFormFields');
    const cancelCustomPatientBtn = document.getElementById('cancelCustomPatient');
    const createCustomPatientBtn = document.getElementById('createCustomPatient');
    
    // Additional DOM elements for AI case generation
    const medicalSpecialtySelect = document.getElementById('medicalSpecialty');
    const symptomsContainer = document.getElementById('symptomsContainer');
    const specialtyDescription = document.getElementById('specialtyDescription');
    const symptomsInstructions = document.getElementById('symptomsInstructions');
    const aiGenerationLoading = document.getElementById('aiGenerationLoading');
    const formValidationSummary = document.getElementById('formValidationSummary');
    const validationErrorsList = document.getElementById('validationErrorsList');
    
    if (autoListenBtn) {
        autoListenBtn.addEventListener('click', async (event) => {
            event.preventDefault();
            event.stopPropagation();
            
            console.log('Button clicked, current stopVAD state:', !!stopVAD);
            
            try {
                if (!stopVAD) {
                    if (!audioContext) {
                        audioContext = new (window.AudioContext || window.webkitAudioContext)();
                        console.log('AudioContext initialized, running system diagnostic...');
                        testAudioSystemAsync();
                    }
                    
                    try {
                        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                        stream.getTracks().forEach(t => t.stop());
                    } catch (err) {
                        console.error('Microphone permission error:', err);
                        updateStatus('Microphone access required');
                        return;
                    }
                    
                    updateStatus('Initializing voice detection...');
                    autoListenBtn.classList.add('recording');
                    stopVAD = await initAutoVAD();
                    updateStatus('Listening…');
                } else {
                    stopVAD();
                    stopVAD = null;
                    updateStatus('Paused');
                    autoListenBtn.classList.remove('recording');
                }
            } catch (error) {
                console.error('Error in click handler:', error);
                updateStatus('Error initializing voice detection');
                autoListenBtn.classList.remove('recording');
                stopVAD = null;
            }
        });
        console.log('Click listener attached');
    } else {
        console.error('Auto listen button not found');
    }

    // Manual recording button event listener
    if (manualRecordBtn) {
        manualRecordBtn.addEventListener('click', async (event) => {
            event.preventDefault();
            event.stopPropagation();
            
            if (!isManualRecording) {
                await startManualRecording();
            } else {
                stopManualRecording();
            }
        });
        console.log('Manual record button listener attached');
    }

    // MULTI-AGENT FUNCTIONS
    function createMultiAgentSetupUI() {
        const setupHTML = `
            <div class="multi-agent-setup" id="multiAgentSetup" style="display: none;">
                <div>
                    <div class="multi-agent-header">
                        <h3>🎯 Start Conference Call</h3>
                        <button class="close-btn" onclick="hideMultiAgentSetup()">&times;</button>
                    </div>
                    <div class="multi-agent-content">
                        <p>Select 2 or more personas to participate in a group conversation:</p>
                        <div class="agent-selection-list" id="agentSelectionList">
                            <!-- Agents will be populated here -->
                        </div>
                        <div class="multi-agent-actions">
                            <button class="btn btn-secondary" onclick="hideMultiAgentSetup()">Cancel</button>
                            <button class="btn btn-primary" id="startMultiAgentBtn" onclick="startMultiAgentConversation()" disabled>
                                Start Conference Call
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', setupHTML);
    }

    async function showMultiAgentSetup() {
        if (!document.getElementById('multiAgentSetup')) {
            createMultiAgentSetupUI();
        }
        await populateAgentSelection();
        document.getElementById('multiAgentSetup').style.display = 'flex';
    }

    function hideMultiAgentSetup() {
        const setup = document.getElementById('multiAgentSetup');
        if (setup) {
            setup.remove();
        }
    }

    async function populateAgentSelection() {
        try {
            const response = await fetch('/api/personas');
            const data = await response.json();
            
            if (data.status === 'success') {
                const agentsList = document.getElementById('agentSelectionList');
                agentsList.innerHTML = '';
                
                for (const [personaId, persona] of Object.entries(data.personas)) {
                    const agentItem = document.createElement('div');
                    agentItem.className = 'agent-selection-item';
                    agentItem.innerHTML = `
                        <label class="agent-checkbox-label">
                            <input type="checkbox" value="${personaId}" onchange="updateStartButtonState()">
                            <div class="agent-info">
                                <strong>${persona.name}</strong>
                                <p>${persona.description}</p>
                                <small>Voice: ${persona.voice_id}</small>
                            </div>
                        </label>
                    `;
                    agentsList.appendChild(agentItem);
                }
            }
        } catch (error) {
            console.error('Error loading agents:', error);
        }
    }

    window.updateStartButtonState = function() {
        const checkboxes = document.querySelectorAll('#agentSelectionList input[type="checkbox"]:checked');
        const startBtn = document.getElementById('startMultiAgentBtn');
        if (startBtn) {
            startBtn.disabled = checkboxes.length < 2;
        }
    }

    window.startMultiAgentConversation = async function() {
        try {
            const checkboxes = document.querySelectorAll('#agentSelectionList input[type="checkbox"]:checked');
            const selectedAgents = Array.from(checkboxes).map(cb => cb.value);
            
            const response = await fetch('/api/multi-agent/create', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    agent_ids: selectedAgents
                })
            });
            
            const data = await response.json();
            
            if (data.status === 'success') {
                multiAgentMode = true;
                activeAgents = data.active_agents;
                currentMultiAgentConversationId = data.conversation_id;
                currentConversationId = data.conversation_id;
                
                // Clear conversation history and update UI
                conversationElement.innerHTML = '';
                
                updateUIForMultiAgent();
                hideMultiAgentSetup();
                
                console.log('Multi-agent conversation started with agents:', activeAgents.map(a => a.name));
            } else {
                alert('Error starting multi-agent conversation: ' + data.message);
            }
        } catch (error) {
            console.error('Error starting multi-agent conversation:', error);
            alert('Error starting multi-agent conversation');
        }
    }

    function updateUIForMultiAgent() {
        // Add multi-agent indicator
        const indicator = document.createElement('div');
        indicator.className = 'multi-agent-indicator';
        indicator.id = 'multiAgentIndicator';
        indicator.innerHTML = `
            <div>
                <strong>🎯 Conference Call Active</strong>
                <div class="active-agents">
                    ${activeAgents.map(agent => `<span class="agent-badge">${agent.name}</span>`).join('')}
                </div>
            </div>
            <button class="btn btn-secondary" onclick="exitMultiAgent()">Exit Conference</button>
        `;
        
        // Insert after header
        const header = document.querySelector('header');
        header.insertAdjacentElement('afterend', indicator);
    }

    window.exitMultiAgent = function() {
        multiAgentMode = false;
        activeAgents = [];
        currentMultiAgentConversationId = null;
        
        // Remove multi-agent indicator
        const indicator = document.getElementById('multiAgentIndicator');
        if (indicator) {
            indicator.remove();
        }
        
        // Refresh conversation list
        loadConversationHistory();
        
        console.log('Exited multi-agent mode');
    }

    window.hideMultiAgentSetup = hideMultiAgentSetup;

    async function processMultiAgentAudio(audioBlob) {
        try {
            updateStatus('Processing with multiple agents...');
            
            const formData = new FormData();
            formData.append('audio', audioBlob);
            
            if (currentVoiceId) {
                formData.append('voice_id', currentVoiceId);
            }
            
            const response = await fetch('/process_audio_multi_agent', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (data.status === 'success') {
                // Add user message
                addMessage('user', data.user_transcription);
                
                // Add each agent response with speaker labels
                for (const response of data.responses) {
                    addMultiAgentMessage(response);
                    
                    // Play audio response
                    if (response.audio) {
                        await playAudioResponse(response.audio);
                        // Small delay between agent speeches
                        await new Promise(resolve => setTimeout(resolve, 500));
                    }
                }
                
                updateStatus('Ready');
            } else {
                throw new Error(data.message || 'Failed to process audio');
            }
        } catch (error) {
            console.error('Error processing multi-agent audio:', error);
            updateStatus('Error processing audio');
        }
    }

    function addMultiAgentMessage(response) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message assistant multi-agent';
        messageDiv.innerHTML = `
            <div class="speaker-label">${response.speaker}</div>
            <div class="message-content">
                <p>${response.content}</p>
            </div>
        `;
        conversationElement.appendChild(messageDiv);
        conversationElement.scrollTop = conversationElement.scrollHeight;
    }

    function addMultiAgentButton() {
        // Add the multi-agent button to the controls
        const controls = document.querySelector('.controls');
        if (controls && !document.getElementById('multiAgentModeBtn')) {
            const multiAgentBtn = document.createElement('button');
            multiAgentBtn.id = 'multiAgentModeBtn';
            multiAgentBtn.className = 'btn btn-primary';
            multiAgentBtn.innerHTML = '🎯 Start Conference Call';
            multiAgentBtn.onclick = showMultiAgentSetup;
            
            // Insert before the auto listen button
            const autoButton = document.getElementById('autoListenBtn');
            if (autoButton) {
                controls.insertBefore(multiAgentBtn, autoButton);
            } else {
                controls.appendChild(multiAgentBtn);
            }
        }
    }

    // MODIFIED: Update processAudio to handle multi-agent mode
    async function processAudio(audioBlob) {
        if (multiAgentMode) {
            return await processMultiAgentAudio(audioBlob);
        }
        
        // Original single-agent processing continues here...
        try {
            console.log(`processAudio: Processing audio blob of size: ${audioBlob.size} bytes, type: ${audioBlob.type}`);
            updateStatus('Processing...');
            
            const formData = new FormData();
            formData.append('audio', audioBlob);
            formData.append('voice_id', currentVoiceId);
            formData.append('conversation_id', currentConversationId);
            
            const response = await fetch('/process_audio', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error(`Server returned status: ${response.status}`);
            }
            
            const data = await response.json();
            
            if (data.status === 'success') {
                addMessage('user', data.user_transcription);
                addMessage('assistant', data.assistant_response_text);
                
                if (data.assistant_response_audio) {
                    playAudioResponse(data.assistant_response_audio);
                }
                
                await loadConversationHistory();
                updateStatus('Ready');
            } else if (data.status === 'exit') {
                addMessage('assistant', data.assistant_response_text);
                updateStatus('Conversation ended');
                await loadConversationHistory();
            } else {
                throw new Error(data.message || 'Failed to process audio');
            }
        } catch (error) {
            console.error('processAudio: Error processing audio:', error);
            updateStatus(`Error: ${error.message || 'Failed to process audio'}`);
        }
    }

    // Add message to conversation
    function addMessage(role, content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role}`;
        messageDiv.textContent = content;
        conversationElement.appendChild(messageDiv);
        conversationElement.scrollTop = conversationElement.scrollHeight;
    }

    // Helper functions
    function float32ToWav(float32, sampleRate = 16000) {
        const length = float32.length;
        const buffer = new ArrayBuffer(44 + length * 2);
        const view = new DataView(buffer);
        
        const write = (offset, str) =>
            str.split('').forEach((s, i) => view.setUint8(offset + i, s.charCodeAt(0)));
        
        // RIFF Header
        write(0, 'RIFF');
        view.setUint32(4, 36 + length * 2, true);
        write(8, 'WAVE');
        write(12, 'fmt ');
        view.setUint32(16, 16, true);
        view.setUint16(20, 1, true);
        view.setUint16(22, 1, true);
        view.setUint32(24, sampleRate, true);
        view.setUint32(28, sampleRate * 2, true);
        view.setUint16(32, 2, true);
        view.setUint16(34, 16, true);
        write(36, 'data');
        view.setUint32(40, length * 2, true);
        
        // PCM Data
        for (let i = 0; i < length; i++) {
            const sample = Math.max(-1, Math.min(1, float32[i]));
            view.setInt16(44 + i * 2, sample * 0x7FFF, true);
        }
        
        return new Blob([buffer], { type: 'audio/wav' });
    }

    function updateStatus(message) {
        if (statusElement) {
            statusElement.textContent = message;
        }
    }

    async function playAudioResponse(base64Audio) {
        try {
            if (!base64Audio || base64Audio.length === 0) {
                console.error('playAudioResponse: Empty audio data received');
                return;
            }

            if (!audioContext) {
                console.error('playAudioResponse: AudioContext not initialized!');
                const audioElement = new Audio(`data:audio/mp3;base64,${base64Audio}`);
                audioElement.play();
                return;
            }

            if (audioContext.state !== 'running') {
                console.warn('playAudioResponse: AudioContext is not running');
                const audioElement = new Audio(`data:audio/mp3;base64,${base64Audio}`);
                audioElement.play();
                return;
            }
            
            // Stop any currently playing audio
            if (currentAudioSource) {
                currentAudioSource.stop();
                currentAudioSource.onended = null;
                currentAudioSource = null;
            }
            
            // Convert base64 to ArrayBuffer
            const binaryString = atob(base64Audio);
            const len = binaryString.length;
            const bytes = new Uint8Array(len);
            
            for (let i = 0; i < len; i++) {
                bytes[i] = binaryString.charCodeAt(i);
            }
            
            // Decode audio data
            let audioBuffer;
            try {
                audioBuffer = await audioContext.decodeAudioData(bytes.buffer);
            } catch (decodeError) {
                console.error('playAudioResponse: Failed to decode audio:', decodeError);
                const audioElement = new Audio(`data:audio/mp3;base64,${base64Audio}`);
                audioElement.play();
                return;
            }
            
            // Create and play audio source
            const source = audioContext.createBufferSource();
            source.buffer = audioBuffer;
            source.connect(audioContext.destination);
            
            currentAudioSource = source;
            
            source.onended = () => {
                currentAudioSource = null;
            };
            
            source.start(0);
            
        } catch (error) {
            console.error('playAudioResponse: Error playing audio:', error);
            try {
                const audioBlob = new Blob(
                    [Uint8Array.from(atob(base64Audio), c => c.charCodeAt(0))], 
                    {type: 'audio/mp3'}
                );
                const audioUrl = URL.createObjectURL(audioBlob);
                const audio = new Audio(audioUrl);
                audio.play();
            } catch (fallbackError) {
                console.error('playAudioResponse: All audio playback attempts failed:', fallbackError);
            }
        }
    }

    async function testAudioSystemAsync() {
        setTimeout(async () => {
            console.log('==== AUDIO SYSTEM DIAGNOSTIC (ASYNC) ====');
            console.log('1. Browser capability check:');
            console.log(' - AudioContext supported:', typeof AudioContext !== 'undefined' || typeof webkitAudioContext !== 'undefined');
            console.log(' - MediaRecorder supported:', typeof MediaRecorder !== 'undefined');
            console.log(' - getUserMedia supported:', !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia));
            console.log(' - Current URL protocol:', window.location.protocol);
            console.log(' - Is HTTPS:', window.location.protocol === 'https:');
            console.log(' - Is localhost:', window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1');
            
            if (audioContext) {
                console.log('2. AudioContext status:');
                console.log(' - Sample rate:', audioContext.sampleRate);
                console.log(' - Current state:', audioContext.state);
            } else {
                console.log('2. AudioContext not yet initialized');
            }
            
            console.log('==== DIAGNOSTIC COMPLETE ====');
        }, 0);
    }

    async function loadConversationHistory() {
        // Placeholder function - would load conversation history from backend
        console.log('Loading conversation history...');
    }

    // Manual recording functions
    async function startManualRecording() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ 
                audio: {
                    channelCount: 1,
                    sampleRate: 16000,
                    echoCancellation: true,
                    noiseSuppression: true
                }
            });
            
            recordedChunks = [];
            mediaRecorder = new MediaRecorder(stream);
            
            mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    recordedChunks.push(event.data);
                }
            };
            
            mediaRecorder.onstop = async () => {
                const audioBlob = new Blob(recordedChunks, { type: 'audio/wav' });
                console.log(`Manual recording stopped, processing ${audioBlob.size} bytes`);
                
                // Stop all audio tracks
                stream.getTracks().forEach(track => track.stop());
                
                updateStatus("Processing audio...");
                await processAudio(audioBlob);
                updateStatus("Ready");
                
                // Reset recording state
                isManualRecording = false;
                if (manualRecordBtn) {
                    manualRecordBtn.classList.remove('recording');
                    manualRecordBtn.innerHTML = '<span class="record-icon"></span>Manual Record';
                }
            };
            
            mediaRecorder.start();
            isManualRecording = true;
            updateStatus("Recording... Click stop when done");
            
            if (manualRecordBtn) {
                manualRecordBtn.classList.add('recording');
                manualRecordBtn.innerHTML = '<span class="record-icon"></span>Stop Recording';
            }
            
        } catch (error) {
            console.error('Manual recording error:', error);
            updateStatus("Microphone access required");
        }
    }
    
    function stopManualRecording() {
        if (mediaRecorder && mediaRecorder.state === 'recording') {
            mediaRecorder.stop();
            updateStatus("Processing recording...");
        }
    }

    // Initialize everything
    updateStatus('Ready');
    addMultiAgentButton();
    
    // Initialize personas and other components
    console.log('App initialization complete');
}); 