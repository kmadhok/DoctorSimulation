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
    let currentConversationId = null;
    let recordedMimeType = '';
    let currentAudioSource = null; // Track current audio source for interruption
    let microphoneSetup = false;

    // Get DOM elements
    // const autoListenBtn = document.getElementById('autoListenBtn');
    // const statusElement = document.getElementById('status');

    async function initAutoVAD() {
        console.log('initAutoVAD: Starting VAD initialization...');
        
        const myvad = await vad.MicVAD.new({
              /* tell VAD where every asset lives on _your_ server */
              baseAssetPath:        '/static/vad-model/',   // .onnx + worklet
              onnxWASMBasePath:     '/static/vad-model/',   // .wasm trio
            
               // (optional – keeps things explicit, but you could omit
               //  because they're derived from baseAssetPath anyway)
               workletURL: '/static/vad-model/vad.worklet.bundle.min.js',
               modelURL:   '/static/vad-model/silero_vad_legacy.onnx',
            
               positiveSpeechThreshold: 0.8,
               negativeSpeechThreshold: 0.5,
               preSpeechPadFrames: 8,
               minSpeechFrames: 3,
               redemptionFrames: 10,
            
               onSpeechStart()  { updateStatus('Listening…') },
               onSpeechEnd     : async (audio) => {
                // … 
                },
            });

        
        try {
            console.log('initAutoVAD: Creating MicVAD instance with config:', {
                positiveSpeechThreshold: 0.8,
                negativeSpeechThreshold: 0.5,
                preSpeechPadFrames: 8,
                minSpeechFrames: 3,
                redemptionFrames: 10
            });

            // Using vad.MicVAD with proper model and worklet paths
            const myvad = await vad.MicVAD.new({
                modelPath: '/static/vad-model/silero_vad_legacy.onnx',
                workletPath: '/static/vad-worklet/vad.worklet.bundle.min.js',
                positiveSpeechThreshold: 0.8,
                negativeSpeechThreshold: 0.5,
                preSpeechPadFrames: 8,
                minSpeechFrames: 3,
                redemptionFrames: 10,

                onSpeechStart: () => {
                    console.log('initAutoVAD: Speech detected, starting recording...');
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
            throw error;
        }
    }

    // DOM elements
    const autoListenBtn = document.getElementById('autoListenBtn');  // ✅ new
    const statusElement = document.getElementById('status');
    const conversationElement = document.getElementById('conversation');
    const simulationSelect = document.getElementById('simulationSelect');
    const voiceSelect = document.getElementById('voiceSelect');
    const conversationListElement = document.getElementById('conversationList');
    const refreshConversationsBtn = document.getElementById('refreshConversationsBtn');
    const newConversationBtn = document.getElementById('newConversationBtn');
    
    if (autoListenBtn) {
        autoListenBtn.addEventListener('click', async (event) => {
            event.preventDefault();
            event.stopPropagation();
            
            console.log('Button clicked, current stopVAD state:', !!stopVAD);
            
            try {
                if (!stopVAD) {
                    // Initialize AudioContext and run diagnostic once
                    if (!audioContext) {
                        audioContext = new (window.AudioContext || window.webkitAudioContext)();
                        console.log('AudioContext initialized, running system diagnostic...');
                        // Run diagnostic once when AudioContext is first created
                        testAudioSystemAsync();
                    }
                    
                    // Simple microphone access using modern API
                    try {
                        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                        stream.getTracks().forEach(t => t.stop()); // Release temporary stream
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

    // New DOM element for patient details - reposition it within main content
    const patientDetailsPanel = document.createElement('div');
    patientDetailsPanel.id = 'patientDetailsPanel';
    patientDetailsPanel.className = 'patient-details-panel';

    // Create this after DOM is fully loaded
    const mainContent = document.querySelector('.main-content');
    mainContent.appendChild(patientDetailsPanel);
    
    function float32ToWav(float32, sampleRate = 16000) {
        const buffer = new ArrayBuffer(44 + float32.length * 2);
        const view   = new DataView(buffer);
      
        // ----- RIFF header -----
        const write = (offset, str) =>
            str.split('').forEach((s, i) => view.setUint8(offset + i, s.charCodeAt(0)));
      
        write(0,  'RIFF');
        view.setUint32(4, 36 + float32.length * 2, true);
        write(8,  'WAVE');
        write(12, 'fmt ');
        view.setUint32(16, 16, true);   // Sub-chunk size
        view.setUint16(20, 1,  true);   // PCM
        view.setUint16(22, 1,  true);   // Mono
        view.setUint32(24, sampleRate, true);
        view.setUint32(28, sampleRate * 2, true); // Byte rate
        view.setUint16(32, 2,  true);   // Block align
        view.setUint16(34, 16, true);   // Bits / sample
        write(36, 'data');
        view.setUint32(40, float32.length * 2, true);
      
        // PCM samples
        for (let i = 0; i < float32.length; i++) {
          const s = Math.max(-1, Math.min(1, float32[i]));
          view.setInt16(44 + i * 2, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
        }
        return new Blob([view], { type: "audio/wav" });
      }
      
    
    // // Initialize audio context on user interaction
    // function initAudioContext() {
    //     if (!audioContext) {
    //         audioContext = new (window.AudioContext || window.webkitAudioContext)();
    //         console.log('AudioContext initialized. Initial state:', audioContext.state);

    //     }
    // }
    
    // Load available simulations
    console.log('<<<<< MAIN.JS: Awaiting loadSimulations... >>>>>');
    await loadConversationHistory();
    console.log('<<<<< MAIN.JS: loadSimulations complete. >>>>>');    

    console.log('<<<<< MAIN.JS: Awaiting loadConversationHistory... >>>>>');
    await loadConversationHistory();
    console.log('<<<<< MAIN.JS: loadConversationHistory complete. >>>>>');

    // Load conversation history
    // await loadConversationHistory();
    
    // Set up event listeners
    // recordButton.addEventListener('mousedown', startRecording);
    // recordButton.addEventListener('mouseup', stopRecording);
    // recordButton.addEventListener('mouseleave', stopRecording);
    simulationSelect.addEventListener('change', handleSimulationChange);
    voiceSelect.addEventListener('change', handleVoiceChange);
    refreshConversationsBtn.addEventListener('click', loadConversationHistory);
    newConversationBtn.addEventListener('click', createNewConversation);
    // autoListenBtn.addEventListener('click', async () => {
    //     if (!stopVAD) {
    //       updateStatus("Listening…");
    //       autoListenBtn.classList.add('recording');
    //       stopVAD = await initAutoVAD();    // starts everything
    //     } else {
    //       stopVAD();                        // pauses VAD and closes mic
    //       stopVAD = null;
    //       updateStatus("Paused");
    //       autoListenBtn.classList.remove('recording');
    //     }
    //   });
   
      
    
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
                // recordButton.disabled = false;
                
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
        if (message.includes('Recording')) {
            statusElement.classList.add('recording');
        } else if (message.includes('Processing')) {
            statusElement.classList.add('processing');
        } else if (message.includes('Error')) {
            statusElement.classList.add('error');
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
                // recordButton.disabled = false;
                
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
    
    // Setup microphone access
    async function setupMicrophone() {
        if (microphoneSetup) return true;
        
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            microphoneSetup = true;
            return true;
        } catch (error) {
            updateStatus(`Error accessing microphone: ${error.message}`);
            console.error('Error accessing microphone:', error);
            return false;
        }
    }
    
    // Add a simple audio level visualization during recording
    // function setupVisualization(stream) {
    //     if (!audioContext) return;
        
    //     // Create a visualization container
    //     const visualizer = document.createElement('div');
    //     visualizer.className = 'audio-visualizer';
    //     // recordButton.appendChild(visualizer);
        
    //     // Create analyzer
    //     const analyser = audioContext.createAnalyser();
    //     const source = audioContext.createMediaStreamSource(stream);
    //     source.connect(analyser);
        
    //     analyser.fftSize = 32;
    //     const bufferLength = analyser.frequencyBinCount;
    //     const dataArray = new Uint8Array(bufferLength);
        
    //     // Create visualization bars
    //     for (let i = 0; i < bufferLength; i++) {
    //         const bar = document.createElement('div');
    //         bar.className = 'visualizer-bar';
    //         visualizer.appendChild(bar);
    //     }
        
    //     // Update visualization
    //     function updateVisualization() {
    //         if (!isRecording) {
    //             visualizer.remove();
    //             return;
    //         }
            
    //         analyser.getByteFrequencyData(dataArray);
    //         const bars = visualizer.querySelectorAll('.visualizer-bar');
            
    //         for (let i = 0; i < bars.length; i++) {
    //             const barHeight = dataArray[i] / 255 * 100;
    //             bars[i].style.height = barHeight + '%';
    //         }
            
    //         requestAnimationFrame(updateVisualization);
    //     }
        
    //     updateVisualization();
    // }
    
    // Modify startRecording to include visualization
    // async function startRecording() {
    //     try {
    //         console.log('startRecording: Starting recording process');
            
    //         // Initialize AudioContext as early as possible upon user interaction
    //         if (!audioContext) {
    //             audioContext = new (window.AudioContext || window.webkitAudioContext)();
    //             console.log('startRecording: AudioContext initialized with state:', audioContext.state);
    //         }
    
    //         if (audioContext && audioContext.state === 'suspended') {
    //             console.log('startRecording: AudioContext is suspended, attempting to resume...');
    //             try {
    //                 await audioContext.resume();
    //                 console.log('startRecording: AudioContext resumed. New state:', audioContext.state);
    //             } catch (resumeError) {
    //                 console.error('startRecording: Error resuming AudioContext:', resumeError);
    //             }
    //         }
    
    //         // Setup Microphone
    //         if (!await setupMicrophone()) {
    //             console.error('startRecording: Failed to set up microphone');
    //             return;
    //         }
    //         console.log('startRecording: Microphone setup complete');
            
    //         // Create a new conversation if none exists
    //         if (!currentConversationId) {
    //             console.log('startRecording: No active conversation, creating new one');
    //             await createNewConversation();
    //         }
            
    //         // Stop any currently playing audio
    //         if (currentAudioSource) {
    //             console.log('startRecording: Stopping previous audio before recording');
    //             currentAudioSource.stop();
    //             if (currentAudioSource.onended) {
    //                 currentAudioSource.onended = null; // Clear handler
    //             }
    //             currentAudioSource = null;
    //         }
            
    //         // Get User Media Stream with explicit constraints for audio quality
    //         console.log('startRecording: Requesting media stream');
    //         const stream = await navigator.mediaDevices.getUserMedia({
    //             audio: {
    //                 echoCancellation: true,
    //                 noiseSuppression: true,
    //                 autoGainControl: true,
    //                 sampleRate: 44100,
    //             }
    //         });
    //         console.log('startRecording: Media stream obtained successfully');
            
    //         // MediaRecorder Setup with MIME Type
    //         console.log('startRecording: Setting up MediaRecorder');
    //         const options = { mimeType: 'audio/webm; codecs=opus' };
    //         if (!MediaRecorder.isTypeSupported(options.mimeType)) {
    //             console.warn(`${options.mimeType} is not Supported, trying audio/webm`);
    //             options.mimeType = 'audio/webm'; 
    //             if (!MediaRecorder.isTypeSupported(options.mimeType)) {
    //                 console.warn(`${options.mimeType} is not Supported, browser default will be used.`);
    //                 delete options.mimeType; 
    //             }
    //         }
            
    //         mediaRecorder = new MediaRecorder(stream, options);
    //         recordedMimeType = mediaRecorder.mimeType; // Store the actual MIME type
    //         console.log('startRecording: MediaRecorder initialized with MIME type:', recordedMimeType);
    
    //         audioChunks = [];
            
    //         mediaRecorder.ondataavailable = (event) => {
    //             audioChunks.push(event.data);
    //             console.log(`startRecording: Audio chunk received, size: ${event.data.size} bytes`);
    //         };
            
    //         mediaRecorder.onstop = async () => {
    //             console.log(`startRecording: MediaRecorder stopped, processing ${audioChunks.length} chunks`);
    //             // Use the stored, correct MIME type here
    //             await processAudio(new Blob(audioChunks, { type: recordedMimeType || 'audio/webm' }));
    //         };
            
    //         mediaRecorder.start();
    //         console.log('startRecording: MediaRecorder started');
    //         isRecording = true;
    //         statusElement.textContent = 'Recording...';
    //         // recordButton.classList.add('recording');
    
    //         // Add visualization for audio feedback
    //         setupVisualization(mediaRecorder.stream);
    
    //     } catch (error) {
    //         console.error('startRecording: Error starting recording:', error);
    //         // Provide more specific error message to the user if possible
    //         if (error.name === 'NotAllowedError' || error.name === 'PermissionDeniedError') {
    //             statusElement.textContent = 'Microphone access denied.';
    //         } else if (error.name === 'NotFoundError') {
    //             statusElement.textContent = 'No microphone found.';
    //         } else {
    //             statusElement.textContent = 'Error starting recording.';
    //         }
    //     }
    // }
    
    // // Stop recording
    // function stopRecording() {
    //     if (isRecording && mediaRecorder) {
    //         mediaRecorder.stop();
    //         isRecording = false;
    //         statusElement.textContent = 'Processing...';
    //         // recordButton.classList.remove('recording');
            
    //         // Stop all audio tracks
    //         mediaRecorder.stream.getTracks().forEach(track => track.stop());
    //     }
    // }
    
    // Process audio
    async function processAudio(audioBlob) {
        try {
            console.log(`processAudio: Processing audio blob of size: ${audioBlob.size} bytes, type: ${audioBlob.type}`);
            statusElement.textContent = 'Processing...';
            
            const formData = new FormData();
            formData.append('audio', audioBlob);
            formData.append('voice_id', currentVoiceId);
            console.log(`processAudio: Using voice_id: ${currentVoiceId}`);
            
            console.log('processAudio: Sending audio to server...');
            const response = await fetch('/process_audio', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error(`Server returned status: ${response.status}`);
            }
            
            const data = await response.json();
            console.log('processAudio: Server response received', {
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
                    console.log(`processAudio: Audio response received, length: ${data.assistant_response_audio.length}`);
                    playAudioResponse(data.assistant_response_audio);
                } else {
                    console.warn('processAudio: No audio response received from server');
                }
                
                // Refresh conversation list to show the updated conversation
                await loadConversationHistory();
                
                statusElement.textContent = 'Ready';
            } else if (data.status === 'exit') {
                console.log('processAudio: Exit command detected');
                addMessage('assistant', data.assistant_response_text);
                statusElement.textContent = 'Conversation ended';
                
                // Refresh conversation list
                await loadConversationHistory();
            } else {
                throw new Error(data.message || 'Failed to process audio');
            }
        } catch (error) {
            console.error('processAudio: Error processing audio:', error);
            statusElement.textContent = `Error: ${error.message || 'Failed to process audio'}`;
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
            console.log('playAudioResponse: Called with audio length:', base64Audio ? base64Audio.length : 0);
            
            if (!base64Audio || base64Audio.length === 0) {
                console.error('playAudioResponse: Empty audio data received');
                return;
            }

            // AudioContext should already be initialized and running from the button click
            if (!audioContext) {
                console.error('playAudioResponse: AudioContext not initialized! This should not happen.');
                // Fallback to HTML5 audio immediately
                console.log('playAudioResponse: Using HTML5 Audio fallback');
                const audioElement = new Audio(`data:audio/mp3;base64,${base64Audio}`);
                audioElement.play().then(() => {
                    console.log('playAudioResponse: HTML5 Audio fallback successful');
                }).catch(htmlAudioError => {
                    console.error('playAudioResponse: HTML5 Audio fallback failed:', htmlAudioError);
                });
                return;
            }

            // Check AudioContext state (should be running already)
            if (audioContext.state !== 'running') {
                console.warn('playAudioResponse: AudioContext is not running, state:', audioContext.state);
                // Try HTML5 audio as fallback instead of trying to fix AudioContext
                console.log('playAudioResponse: Using HTML5 Audio fallback due to AudioContext state');
                const audioElement = new Audio(`data:audio/mp3;base64,${base64Audio}`);
                audioElement.play().then(() => {
                    console.log('playAudioResponse: HTML5 Audio fallback successful');
                }).catch(htmlAudioError => {
                    console.error('playAudioResponse: HTML5 Audio fallback failed:', htmlAudioError);
                });
                return;
            }
            
            // Stop any currently playing audio
            if (currentAudioSource) {
                console.log('playAudioResponse: Stopping existing audio source');
                currentAudioSource.stop();
                currentAudioSource.onended = null; // Clear previous handler
                currentAudioSource = null;
            }
            
            // Convert base64 to ArrayBuffer
            console.log('playAudioResponse: Converting base64 to ArrayBuffer');
            const binaryString = atob(base64Audio);
            const len = binaryString.length;
            const bytes = new Uint8Array(len);
            
            for (let i = 0; i < len; i++) {
                bytes[i] = binaryString.charCodeAt(i);
            }
            
            console.log(`playAudioResponse: Created bytes array of length ${bytes.length}`);
            
            // Decode audio data
            console.log('playAudioResponse: Decoding audio data...');
            let audioBuffer;
            try {
                audioBuffer = await audioContext.decodeAudioData(bytes.buffer);
                console.log(`playAudioResponse: Audio successfully decoded, duration: ${audioBuffer.duration}s, channels: ${audioBuffer.numberOfChannels}`);
            } catch (decodeError) {
                console.error('playAudioResponse: Failed to decode audio:', decodeError);
                // Try playing as a regular HTML5 audio element as fallback
                console.log('playAudioResponse: Attempting HTML5 Audio fallback');
                const audioElement = new Audio(`data:audio/mp3;base64,${base64Audio}`);
                audioElement.play().then(() => {
                    console.log('playAudioResponse: HTML5 Audio fallback successful');
                }).catch(htmlAudioError => {
                    console.error('playAudioResponse: HTML5 Audio fallback failed:', htmlAudioError);
                });
                return;
            }
            
            // Create and play audio source
            console.log('playAudioResponse: Creating audio source');
            const source = audioContext.createBufferSource();
            source.buffer = audioBuffer;
            source.connect(audioContext.destination);
            
            // Save reference to current source for potential interruption
            currentAudioSource = source;
            
            // Add event handlers
            source.onended = () => {
                console.log('playAudioResponse: Audio playback completed naturally');
                currentAudioSource = null;
            };
            
            // Actually play the audio
            console.log('playAudioResponse: Starting audio playback');
            source.start(0);
            console.log('playAudioResponse: Audio playback started');
            
        } catch (error) {
            console.error('playAudioResponse: Error playing audio:', error);
            // Try one more fallback approach with vanilla HTML audio
            try {
                console.log('playAudioResponse: Attempting final HTML5 Audio fallback');
                const audioBlob = new Blob(
                    [Uint8Array.from(atob(base64Audio), c => c.charCodeAt(0))], 
                    {type: 'audio/mp3'}
                );
                const audioUrl = URL.createObjectURL(audioBlob);
                const audio = new Audio(audioUrl);
                audio.play();
                console.log('playAudioResponse: Final HTML5 Audio fallback attempted');
            } catch (fallbackError) {
                console.error('playAudioResponse: All audio playback attempts failed:', fallbackError);
            }
        }
    }
    
    // Add touch support for mobile devices
    // recordButton.addEventListener('touchstart', async function(e) {
    //     e.preventDefault(); // Prevent default touch behavior
    //     startRecording();
    // });
    
    // recordButton.addEventListener('touchend', function(e) {
    //     e.preventDefault(); // Prevent default touch behavior
    //     stopRecording();
    // });
    
    // Add diagnostic function to test audio system (only runs on user interaction)
    async function testAudioSystem() {
        console.log('==== AUDIO SYSTEM DIAGNOSTIC ====');
        
        // Check if browser supports necessary audio APIs
        console.log('1. Browser capability check:');
        console.log(' - AudioContext supported:', typeof AudioContext !== 'undefined' || typeof webkitAudioContext !== 'undefined');
        console.log(' - MediaRecorder supported:', typeof MediaRecorder !== 'undefined');
        console.log(' - navigator.mediaDevices exists:', !!navigator.mediaDevices);
        console.log(' - getUserMedia supported:', !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia));
        console.log(' - Legacy getUserMedia supported:', !!(navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia));
        console.log(' - Current URL protocol:', window.location.protocol);
        console.log(' - Is HTTPS:', window.location.protocol === 'https:');
        console.log(' - Is localhost:', window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1');
        console.log(' - Supported MIME types for recording:');
        
        const testMimeTypes = [
            'audio/webm', 
            'audio/webm;codecs=opus', 
            'audio/mp4',
            'audio/wav',
            'audio/ogg'
        ];
        
        testMimeTypes.forEach(type => {
            if (typeof MediaRecorder !== 'undefined') {
                console.log(`   - ${type}: ${MediaRecorder.isTypeSupported(type)}`);
            }
        });
        
        // Test AudioContext creation (only after user interaction)
        console.log('2. AudioContext creation test:');
        try {
            const testContext = new (window.AudioContext || window.webkitAudioContext)();
            console.log(' - AudioContext created successfully');
            console.log(' - Sample rate:', testContext.sampleRate);
            console.log(' - Initial state:', testContext.state);
            
            // Test resume capability (this should work now since we're in a user gesture)
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
    updateStatus('Ready');
    
    // Audio system diagnostic will run when user clicks Auto Listen button
    
    // Listen for script loading errors
    window.addEventListener('error', (event) => {
        if (event.target && event.target.src && event.target.src.includes('vad-web')) {
            console.error('App initialization: Error loading VAD library:', event.error || event.message);
        }
    });

    // Log browser audio capabilities on startup (without creating AudioContext)
    console.log('App initialization: Browser audio capabilities:');
    console.log(' - AudioContext supported:', typeof AudioContext !== 'undefined' || typeof webkitAudioContext !== 'undefined');
    console.log(' - MediaRecorder supported:', typeof MediaRecorder !== 'undefined');
    console.log(' - navigator.mediaDevices exists:', !!navigator.mediaDevices);
    console.log(' - getUserMedia supported:', !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia));
    console.log(' - Legacy getUserMedia supported:', !!(navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia));
    console.log(' - Current URL protocol:', window.location.protocol);
    console.log(' - Is HTTPS:', window.location.protocol === 'https:');
    console.log(' - Is localhost:', window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1');

    // Update DOM structure to fix layout
    function updateLayoutStructure() {
        const mainContent = document.querySelector('.main-content');
        const main = document.querySelector('main');
        
        // Move patient details panel before main
        mainContent.insertBefore(patientDetailsPanel, main);
    }

    // Call this after initializing the patient details panel
    updateLayoutStructure();

    // Add this new non-blocking diagnostic function:
    async function testAudioSystemAsync() {
        // Use setTimeout to run this after the current event loop
        setTimeout(async () => {
            console.log('==== AUDIO SYSTEM DIAGNOSTIC (ASYNC) ====');
            
            // Check if browser supports necessary audio APIs
            console.log('1. Browser capability check:');
            console.log(' - AudioContext supported:', typeof AudioContext !== 'undefined' || typeof webkitAudioContext !== 'undefined');
            console.log(' - MediaRecorder supported:', typeof MediaRecorder !== 'undefined');
            console.log(' - navigator.mediaDevices exists:', !!navigator.mediaDevices);
            console.log(' - getUserMedia supported:', !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia));
            console.log(' - Legacy getUserMedia supported:', !!(navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia));
            console.log(' - Current URL protocol:', window.location.protocol);
            console.log(' - Is HTTPS:', window.location.protocol === 'https:');
            console.log(' - Is localhost:', window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1');
            console.log(' - Supported MIME types for recording:');
            
            const testMimeTypes = [
                'audio/webm', 
                'audio/webm;codecs=opus', 
                'audio/mp4',
                'audio/wav',
                'audio/ogg'
            ];
            
            testMimeTypes.forEach(type => {
                if (typeof MediaRecorder !== 'undefined') {
                    console.log(`   - ${type}: ${MediaRecorder.isTypeSupported(type)}`);
                }
            });
            
            // Check current AudioContext state (don't create a new one)
            console.log('2. AudioContext status check:');
            if (audioContext) {
                console.log(' - AudioContext exists:', !!audioContext);
                console.log(' - Sample rate:', audioContext.sampleRate);
                console.log(' - Current state:', audioContext.state);
            } else {
                console.log(' - AudioContext not yet initialized');
            }
            
            console.log('==== DIAGNOSTIC COMPLETE ====');
        }, 0);
    }

    // Initialize the application
    await loadConversationHistory();
    
    // Setup event listeners
    setupEventListeners();
});

function setupEventListeners() {
    // Custom patient form submission
    document.getElementById('customPatientForm').addEventListener('submit', handleCustomPatientSubmit);
    
    // New patient button (clears form)
    document.getElementById('newPatientBtn').addEventListener('click', createNewPatient);
    
    // Voice change handler
    document.getElementById('voiceSelect').addEventListener('change', handleVoiceChange);
    
    // Other existing event listeners...
    document.getElementById('refreshConversationsBtn').addEventListener('click', loadConversationHistory);
}

async function handleCustomPatientSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());
    
    // Basic validation
    if (!data.patient_name || !data.age || !data.gender) {
        alert('Please fill in required fields (Name, Age, Gender)');
        return;
    }
    
    try {
        updateStatus('Creating patient and generating condition...');
        
        const response = await fetch('/api/create-custom-patient', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.status === 'success') {
            // Patient created successfully
            currentConversationId = result.conversation_id;
            
            // Hide the form and show patient details
            document.getElementById('patientCreator').style.display = 'none';
            
            // Enable the auto listen button
            document.getElementById('autoListenBtn').disabled = false;
            
            // Load the new patient details
            await loadPatientDetails();
            
            // Clear conversation display and show welcome
            document.getElementById('conversation').innerHTML = `
                <div class="patient-created-message">
                    <h3>✅ Patient Created: ${result.patient_name}</h3>
                    <p><strong>Generated Condition:</strong> ${result.generated_disease}</p>
                    <p><em>This diagnosis is now hidden from you. Begin your consultation!</em></p>
                    <button onclick="startConsultation()">Start Consultation</button>
                </div>
            `;
            
            // Refresh conversation list to show the new conversation
            await loadConversationHistory();
            
            updateStatus('Patient ready - Start your consultation!');
        } else {
            throw new Error(result.message);
        }
        
    } catch (error) {
        console.error('Error creating custom patient:', error);
        updateStatus('Error creating patient');
        alert('Error creating custom patient: ' + error.message);
    }
}

function createNewPatient() {
    // Reset form
    document.getElementById('customPatientForm').reset();
    
    // Show the patient creation form
    document.getElementById('patientCreator').style.display = 'block';
    
    // Disable auto listen button until patient is created
    document.getElementById('autoListenBtn').disabled = true;
    
    // Clear conversation display
    document.getElementById('conversation').innerHTML = `
        <div class="welcome-message">
            <p>👩‍⚕️ Create a new patient to begin your diagnostic interview.</p>
        </div>
    `;
    
    // Clear patient details
    const patientDetailsPanel = document.getElementById('patientDetailsPanel');
    if (patientDetailsPanel) {
        patientDetailsPanel.innerHTML = '';
    }
    
    updateStatus('Fill out patient details above');
}

function startConsultation() {
    // Clear the conversation and prepare for the actual consultation
    document.getElementById('conversation').innerHTML = '';
    updateStatus('Ready - Ask your first question!');
}

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
        // Create patient details panel if it doesn't exist
        let patientDetailsPanel = document.getElementById('patientDetailsPanel');
        if (!patientDetailsPanel) {
            patientDetailsPanel = document.createElement('div');
            patientDetailsPanel.id = 'patientDetailsPanel';
            patientDetailsPanel.className = 'patient-details-panel';
            document.querySelector('.main-content').appendChild(patientDetailsPanel);
        }
        patientDetailsPanel.innerHTML = '<p class="error">Error loading patient details</p>';
    }
}

function displayPatientDetails(details) {
    // Create patient details panel if it doesn't exist
    let patientDetailsPanel = document.getElementById('patientDetailsPanel');
    if (!patientDetailsPanel) {
        patientDetailsPanel = document.createElement('div');
        patientDetailsPanel.id = 'patientDetailsPanel';
        patientDetailsPanel.className = 'patient-details-panel';
        document.querySelector('.main-content').appendChild(patientDetailsPanel);
    }
    
    patientDetailsPanel.innerHTML = '<h3>Current Patient</h3>';
    
    if (!details || Object.keys(details).length === 0) {
        patientDetailsPanel.innerHTML += '<p>No patient details available</p>';
        return;
    }
    
    const detailsList = document.createElement('ul');
    
    // Display patient fields (illness is hidden)
    const fieldsToDisplay = {
        'name': 'Name',
        'age': 'Age',
        'gender': 'Gender',
        'occupation': 'Occupation',
        'medical_history': 'Medical History',
        'area_of_medicine': 'Area of Medicine',
        'body_part': 'Body Part',
        'recent_exposure': 'Additional Info'
    };
    
    for (const [key, label] of Object.entries(fieldsToDisplay)) {
        if (details[key]) {
            const item = document.createElement('li');
            item.innerHTML = `<strong>${label}:</strong> ${details[key]}`;
            detailsList.appendChild(item);
        }
    }
    
    patientDetailsPanel.appendChild(detailsList);
    
    // Add reveal diagnosis button (for end of session)
    const revealBtn = document.createElement('button');
    revealBtn.textContent = 'Reveal Diagnosis';
    revealBtn.className = 'reveal-diagnosis-btn';
    revealBtn.onclick = revealDiagnosis;
    patientDetailsPanel.appendChild(revealBtn);
}

async function revealDiagnosis() {
    try {
        const response = await fetch('/api/reveal-diagnosis');
        const data = await response.json();
        
        if (data.status === 'success') {
            alert(`The actual diagnosis was: ${data.diagnosis}\n\nHow did you do?`);
        } else {
            throw new Error(data.message);
        }
    } catch (error) {
        console.error('Error revealing diagnosis:', error);
        alert('Error revealing diagnosis: ' + error.message);
    }
}

// Keep existing functions for:
// - processAudio()
// - addMessage()
// - handleVoiceChange()
// - loadConversationHistory()
// - etc. 