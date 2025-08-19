// NEW: Diagnosis panel variables (moved to global scope)
let diagnosisPanelVisible = false;
let currentPatientDiagnosis = null;
let diagnosisAttemptCount = 0;
const maxDiagnosisAttempts = 3;

// Move currentConversationId to global scope for diagnosis functions
let currentConversationId = null;

/**
 * AUDIO QUEUE BEHAVIOR NOTE:
 * 
 * When users interrupt (barge-in), we clear the audio queue to prevent
 * outdated responses from playing. However, these interrupted responses
 * remain in the database and conversation history since they were already
 * processed and saved server-side.
 * 
 * This means:
 * - Database conversation history may include responses user didn't hear
 * - AI agents will reference these responses in future interactions
 * - Users can review full conversation history if needed
 * 
 * This behavior mirrors real-world medical consultations where interruptions
 * can occur mid-sentence but the speaker's intended message was still formed.
 */

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

    // --- Audio queue state ---
    const IDLE_MS = 5000;           // 5 s of silence triggers auto-turn
    let audioQueue = [];
    let isAudioPlaying = false;
    let idleHandle = null;
    // NEW: single-source-of-truth playback state helpers
    let pendingResolve = null;    // promise resolver for the clip currently playing
    let currentSpeaker = null;    // who is speaking (for logging)
    // NEW: Audio source ID tracking to prevent race conditions
    let currentAudioSourceId = 0; // Unique ID for each audio source
    let activeAudioSourceId = null; // ID of the currently valid audio source
    // NEW: Request ID tracking to prevent server-side race conditions
    let currentRequestId = 0; // Unique ID for each server request
    let activeRequestId = null; // ID of the currently valid request

    function cancelIdleTimer() {
        if (idleHandle) {
            clearTimeout(idleHandle);
            idleHandle = null;
        }
    }

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
                    
                    if (isAudioPlaying) {
                        handleUserBargeIn();
                    }
                    
                    updateStatus("Listening...");
                    cancelIdleTimer();
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

    // Conversation sidebar event listeners
    if (refreshConversationsBtn) {
        refreshConversationsBtn.addEventListener('click', async (event) => {
            event.preventDefault();
            console.log('Refresh conversations button clicked');
            await loadConversationHistory();
        });
        console.log('Refresh conversations button listener attached');
    }

    if (newConversationBtn) {
        newConversationBtn.addEventListener('click', (event) => {
            event.preventDefault();
            console.log('New conversation button clicked');
            createNewConversation();
        });
        console.log('New conversation button listener attached');
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
                
                // ✅ FIX: Initialize AudioContext for multi-agent playback
                if (!audioContext) {
                    audioContext = new (window.AudioContext || window.webkitAudioContext)();
                    console.log('AudioContext initialized for multi-agent mode');
                }
                
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
            
            // NEW: Generate unique request ID and mark as active
            const requestId = ++currentRequestId;
            activeRequestId = requestId;
            console.log(`🔄 Starting multi-agent request ${requestId}`);
            
            // Clear any stale audio queue
            if (audioQueue.length > 0) {
                const queuedSpeakers = audioQueue.map(item => item.speaker || 'Unknown').join(', ');
                console.log(`🔄 Multi-agent: clearing ${audioQueue.length} stale audio items before processing new input`);
                console.log(`🔄 Interrupted speakers: ${queuedSpeakers}`);
                console.log('⚠️ Note: Cleared items were already saved to database');
                audioQueue.length = 0;
            }
            
            const formData = new FormData();
            formData.append('audio', audioBlob);
            formData.append('conversation_id', currentConversationId);
            
            if (currentVoiceId) {
                formData.append('voice_id', currentVoiceId);
            }
            
            const response = await fetch('/process_audio_multi_agent', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            // NEW: Check if this request is still active before processing response
            if (activeRequestId !== requestId) {
                console.log(`🔇 Ignoring response from outdated request ${requestId} (current: ${activeRequestId})`);
                console.log('⚠️ User has moved on to newer input, discarding stale server response');
                return;
            }
            
            if (data.status === 'success') {
                console.log(`✅ Processing valid response from request ${requestId}`);
                
                // Add user message
                addMessage('user', data.user_transcription);
                
                // Add each agent response with speaker labels
                for (const response of data.responses) {
                    addMultiAgentMessage(response);
                    
                    // Play audio response (only if request is still active)
                    if (response.audio && activeRequestId === requestId) {
                        await playAudioResponse(response.audio, response.speaker);
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
        
        try {
            console.log(`processAudio: Processing audio blob of size: ${audioBlob.size} bytes, type: ${audioBlob.type}`);
            updateStatus('Processing...');
            
            // NEW: Generate unique request ID and mark as active
            const requestId = ++currentRequestId;
            activeRequestId = requestId;
            console.log(`🔄 Starting single-agent request ${requestId}`);
            
            // Clear any stale audio queue
            if (audioQueue.length > 0) {
                const queuedSpeakers = audioQueue.map(item => item.speaker || 'Unknown').join(', ');
                console.log(`🔄 Clearing ${audioQueue.length} stale audio items before processing new input`);
                console.log(`🔄 Interrupted speakers: ${queuedSpeakers}`);
                console.log('⚠️ Note: Cleared items were already saved to database');
                audioQueue.length = 0;
            }
            
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
            
            // NEW: Check if this request is still active before processing response
            if (activeRequestId !== requestId) {
                console.log(`🔇 Ignoring response from outdated request ${requestId} (current: ${activeRequestId})`);
                console.log('⚠️ User has moved on to newer input, discarding stale server response');
                return;
            }
            
            if (data.status === 'success') {
                console.log(`✅ Processing valid response from request ${requestId}`);
                
                addMessage('user', data.user_transcription);
                addMessage('assistant', data.assistant_response_text);
                
                if (data.assistant_response_audio && activeRequestId === requestId) {
                    await playAudioResponse(data.assistant_response_audio, 'Assistant');
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

    // NEW: Add this helper function for debugging (can be removed in production)
    function logAudioQueueState(context) {
        if (audioQueue.length > 0) {
            const speakers = audioQueue.map(item => item.speaker || 'Unknown').join(', ');
            console.log(`[AUDIO QUEUE] ${context}: ${audioQueue.length} items queued from [${speakers}], currently playing: ${isAudioPlaying ? currentSpeaker : 'none'}`);
        } else {
            console.log(`[AUDIO QUEUE] ${context}: Empty queue, currently playing: ${isAudioPlaying ? currentSpeaker : 'none'}`);
        }
    }

    // NEW: Debug helper for audio source state
    function logAudioSourceState(context) {
        console.log(`[AUDIO SOURCE] ${context}: Current ID: ${currentAudioSourceId}, Active ID: ${activeAudioSourceId}, Playing: ${isAudioPlaying ? currentSpeaker : 'none'}`);
    }

    // NEW: Debug helper for request state
    function logRequestState(context) {
        console.log(`[REQUEST] ${context}: Current ID: ${currentRequestId}, Active ID: ${activeRequestId}`);
    }

    // -------------------------------------------------------------
    // Playback finalisation & barge-in helpers
    function finalizePlayback(reason = 'completed') {
        if (!isAudioPlaying) return;

        console.log(`[AUDIO] ${reason} - ${currentSpeaker || 'unknown'}`);

        currentAudioSource = null;
        isAudioPlaying = false;
        currentSpeaker = null;

        try {
            pendingResolve?.();
        } finally {
            pendingResolve = null;
        }

        // Only advance queue if not interrupted
        if (reason !== 'interrupted') {
            processAudioQueue();
            if (!isAudioPlaying && audioQueue.length === 0 && !idleHandle) {
                idleHandle = setTimeout(onIdle, IDLE_MS);
            }
        } else {
            console.log('[AUDIO] Skipping queue processing due to user interruption');
            // Schedule idle timer since queue is now empty
            if (!idleHandle) {
                idleHandle = setTimeout(onIdle, IDLE_MS);
            }
        }
    }

    function handleUserBargeIn() {
        if (!currentAudioSource) return;
        
        const queuedCount = audioQueue.length;
        const queuedSpeakers = audioQueue.map(item => item.speaker || 'Unknown').join(', ');
        
        console.log(`🔇 User barge-in detected - stopping current audio and clearing queue`);
        console.log(`🔇 Barge-in: stopping audio, clearing ${queuedCount} queued items`);
        
        if (queuedCount > 0) {
            console.log(`🔇 About to clear ${queuedCount} queued responses from: ${queuedSpeakers}`);
            console.log('⚠️ Note: These responses are already saved in database but won\'t be heard by user');
        }
        
        // NEW: Invalidate current request to ignore pending server responses
        activeRequestId = null;
        console.log('🔇 Invalidated current request to prevent server race conditions');
        
        // NEW: Invalidate the current audio source to prevent late onended events
        activeAudioSourceId = null;
        console.log('🔇 Invalidated current audio source to prevent race conditions');
        
        try {
            currentAudioSource.stop();
        } catch (e) {
            // ignore race where source already ended
        }
        
        // Resolve pending promises before clearing
        audioQueue.forEach(item => {
            if (item.resolve) {
                try {
                    item.resolve();
                } catch (e) {}
            }
        });
        
        // Clear the audio queue
        audioQueue.length = 0;
        console.log('🔇 Audio queue cleared due to user interruption');
        
        finalizePlayback('interrupted');
    }

    // Push a clip onto the queue and kick the worker
    async function playAudioResponse(base64Audio, speaker = 'Assistant') {
        return new Promise(resolve => {
            cancelIdleTimer();
            audioQueue.push({ base64Audio, speaker, resolve });
            processAudioQueue();
        });
    }

    async function processAudioQueue() {
        if (isAudioPlaying || audioQueue.length === 0) return;

        const { base64Audio, speaker, resolve } = audioQueue.shift();
        isAudioPlaying = true;
        pendingResolve = resolve;
        currentSpeaker = speaker;

        try {
            if (!base64Audio) {
                console.error(`[AUDIO] ${speaker} – empty payload`);
                finalizePlayback('empty');
                return;
            }

            // Fallback when AudioContext is not ready
            if (!audioContext || audioContext.state !== 'running') {
                console.log(`[AUDIO] Using HTML Audio fallback for ${speaker}`);
                const element = new Audio(`data:audio/mp3;base64,${base64Audio}`);
                
                // NEW: Assign unique ID and track active source
                const sourceId = ++currentAudioSourceId;
                // Handle integer overflow (extremely unlikely but defensive programming)
                if (currentAudioSourceId > Number.MAX_SAFE_INTEGER - 1000) {
                    currentAudioSourceId = 1;
                    console.log('[AUDIO] Reset audio source ID counter due to overflow');
                }
                activeAudioSourceId = sourceId;
                console.log(`[AUDIO] Created HTML audio source ${sourceId} for ${speaker}`);
                
                element.onended = () => {
                    // NEW: Only finalize if this source is still active
                    if (activeAudioSourceId === sourceId) {
                        console.log(`[AUDIO] Valid completion from HTML source ${sourceId} (${speaker})`);
                        finalizePlayback('completed');
                    } else {
                        console.log(`[AUDIO] Ignoring onended from invalidated HTML source ${sourceId} (${speaker})`);
                    }
                };
                element.onerror = (err) => {
                    if (activeAudioSourceId === sourceId) {
                        console.error(`[AUDIO] ${speaker} playback failed (HTML Audio):`, err);
                        finalizePlayback('error');
                    } else {
                        console.log(`[AUDIO] Ignoring onerror from invalidated HTML source ${sourceId} (${speaker})`);
                    }
                };
                element.play().catch(err => {
                    if (activeAudioSourceId === sourceId) {
                        console.error(`[AUDIO] ${speaker} play() failed:`, err);
                        finalizePlayback('error');
                    } else {
                        console.log(`[AUDIO] Ignoring play error from invalidated HTML source ${sourceId} (${speaker})`);
                    }
                });
                return;
            }

            // Base-64 → Uint8Array
            console.log(`[AUDIO] Decoding audio for ${speaker} using AudioContext`);
            const bytes = Uint8Array.from(atob(base64Audio), c => c.charCodeAt(0));
            const audioBuffer = await audioContext.decodeAudioData(bytes.buffer);

            const source = audioContext.createBufferSource();
            source.buffer = audioBuffer;
            source.connect(audioContext.destination);
            currentAudioSource = source;

            // NEW: Assign unique ID and track active source
            const sourceId = ++currentAudioSourceId;
            // Handle integer overflow (extremely unlikely but defensive programming)
            if (currentAudioSourceId > Number.MAX_SAFE_INTEGER - 1000) {
                currentAudioSourceId = 1;
                console.log('[AUDIO] Reset audio source ID counter due to overflow');
            }
            activeAudioSourceId = sourceId;
            console.log(`[AUDIO] Created AudioContext source ${sourceId} for ${speaker}`);

            source.onended = () => {
                // NEW: Only finalize if this source is still active
                if (activeAudioSourceId === sourceId) {
                    console.log(`[AUDIO] Valid completion from AudioContext source ${sourceId} (${speaker})`);
                    finalizePlayback('completed');
                } else {
                    console.log(`[AUDIO] Ignoring onended from invalidated AudioContext source ${sourceId} (${speaker})`);
                }
            };

            console.log(`[AUDIO] Starting playback for ${speaker}`);
            source.start(0);
        } catch (err) {
            console.error('Audio playback failed', err);
            finalizePlayback('error');
        }
    }

    async function onIdle() {
        cancelIdleTimer();
        try {
            const resp = await fetch('/continue_multi_agent', { method: 'POST' });
            const data = await resp.json();
            if (data.status === 'success') {
                for (const r of data.responses) {
                    addMultiAgentMessage(r);
                    if (r.audio) {
                        await playAudioResponse(r.audio, r.speaker);
                    }
                }
            }
        } catch (err) {
            console.error('onIdle error', err);
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
        try {
            console.log('Loading conversation history from backend...');
            const response = await fetch('/api/conversations');
            const conversations = await response.json();
            
            const conversationListElement = document.getElementById('conversationList');
            if (!conversationListElement) {
                console.error('Conversation list element not found');
                return;
            }
            
            // Clear existing content
            conversationListElement.innerHTML = '';
            
            if (!conversations || conversations.length === 0) {
                conversationListElement.innerHTML = '<div class="empty-state">No saved conversations</div>';
                return;
            }
            
            // Render each conversation
            conversations.forEach(conversation => {
                const conversationItem = document.createElement('div');
                conversationItem.className = 'conversation-item';
                conversationItem.dataset.conversationId = conversation.id;
                
                // Format the date
                const createdDate = new Date(conversation.created_at);
                const formattedDate = createdDate.toLocaleDateString() + ' ' + 
                                   createdDate.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
                
                conversationItem.innerHTML = `
                    <div class="conversation-title">${conversation.title}</div>
                    <div class="conversation-meta">
                        <span class="conversation-date">${formattedDate}</span>
                        ${conversation.simulation_file ? `<span class="conversation-type">File: ${conversation.simulation_file}</span>` : ''}
                    </div>
                `;
                
                // Add click handler to load conversation
                conversationItem.addEventListener('click', () => loadConversation(conversation.id));
                
                conversationListElement.appendChild(conversationItem);
            });
            
            console.log(`Loaded ${conversations.length} conversations`);
            
        } catch (error) {
            console.error('Error loading conversation history:', error);
            const conversationListElement = document.getElementById('conversationList');
            if (conversationListElement) {
                conversationListElement.innerHTML = '<div class="error-state">Failed to load conversations</div>';
            }
        }
    }
    
    async function loadConversation(conversationId) {
        try {
            console.log(`Loading conversation ${conversationId}...`);
            const response = await fetch(`/api/conversations/${conversationId}`);
            const conversation = await response.json();
            
            if (!conversation) {
                console.error('Conversation not found');
                return;
            }
            
            // Clear current conversation display
            const conversationElement = document.getElementById('conversation');
            if (conversationElement) {
                conversationElement.innerHTML = '';
            }
            
            // Load conversation messages
            if (conversation.messages && conversation.messages.length > 0) {
                conversation.messages.forEach(message => {
                    addMessage(message.role, message.content);
                });
            }
            
            // Update current conversation ID
            currentConversationId = conversationId;
            
            // Highlight selected conversation in sidebar
            document.querySelectorAll('.conversation-item').forEach(item => {
                item.classList.remove('active');
            });
            const selectedItem = document.querySelector(`[data-conversation-id="${conversationId}"]`);
            if (selectedItem) {
                selectedItem.classList.add('active');
            }
            
            console.log(`Loaded conversation: ${conversation.title}`);
            updateStatus(`Loaded: ${conversation.title}`);
            
        } catch (error) {
            console.error('Error loading conversation:', error);
            updateStatus('Failed to load conversation');
        }
    }
    
    function createNewConversation() {
        // Clear current conversation
        const conversationElement = document.getElementById('conversation');
        if (conversationElement) {
            conversationElement.innerHTML = '';
        }
        
        // Reset conversation ID
        currentConversationId = null;
        
        // Clear active selection in sidebar
        document.querySelectorAll('.conversation-item').forEach(item => {
            item.classList.remove('active');
        });
        
        console.log('Started new conversation');
        updateStatus('New conversation started');
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
    
    // Load conversation history on page load
    await loadConversationHistory();
    
    // Initialize personas and other components
    console.log('App initialization complete');
}); 