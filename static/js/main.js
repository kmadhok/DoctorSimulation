document.addEventListener('DOMContentLoaded', async () => {
    // DOM elements
    const recordButton = document.getElementById('recordButton');
    const statusElement = document.getElementById('status');
    const conversationElement = document.getElementById('conversation');
    const simulationSelect = document.getElementById('simulationSelect');
    const voiceSelect = document.getElementById('voiceSelect');
    const conversationListElement = document.getElementById('conversationList');
    const refreshConversationsBtn = document.getElementById('refreshConversationsBtn');
    const newConversationBtn = document.getElementById('newConversationBtn');
    
    // New DOM element for patient details - reposition it within main content
    const patientDetailsPanel = document.createElement('div');
    patientDetailsPanel.id = 'patientDetailsPanel';
    patientDetailsPanel.className = 'patient-details-panel';

    // Create this after DOM is fully loaded
    const mainContent = document.querySelector('.main-content');
    mainContent.appendChild(patientDetailsPanel);
    
    // Audio and VAD variables
    let audioContext = null;
    let currentAudioSource = null; // Track current audio source for interruption
    let currentSimulation = null;
    let currentVoiceId = 'Fritz-PlayAI'; // Default voice
    let currentConversationId = null;
    let isVadActive = false;
    let isProcessingAudio = false;
    
    // Initialize audio context on user interaction
    function initAudioContext() {
        if (!audioContext) {
            audioContext = new (window.AudioContext || window.webkitAudioContext)();
            console.log('AudioContext initialized. Initial state:', audioContext.state);
        }
    }
    
    // Load available simulations
    await loadSimulations();
    
    // Load conversation history
    await loadConversationHistory();
    
    // Set up event listeners
    recordButton.addEventListener('click', toggleVad);
    simulationSelect.addEventListener('change', handleSimulationChange);
    voiceSelect.addEventListener('change', handleVoiceChange);
    refreshConversationsBtn.addEventListener('click', loadConversationHistory);
    newConversationBtn.addEventListener('click', createNewConversation);
    
    // Create a new empty conversation
    async function createNewConversation() {
        try {
            updateStatus('Creating new conversation...');
            
            // Clear simulation selection
            simulationSelect.value = '';
            currentSimulation = null;
            
            // Get current voice selection
            currentVoiceId = voiceSelect.value;
            
            const response = await fetch('/api/conversations/new', {
                method: 'POST'
            });
            
            const data = await response.json();
            
            if (data.status === 'success') {
                currentConversationId = data.conversation_id;
                conversationElement.innerHTML = ''; // Clear conversation display
                
                // Save voice preference for this conversation
                await fetch('/api/update-voice', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        voice_id: currentVoiceId,
                        conversation_id: currentConversationId
                    })
                });
                
                // Enable recording button
                recordButton.disabled = false;
                
                // Refresh the conversation list
                await loadConversationHistory();
                
                updateStatus('Ready');
            } else {
                throw new Error(data.message || 'Failed to create new conversation');
            }
        } catch (error) {
            console.error('Error creating new conversation:', error);
            updateStatus('Error creating new conversation');
        }
    }
    
    // Update status message
    function updateStatus(message) {
        statusElement.textContent = message;
        
        // Clear all status classes
        statusElement.classList.remove('recording', 'processing', 'error');
        
        // Add appropriate class based on status message
        if (message.includes('Recording') || message.includes('Listening')) {
            statusElement.classList.add('recording');
        } else if (message.includes('Processing')) {
            statusElement.classList.add('processing');
        } else if (message.includes('Error')) {
            statusElement.classList.add('error');
        }
    }
    
    // Load available simulations
    async function loadSimulations() {
        try {
            const response = await fetch('/api/patient-simulations');
            const data = await response.json();
            
            if (data.status === 'success') {
                // Clear loading option
                // Keep the "No simulation" option and remove all others
                while (simulationSelect.options.length > 1) {
                    simulationSelect.remove(1);
                }
                
                // Add simulations to select
                data.simulations.forEach(simulation => {
                    const option = document.createElement('option');
                    option.value = simulation;
                    option.textContent = simulation;
                    simulationSelect.appendChild(option);
                });
                
                // Set current simulation if available
                if (data.current_simulation) {
                    simulationSelect.value = data.current_simulation;
                    currentSimulation = data.current_simulation;
                }
            } else {
                throw new Error(data.message || 'Failed to load simulations');
            }
        } catch (error) {
            console.error('Error loading simulations:', error);
            statusElement.textContent = 'Error loading simulations';
        }
    }
    
    // Load conversation history from the server
    async function loadConversationHistory() {
        try {
            updateStatus('Loading conversations...');
            
            const response = await fetch('/api/conversations');
            const data = await response.json();
            
            if (data.status === 'success') {
                renderConversationList(data.conversations);
                updateStatus('Ready');
            } else {
                throw new Error(data.message || 'Failed to load conversations');
            }
        } catch (error) {
            console.error('Error loading conversations:', error);
            updateStatus('Error loading conversations');
        }
    }
    
    // Render the conversation list in the sidebar
    function renderConversationList(conversations) {
        // Clear the list
        conversationListElement.innerHTML = '';
        
        if (conversations.length === 0) {
            const emptyState = document.createElement('div');
            emptyState.className = 'empty-state';
            emptyState.textContent = 'No saved conversations';
            conversationListElement.appendChild(emptyState);
            return;
        }
        
        // Add each conversation to the list
        conversations.forEach(conversation => {
            const item = document.createElement('div');
            item.className = 'conversation-item';
            if (conversation.id === currentConversationId) {
                item.classList.add('active');
            }
            
            // Create conversation title
            const title = document.createElement('div');
            title.className = 'conversation-title';
            title.textContent = conversation.title;
            
            // Create date element
            const date = document.createElement('div');
            date.className = 'conversation-date';
            date.textContent = formatDate(conversation.updated_at);
            
            // Create action buttons
            const actions = document.createElement('div');
            actions.className = 'conversation-actions';
            
            const loadBtn = document.createElement('button');
            loadBtn.className = 'conversation-action-btn load';
            loadBtn.textContent = 'Load';
            loadBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                loadConversation(conversation.id);
            });
            
            const deleteBtn = document.createElement('button');
            deleteBtn.className = 'conversation-action-btn delete';
            deleteBtn.textContent = 'Delete';
            deleteBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                deleteConversation(conversation.id);
            });
            
            actions.appendChild(loadBtn);
            actions.appendChild(deleteBtn);
            
            // Add elements to the item
            item.appendChild(title);
            item.appendChild(date);
            item.appendChild(actions);
            
            // Add item to the list
            conversationListElement.appendChild(item);
        });
    }
    
    // Format a date string
    function formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleString();
    }
    
    // Load a conversation
    async function loadConversation(conversationId) {
        try {
            updateStatus('Loading conversation...');
            
            const response = await fetch(`/api/conversations/${conversationId}/load`, {
                method: 'POST'
            });
            
            const data = await response.json();
            
            if (data.status === 'success') {
                currentConversationId = conversationId;
                
                // Set the simulation if available
                if (data.conversation.simulation_file) {
                    currentSimulation = data.conversation.simulation_file;
                    simulationSelect.value = currentSimulation;
                } else {
                    // Clear simulation if none is associated
                    currentSimulation = null;
                    simulationSelect.value = '';
                }
                
                // Set the voice if available
                if (data.voice_id) {
                    currentVoiceId = data.voice_id;
                    voiceSelect.value = currentVoiceId;
                } else {
                    // Set to default voice
                    currentVoiceId = 'Fritz-PlayAI';
                    voiceSelect.value = currentVoiceId;
                }
                
                // Clear the conversation display
                conversationElement.innerHTML = '';
                
                // Add messages to conversation display
                data.conversation.messages.forEach(message => {
                    addMessage(message.role, message.content);
                });
                
                // If the conversation has an associated simulation, load the patient details
                if (data.conversation.simulation_file) {
                    await loadPatientDetails();
                } else {
                    // Clear patient details panel if no simulation
                    patientDetailsPanel.innerHTML = '';
                }
                
                // Update UI
                updateStatus('Ready');
                recordButton.disabled = false;
                
                // Update active conversation in sidebar
                const items = conversationListElement.querySelectorAll('.conversation-item');
                items.forEach(item => item.classList.remove('active'));
                const activeItem = Array.from(items).find(item => {
                    return item.querySelector('.load').addEventListener('click', () => loadConversation(conversationId));
                });
                if (activeItem) {
                    activeItem.classList.add('active');
                }
            } else {
                throw new Error(data.message || 'Failed to load conversation');
            }
        } catch (error) {
            console.error('Error loading conversation:', error);
            updateStatus('Error loading conversation');
        }
    }
    
    // Delete a conversation
    async function deleteConversation(conversationId) {
        if (!confirm('Are you sure you want to delete this conversation? This action cannot be undone.')) {
            return;
        }
        
        try {
            updateStatus('Deleting conversation...');
            
            const response = await fetch(`/api/conversations/${conversationId}`, {
                method: 'DELETE'
            });
            
            const data = await response.json();
            
            if (data.status === 'success') {
                // If the deleted conversation was the current one, reset
                if (currentConversationId === conversationId) {
                    currentConversationId = null;
                    conversationElement.innerHTML = '';
                }
                
                // Reload the conversation list
                await loadConversationHistory();
                updateStatus('Conversation deleted');
            } else {
                throw new Error(data.message || 'Failed to delete conversation');
            }
        } catch (error) {
            console.error('Error deleting conversation:', error);
            updateStatus('Error deleting conversation');
        }
    }
    
    // Handle simulation change
    async function handleSimulationChange(event) {
        const selectedSimulation = event.target.value;
        
        try {
            statusElement.textContent = 'Loading simulation...';
            recordButton.disabled = true;
            
            // Keep track of current voice selection
            currentVoiceId = voiceSelect.value;
            
            const response = await fetch('/api/select-simulation', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    simulation_file: selectedSimulation
                })
            });
            
            const data = await response.json();
            
            if (data.status === 'success') {
                currentSimulation = data.current_simulation;
                currentConversationId = data.conversation_id;
                statusElement.textContent = 'Ready';
                recordButton.disabled = false;
                conversationElement.innerHTML = ''; // Clear conversation
                
                // Update voice preference for this conversation
                if (currentConversationId) {
                    await fetch('/api/update-voice', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            voice_id: currentVoiceId,
                            conversation_id: currentConversationId
                        })
                    });
                }
                
                // Load patient details if a simulation is selected
                if (selectedSimulation) {
                    await loadPatientDetails();
                } else {
                    // Clear patient details panel if no simulation selected
                    patientDetailsPanel.innerHTML = '';
                }
                
                // Refresh conversation list
                await loadConversationHistory();
            } else {
                throw new Error(data.message || 'Failed to select simulation');
            }
        } catch (error) {
            console.error('Error selecting simulation:', error);
            statusElement.textContent = 'Error selecting simulation';
            recordButton.disabled = true;
        }
    }
    
    // Add voice change handler
    async function handleVoiceChange(event) {
        currentVoiceId = event.target.value;
        
        try {
            updateStatus('Updating voice...');
            
            const response = await fetch('/api/update-voice', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    voice_id: currentVoiceId,
                    conversation_id: currentConversationId
                })
            });
            
            const data = await response.json();
            
            if (data.status === 'success') {
                updateStatus('Voice updated');
            } else {
                throw new Error(data.message || 'Failed to update voice');
            }
        } catch (error) {
            console.error('Error updating voice:', error);
            updateStatus('Error updating voice');
        }
    }
    
    // New function to load patient details
    async function loadPatientDetails() {
        try {
            const response = await fetch('/api/current-patient-details');
            const data = await response.json();
            
            if (data.status === 'success') {
                displayPatientDetails(data.patient_details);
            } else {
                throw new Error(data.message || 'Failed to load patient details');
            }
        } catch (error) {
            console.error('Error loading patient details:', error);
            patientDetailsPanel.innerHTML = '<p class="error">Error loading patient details</p>';
        }
    }
    
    // New function to display patient details
    function displayPatientDetails(details) {
        patientDetailsPanel.innerHTML = '<h3>Patient Details</h3>';
        
        if (!details || Object.keys(details).length === 0) {
            patientDetailsPanel.innerHTML += '<p>No patient details available</p>';
            return;
        }
        
        const detailsList = document.createElement('ul');
        
        // Display each field except 'illness'
        const fieldsToDisplay = {
            'age': 'Age',
            'gender': 'Gender',
            'occupation': 'Occupation',
            'medical_history': 'Medical History',
            'recent_exposure': 'Recent Exposure'
        };
        
        for (const [key, label] of Object.entries(fieldsToDisplay)) {
            if (details[key]) {
                const item = document.createElement('li');
                item.innerHTML = `<strong>${label}:</strong> ${details[key]}`;
                detailsList.appendChild(item);
            }
        }
        
        patientDetailsPanel.appendChild(detailsList);
    }
    
    // Initialize the Silero VAD
    let vad = null;
    let audioChunks = [];
    let isVadInitialized = false;
    
    // Setup microphone access with VAD
    async function setupMicrophone() {
        try {
            // Request microphone permissions
            await navigator.mediaDevices.getUserMedia({ audio: true });
            return true;
        } catch (error) {
            updateStatus(`Error accessing microphone: ${error.message}`);
            console.error('Error accessing microphone:', error);
            return false;
        }
    }
    
    // Initialize VAD model
    async function initializeVad() {
        if (isVadInitialized) return true;
        
        try {
            console.log('Initializing VAD...');
            updateStatus('Initializing voice detection...');
            
            // Load the VAD module
            const { MicVAD } = await import('https://cdn.jsdelivr.net/npm/@ricky0123/vad@0.3.1/dist/bundle.min.js');
            
            // Create AudioContext for sample rate detection
            if (!audioContext) {
                audioContext = new (window.AudioContext || window.webkitAudioContext)();
            }
            
            if (audioContext.state === 'suspended') {
                await audioContext.resume();
            }
            
            // Configure and create VAD instance
            vad = await MicVAD.new({
                onSpeechStart: () => {
                    console.log('VAD: Speech detected');
                    updateStatus('Listening...');
                    audioChunks = []; // Reset chunks at the start of speech
                    recordButton.classList.add('recording');
                },
                onSpeechEnd: async (audio) => {
                    console.log('VAD: Speech ended');
                    updateStatus('Processing...');
                    recordButton.classList.remove('recording');
                    
                    // Convert the audio data to proper format
                    const audioBlob = await float32ArrayToWav(audio.audioData);
                    await processAudio(audioBlob);
                },
                onVADMisfire: () => {
                    console.log('VAD: False positive detected');
                    updateStatus('Ready');
                    recordButton.classList.remove('recording');
                },
                // Additional VAD configuration options
                positiveSpeechThreshold: 0.80,  // Higher threshold for more certainty
                negativeSpeechThreshold: 0.70,  // Lower threshold to detect end of speech faster
                minSpeechFrames: 5,             // Minimum frames of speech needed
                preSpeechPadFrames: 5,          // Frames to include before speech starts
                redemptionFrames: 25,           // How many frames to wait before deciding speech is over
                frameSamples: 1024,             // Samples per frame
                modelUrl: '/static/models/vad/silero_vad.onnx' // Path to our local model file
            });
            
            isVadInitialized = true;
            console.log('VAD initialized successfully');
            updateStatus('Ready');
            return true;
        } catch (error) {
            console.error('Failed to initialize VAD:', error);
            updateStatus('Error initializing voice detection');
            return false;
        }
    }
    
    // Toggle VAD on/off
    async function toggleVad() {
        try {
            // Initialize AudioContext on first interaction
            initAudioContext();
            
            // Create a new conversation if none exists
            if (!currentConversationId) {
                await createNewConversation();
            }
            
            // Stop any currently playing audio
            if (currentAudioSource) {
                currentAudioSource.stop();
                if (currentAudioSource.onended) {
                    currentAudioSource.onended = null;
                }
                currentAudioSource = null;
            }
            
            if (!await setupMicrophone()) {
                return;
            }
            
            if (!isVadInitialized) {
                if (!await initializeVad()) {
                    return;
                }
            }
            
            if (isVadActive) {
                // Stop VAD
                vad.pause();
                isVadActive = false;
                recordButton.classList.remove('active');
                recordButton.querySelector('span').textContent = 'Start Listening';
                updateStatus('Ready');
            } else {
                // Start VAD
                await vad.start();
                isVadActive = true;
                recordButton.classList.add('active');
                recordButton.querySelector('span').textContent = 'Stop Listening';
                updateStatus('Listening for speech...');
            }
        } catch (error) {
            console.error('Error toggling VAD:', error);
            updateStatus('Error with voice detection');
        }
    }
    
    // Convert Float32Array to WAV blob
    async function float32ArrayToWav(audioData) {
        // WAV header generation
        const numChannels = 1;
        const sampleRate = audioContext ? audioContext.sampleRate : 16000;
        const bitsPerSample = 16;
        const bytesPerSample = bitsPerSample / 8;
        const blockAlign = numChannels * bytesPerSample;
        const byteRate = sampleRate * blockAlign;
        const dataSize = audioData.length * bytesPerSample;
        const buffer = new ArrayBuffer(44 + dataSize);
        const view = new DataView(buffer);
        
        // Write WAV header
        // "RIFF" chunk descriptor
        writeString(view, 0, 'RIFF');
        view.setUint32(4, 36 + dataSize, true);
        writeString(view, 8, 'WAVE');
        
        // "fmt " sub-chunk
        writeString(view, 12, 'fmt ');
        view.setUint32(16, 16, true);             // SubChunk1Size (16 for PCM)
        view.setUint16(20, 1, true);              // AudioFormat (1 for PCM)
        view.setUint16(22, numChannels, true);    // NumChannels
        view.setUint32(24, sampleRate, true);     // SampleRate
        view.setUint32(28, byteRate, true);       // ByteRate
        view.setUint16(32, blockAlign, true);     // BlockAlign
        view.setUint16(34, bitsPerSample, true);  // BitsPerSample
        
        // "data" sub-chunk
        writeString(view, 36, 'data');
        view.setUint32(40, dataSize, true);       // SubChunk2Size
        
        // Write audio data
        floatTo16BitPCM(view, 44, audioData);
        
        return new Blob([buffer], { type: 'audio/wav' });
    }
    
    // Utility to write string to DataView
    function writeString(view, offset, string) {
        for (let i = 0; i < string.length; i++) {
            view.setUint8(offset + i, string.charCodeAt(i));
        }
    }
    
    // Convert Float32 to 16-bit PCM
    function floatTo16BitPCM(output, offset, input) {
        for (let i = 0; i < input.length; i++) {
            const s = Math.max(-1, Math.min(1, input[i]));
            output.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
            offset += 2;
        }
    }
    
    // Process audio
    async function processAudio(audioBlob) {
        if (isProcessingAudio) {
            console.log('Already processing audio, ignoring new request');
            return;
        }
        
        isProcessingAudio = true;
        
        try {
            console.log(`Processing audio blob of size: ${audioBlob.size} bytes, type: ${audioBlob.type}`);
            statusElement.textContent = 'Processing...';
            
            const formData = new FormData();
            formData.append('audio', audioBlob);
            formData.append('voice_id', currentVoiceId);
            console.log(`Using voice_id: ${currentVoiceId}`);
            
            console.log('Sending audio to server...');
            const response = await fetch('/process_audio', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error(`Server returned status: ${response.status}`);
            }
            
            const data = await response.json();
            console.log('Server response received', {
                status: data.status,
                transcription_length: data.user_transcription?.length,
                response_length: data.assistant_response_text?.length,
                audio_received: !!data.assistant_response_audio
            });
            
            if (data.status === 'success') {
                // Add user message
                addMessage('user', data.user_transcription);
                
                // Add assistant message
                addMessage('assistant', data.assistant_response_text);
                
                // Play audio response if available
                if (data.assistant_response_audio) {
                    console.log(`Audio response received, length: ${data.assistant_response_audio.length}`);
                    await playAudioResponse(data.assistant_response_audio);
                } else {
                    console.warn('No audio response received from server');
                }
                
                // Refresh conversation list to show the updated conversation
                await loadConversationHistory();
                
                statusElement.textContent = isVadActive ? 'Listening for speech...' : 'Ready';
            } else if (data.status === 'exit') {
                console.log('Exit command detected');
                addMessage('assistant', data.assistant_response_text);
                statusElement.textContent = 'Conversation ended';
                recordButton.disabled = true;
                
                // Stop VAD if active
                if (isVadActive && vad) {
                    vad.pause();
                    isVadActive = false;
                    recordButton.classList.remove('active');
                }
                
                // Refresh conversation list
                await loadConversationHistory();
            } else {
                throw new Error(data.message || 'Failed to process audio');
            }
        } catch (error) {
            console.error('Error processing audio:', error);
            statusElement.textContent = `Error: ${error.message || 'Failed to process audio'}`;
        } finally {
            isProcessingAudio = false;
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
    
    // Play audio response
    async function playAudioResponse(base64Audio) {
        try {
            console.log('Playing audio response with length:', base64Audio ? base64Audio.length : 0);
            
            if (!base64Audio || base64Audio.length === 0) {
                console.error('Empty audio data received');
                return;
            }

            // Initialize audio context if not already done
            if (!audioContext) {
                audioContext = new (window.AudioContext || window.webkitAudioContext)();
                console.log('AudioContext initialized with state:', audioContext.state);
            }

            // Resume AudioContext - this is critical for browsers that suspend by default
            if (audioContext.state === 'suspended') {
                console.log('AudioContext is suspended, attempting to resume...');
                await audioContext.resume();
                console.log('AudioContext resume attempt completed. New state:', audioContext.state);
            }
            
            // Stop any currently playing audio
            if (currentAudioSource) {
                console.log('Stopping existing audio source');
                currentAudioSource.stop();
                currentAudioSource.onended = null; // Clear previous handler
                currentAudioSource = null;
            }
            
            // Convert base64 to ArrayBuffer
            console.log('Converting base64 to ArrayBuffer');
            const binaryString = atob(base64Audio);
            const len = binaryString.length;
            const bytes = new Uint8Array(len);
            
            for (let i = 0; i < len; i++) {
                bytes[i] = binaryString.charCodeAt(i);
            }
            
            console.log(`Created bytes array of length ${bytes.length}`);
            
            // Decode audio data
            console.log('Decoding audio data...');
            let audioBuffer;
            try {
                audioBuffer = await audioContext.decodeAudioData(bytes.buffer);
                console.log(`Audio successfully decoded, duration: ${audioBuffer.duration}s, channels: ${audioBuffer.numberOfChannels}`);
            } catch (decodeError) {
                console.error('Failed to decode audio:', decodeError);
                // Try playing as a regular HTML5 audio element as fallback
                console.log('Attempting HTML5 Audio fallback');
                const audioElement = new Audio(`data:audio/mp3;base64,${base64Audio}`);
                audioElement.play().then(() => {
                    console.log('HTML5 Audio fallback successful');
                }).catch(htmlAudioError => {
                    console.error('HTML5 Audio fallback failed:', htmlAudioError);
                });
                return;
            }
            
            // Create and play audio source
            console.log('Creating audio source');
            const source = audioContext.createBufferSource();
            source.buffer = audioBuffer;
            source.connect(audioContext.destination);
            
            // Save reference to current source for potential interruption
            currentAudioSource = source;
            
            // Add event handlers
            source.onended = () => {
                console.log('Audio playback completed naturally');
                currentAudioSource = null;
            };
            
            // Actually play the audio
            console.log('Starting audio playback');
            source.start(0);
            console.log('Audio playback started');
            
        } catch (error) {
            console.error('Error playing audio:', error);
            // Try one more fallback approach with vanilla HTML audio
            try {
                console.log('Attempting final HTML5 Audio fallback');
                const audioBlob = new Blob(
                    [Uint8Array.from(atob(base64Audio), c => c.charCodeAt(0))], 
                    {type: 'audio/mp3'}
                );
                const audioUrl = URL.createObjectURL(audioBlob);
                const audio = new Audio(audioUrl);
                audio.play();
                console.log('Final HTML5 Audio fallback attempted');
            } catch (fallbackError) {
                console.error('All audio playback attempts failed:', fallbackError);
            }
        }
    }
    
    // Add touch support for mobile devices
    recordButton.addEventListener('touchstart', async function(e) {
        e.preventDefault(); // Prevent default touch behavior
        toggleVad();
    });
    
    // Update DOM structure to fix layout
    function updateLayoutStructure() {
        const mainContent = document.querySelector('.main-content');
        const main = document.querySelector('main');
        
        // Move patient details panel before main
        mainContent.insertBefore(patientDetailsPanel, main);
    }
    
    // Update the record button styles for VAD
    function styleRecordButton() {
        recordButton.innerHTML = `
            <div class="record-button-inner">
                <div class="record-icon"></div>
                <span>Start Listening</span>
            </div>
        `;
        recordButton.classList.add('vad-button');
    }
    
    // Add diagnostic function to test audio system
    async function testAudioSystem() {
        console.log('==== AUDIO SYSTEM DIAGNOSTIC ====');
        
        // Check if browser supports necessary audio APIs
        console.log('1. Browser capability check:');
        console.log(' - AudioContext supported:', typeof AudioContext !== 'undefined' || typeof webkitAudioContext !== 'undefined');
        console.log(' - MediaRecorder supported:', typeof MediaRecorder !== 'undefined');
        console.log(' - getUserMedia supported:', navigator.mediaDevices && typeof navigator.mediaDevices.getUserMedia !== 'undefined');
        
        // Test AudioContext creation
        console.log('2. AudioContext creation test:');
        try {
            const testContext = new (window.AudioContext || window.webkitAudioContext)();
            console.log(' - AudioContext created successfully');
            console.log(' - Sample rate:', testContext.sampleRate);
            console.log(' - Initial state:', testContext.state);
            
            // Test resume capability
            if (testContext.state === 'suspended') {
                try {
                    console.log(' - Attempting to resume AudioContext...');
                    await testContext.resume();
                    console.log(' - Resume successful, new state:', testContext.state);
                } catch (resumeError) {
                    console.error(' - Error resuming AudioContext:', resumeError);
                }
            }
            
            // Clean up
            testContext.close();
        } catch (contextError) {
            console.error(' - Error creating AudioContext:', contextError);
        }
        
        console.log('==== DIAGNOSTIC COMPLETE ====');
    }

    // Initialize the app
    styleRecordButton();
    updateLayoutStructure();
    updateStatus('Ready');
    
    // Run audio system diagnostic
    testAudioSystem().catch(err => console.error('Audio diagnostic error:', err));
}); 