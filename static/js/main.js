document.addEventListener('DOMContentLoaded', async () => {

    let stopVAD = null;        // will hold the cleanup fn

    async function initAutoVAD() {
    // Wait until the library has loaded
    while (!window.MicVAD) await new Promise(r => setTimeout(r, 50));

    const vad = await MicVAD.new({
        positiveSpeechThreshold : 0.8,  // raise if background noise triggers
        negativeSpeechThreshold : 0.5,
        preSpeechPadFrames      : 8,    // ms before first speech frame
        minSpeechFrames         : 3,    // 3 × 30 ms  = 90 ms
        redemptionFrames        : 10,   // hysteresis for trailing silence

        onSpeechEnd: async (float32Audio) => {
        updateStatus("Processing…");
        const wavBlob = float32ToWav(float32Audio);
        await processAudio(wavBlob);  // <- your existing pipeline
        updateStatus("Ready");
        },
    });

    await vad.start();       // Mic opened, worklet running
    return () => vad.pause();  // cleanup fn to stop VAD + mic
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
    
    // New DOM element for patient details - reposition it within main content
    const patientDetailsPanel = document.createElement('div');
    patientDetailsPanel.id = 'patientDetailsPanel';
    patientDetailsPanel.className = 'patient-details-panel';

    // Create this after DOM is fully loaded
    const mainContent = document.querySelector('.main-content');
    mainContent.appendChild(patientDetailsPanel);
    
    // Audio recording variables
    let mediaRecorder = null;
    let audioChunks = [];
    let isRecording = false;
    let currentSimulation = null;
    let currentVoiceId = 'Fritz-PlayAI'; // Default voice
    let currentConversationId = null;
    let recordedMimeType = '';
    // Audio context for playback
    let audioContext;
    let currentAudioSource = null; // Track current audio source for interruption

    // // Dynamic import works in every browser that supports modules
    // import("https://cdn.jsdelivr.net/npm/@ricky0123/vad-web@0.0.22/dist/bundle.min.js")
    // .then((module) => {
    //     window.MicVAD = module.MicVAD;   // MicVAD is exported at top level
    // })
    
    // .catch(console.error);
    import("https://cdn.jsdelivr.net/npm/@ricky0123/vad-web@0.0.22/dist/index.js")
    .then(({ MicVAD }) => (window.MicVAD = MicVAD))
    .catch(console.error);
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
    // recordButton.addEventListener('mousedown', startRecording);
    // recordButton.addEventListener('mouseup', stopRecording);
    // recordButton.addEventListener('mouseleave', stopRecording);
    simulationSelect.addEventListener('change', handleSimulationChange);
    voiceSelect.addEventListener('change', handleVoiceChange);
    refreshConversationsBtn.addEventListener('click', loadConversationHistory);
    newConversationBtn.addEventListener('click', createNewConversation);
    autoListenBtn.addEventListener('click', async () => {
        if (!stopVAD) {
          updateStatus("Listening…");
          autoListenBtn.classList.add('recording');
          stopVAD = await initAutoVAD();    // starts everything
        } else {
          stopVAD();                        // pauses VAD and closes mic
          stopVAD = null;
          updateStatus("Paused");
          autoListenBtn.classList.remove('recording');
        }
      });
      
    
    // Request microphone access on first recording attempt rather than on page load
    let microphoneSetup = false;
    
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
            // recordButton.disabled = true;
            
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
                // recordButton.disabled = false;
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
            // recordButton.disabled = true;
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
                // recordButton.disabled = true;
                
                // Refresh conversation list
                await loadConversationHistory();
            } else {
                throw new Error(data.message || 'Failed to process audio');
            }
        } catch (error) {
            console.error('processAudio: Error processing audio:', error);
            statusElement.textContent = `Error: ${error.message || 'Failed to process audio'}`;
            
            // // Enable the record button again so users can retry
            // recordButton.disabled = false;
            // recordButton.classList.remove('recording');
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

            // Initialize audio context if not already done
            if (!audioContext) {
                audioContext = new (window.AudioContext || window.webkitAudioContext)();
                console.log('playAudioResponse: AudioContext initialized with state:', audioContext.state);
            }

            // Resume AudioContext - this is critical for browsers that suspend by default
            if (audioContext.state === 'suspended') {
                console.log('playAudioResponse: AudioContext is suspended, attempting to resume...');
                await audioContext.resume();
                console.log('playAudioResponse: AudioContext resume attempt completed. New state:', audioContext.state);
            }
            
            if (audioContext.state !== 'running') {
                console.warn('playAudioResponse: AudioContext is NOT running after attempt to resume. State:', audioContext.state);
                // Try to create a fresh audio context as a fallback
                console.log('playAudioResponse: Attempting to create new AudioContext as fallback');
                audioContext = new (window.AudioContext || window.webkitAudioContext)();
                await audioContext.resume();
                console.log('playAudioResponse: New AudioContext state:', audioContext.state);
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
    
    // Add diagnostic function to test audio system
    async function testAudioSystem() {
        console.log('==== AUDIO SYSTEM DIAGNOSTIC ====');
        
        // Check if browser supports necessary audio APIs
        console.log('1. Browser capability check:');
        console.log(' - AudioContext supported:', typeof AudioContext !== 'undefined' || typeof webkitAudioContext !== 'undefined');
        console.log(' - MediaRecorder supported:', typeof MediaRecorder !== 'undefined');
        console.log(' - getUserMedia supported:', navigator.mediaDevices && typeof navigator.mediaDevices.getUserMedia !== 'undefined');
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
        
        // Test audio decoding with a minimal audio
        console.log('3. Audio decoding capability test:');
        try {
            // Create a minimal silent MP3 (1 frame)
            const silentMp3Base64 = 'SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU4Ljc2LjEwMAAAAAAAAAAAAAAA//tAwAAAAAAAAAAAAAAAAAAAAAAAWGluZwAAAA8AAAACAAABGADbW1tbW1tbW1tbW1tbW1tbW1tbW1tbW1tbW1tbW1tb29vb29vb29vb29vb29vb29vb29vb29vb29vb29v///////////////////////////////////////////8AAAAATGF2YzU4LjEzAAAAAAAAAAAAAAAAJAAAAAAAAAAAARiN6AYcAAAAAAAAAAAAAAAAAAAAAP/7kGQAAANkAEj0AAACPQCJHoAAEYwYSPmMADRBghk/MYAGvtm2YG7aBtvAAGxu3dMzdu8m5t7d1TM3b7Jx9suKKOOTkyDjNxcUcckUcbOTIONnJxRxw5I4uKOEIQhDjjk4o44QhMg4zYcIQhEIQhDanHJ28IQhD6nHHHCEIREIQhCanH1OPqcfU4444QhCEIQhCEIQhCEIQhCEIhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh/+5JkEI/0iGdH+ewANHkNCP89gAafCggQEDDCgIB4WIGAEMArhgZgwZkI2YFCBAAGDBRw4MIHAgAfW8b9f/1eN+v9fWtlMy8b8Hliz//Liz//Liz//4uNS4uNS4uP+NS4uP+NS5//8uP//+X//4AAAAMw13m22BTMzAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA';
            
            const binaryString = atob(silentMp3Base64);
            const len = binaryString.length;
            const bytes = new Uint8Array(len);
            for (let i = 0; i < len; i++) {
                bytes[i] = binaryString.charCodeAt(i);
            }
            
            const testContext = new (window.AudioContext || window.webkitAudioContext)();
            const result = await testContext.decodeAudioData(bytes.buffer);
            console.log(' - Audio decoding successful');
            console.log(' - Decoded audio duration:', result.duration);
            console.log(' - Decoded audio channels:', result.numberOfChannels);
            
            // Test playback
            console.log(' - Testing audio playback...');
            const source = testContext.createBufferSource();
            source.buffer = result;
            source.connect(testContext.destination);
            source.onended = () => console.log(' - Test playback completed');
            source.start(0);
            
        } catch (decodeError) {
            console.error(' - Audio decoding failed:', decodeError);
        }
        
        console.log('==== DIAGNOSTIC COMPLETE ====');
    }

    // Initialize the app
    updateStatus('Ready');
    
    // Run audio system diagnostic
    testAudioSystem().catch(err => console.error('Audio diagnostic error:', err));

    // Add this after creating recordButton constant
    // function styleAutoListenBtn() {
    //     autoListenBtn.innerHTML = `
    //         <div class="controls">
    //         <button id="autoListenBtn" class="record-button">
    //             <span class="record-icon"></span>
    //             Auto Listen
    //         </button>
    //         </div>
    //     `
    //     ;
    // }
    // styleAutoListenBtn();

    // Update DOM structure to fix layout
    function updateLayoutStructure() {
        const mainContent = document.querySelector('.main-content');
        const main = document.querySelector('main');
        
        // Move patient details panel before main
        mainContent.insertBefore(patientDetailsPanel, main);
    }

    // Call this after initializing the patient details panel
    updateLayoutStructure();
}); 