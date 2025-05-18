document.addEventListener('DOMContentLoaded', async () => {
    // DOM elements
    const recordButton = document.getElementById('recordButton');
    const statusElement = document.getElementById('status');
    const conversationElement = document.getElementById('conversation');
    const simulationSelect = document.getElementById('simulationSelect');
    const conversationListElement = document.getElementById('conversationList');
    const refreshConversationsBtn = document.getElementById('refreshConversationsBtn');
    const newConversationBtn = document.getElementById('newConversationBtn');
    
    // Audio recording variables
    let mediaRecorder = null;
    let audioChunks = [];
    let isRecording = false;
    let currentSimulation = null;
    let currentConversationId = null;
    let recordedMimeType = '';
    // Audio context for playback
    let audioContext;
    let currentAudioSource = null; // Track current audio source for interruption
    
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
    recordButton.addEventListener('mousedown', startRecording);
    recordButton.addEventListener('mouseup', stopRecording);
    recordButton.addEventListener('mouseleave', stopRecording);
    simulationSelect.addEventListener('change', handleSimulationChange);
    refreshConversationsBtn.addEventListener('click', loadConversationHistory);
    newConversationBtn.addEventListener('click', createNewConversation);
    
    // Request microphone access on first recording attempt rather than on page load
    let microphoneSetup = false;
    
    // Create a new empty conversation
    async function createNewConversation() {
        try {
            updateStatus('Creating new conversation...');
            
            // Clear simulation selection
            simulationSelect.value = '';
            currentSimulation = null;
            
            const response = await fetch('/api/conversations/new', {
                method: 'POST'
            });
            
            const data = await response.json();
            
            if (data.status === 'success') {
                currentConversationId = data.conversation_id;
                conversationElement.innerHTML = ''; // Clear conversation display
                
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
                
                // Clear the conversation display
                conversationElement.innerHTML = '';
                
                // Add messages to conversation display
                data.conversation.messages.forEach(message => {
                    addMessage(message.role, message.content);
                });
                
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
    async function startRecording() {
        try {
            // 1. Initialize and Resume AudioContext (if needed)
            // This should be done as early as possible upon user interaction.
            // 'startRecording' is triggered by mousedown/touchstart, which is a user interaction.
            initAudioContext(); // Make sure audioContext is created
    
            if (audioContext && audioContext.state === 'suspended') {
                console.log('startRecording: AudioContext is suspended, attempting to resume...');
                await audioContext.resume(); // Asynchronous, wait for it
                console.log('startRecording: AudioContext resumed. New state:', audioContext.state);
            }
    
            // 2. Setup Microphone (your existing logic)
            if (!await setupMicrophone()) { // setupMicrophone also good place to initAudioContext if not already
                return;
            }
            
            // 3. Create a new conversation if none exists (your existing logic)
            if (!currentConversationId) {
                await createNewConversation();
            }
            
            // 4. Stop any currently playing audio (your existing logic, with onended fix)
            if (currentAudioSource) {
                console.log('startRecording: Stopping previous audio source before recording.');
                currentAudioSource.stop();
                if (currentAudioSource.onended) { // Check if onended was set
                    currentAudioSource.onended = null; // Clear handler to prevent old logic firing
                }
                currentAudioSource = null;
            }
            
            // 5. Get User Media Stream (your existing logic)
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            
            // 6. MediaRecorder Setup with MIME Type (your existing good logic)
            const options = { mimeType: 'audio/webm; codecs=opus' };
            if (!MediaRecorder.isTypeSupported(options.mimeType)) {
                console.warn(`${options.mimeType} is not Supported, trying audio/webm`);
                options.mimeType = 'audio/webm'; 
                if (!MediaRecorder.isTypeSupported(options.mimeType)) {
                    console.warn(`${options.mimeType} is not Supported, browser default will be used.`);
                    delete options.mimeType; 
                }
            }
            
            mediaRecorder = new MediaRecorder(stream, options);
            recordedMimeType = mediaRecorder.mimeType; // Store the actual MIME type
            console.log('Recording with MIME type:', recordedMimeType);
    
            audioChunks = [];
            
            mediaRecorder.ondataavailable = (event) => {
                audioChunks.push(event.data);
            };
            
            mediaRecorder.onstop = async () => {
                // Use the stored, correct MIME type here
                await processAudio(new Blob(audioChunks, { type: recordedMimeType || 'audio/webm' }));
            };
            
            mediaRecorder.start();
            isRecording = true;
            statusElement.textContent = 'Recording...';
            recordButton.classList.add('recording');
    
        } catch (error) {
            console.error('Error starting recording:', error);
            // Provide more specific error message to the user if possible
            if (error.name === 'NotAllowedError' || error.name === 'PermissionDeniedError') {
                statusElement.textContent = 'Microphone access denied.';
            } else if (error.name === 'NotFoundError') {
                statusElement.textContent = 'No microphone found.';
            } else {
                statusElement.textContent = 'Error starting recording.';
            }
        }
    } 
    // // Start recording
    // async function startRecording() {
    //     try {
    //         // Initialize microphone if not already done
    //         if (!await setupMicrophone()) {
    //             return;
    //         }
            
    //         // Create a new conversation if none exists
    //         if (!currentConversationId) {
    //             await createNewConversation();
    //         }
            
    //         // Stop any currently playing audio
    //         if (currentAudioSource) {
    //             currentAudioSource.stop();
    //             currentAudioSource = null;
    //         }
            
    //         const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    //    // Try to get a preferred MIME type, fallback if not supported
    //         const options = { mimeType: 'audio/webm; codecs=opus' }; // Prefer WebM Opus
    //         if (!MediaRecorder.isTypeSupported(options.mimeType)) {
    //             console.warn(`${options.mimeType} is not Supported, trying audio/webm`);
    //             options.mimeType = 'audio/webm'; // Fallback to generic WebM
    //             if (!MediaRecorder.isTypeSupported(options.mimeType)) {
    //                 console.warn(`${options.mimeType} is not Supported, browser default will be used.`);
    //                 delete options.mimeType; // Let browser decide
    //             }
    //         }
    //         mediaRecorder = new MediaRecorder(stream, options);
            
    //         recordedMimeType=mediaRecorder.mimeType;

    //         audioChunks = [];
            
    //         mediaRecorder.ondataavailable = (event) => {
    //             audioChunks.push(event.data);
    //         };
            
    //         mediaRecorder.onstop = async () => {
    //             await processAudio(new Blob(audioChunks, { type: 'audio/webm' }));
    //         };
            
    //         mediaRecorder.start();
    //         isRecording = true;
    //         statusElement.textContent = 'Recording...';
    //         recordButton.classList.add('recording');
    //     } catch (error) {
    //         console.error('Error starting recording:', error);
    //         statusElement.textContent = 'Error starting recording';
    //     }
    // }
    
    // Stop recording
    function stopRecording() {
        if (isRecording && mediaRecorder) {
            mediaRecorder.stop();
            isRecording = false;
            statusElement.textContent = 'Processing...';
            recordButton.classList.remove('recording');
            
            // Stop all audio tracks
            mediaRecorder.stream.getTracks().forEach(track => track.stop());
        }
    }
    
    // Process audio
    async function processAudio(audioBlob) {
        try {
            const formData = new FormData();
            formData.append('audio', audioBlob);
            
            const response = await fetch('/process_audio', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (data.status === 'success') {
                // Add user message
                addMessage('user', data.user_transcription);
                
                // Add assistant message
                addMessage('assistant', data.assistant_response_text);
                
                // Play audio response if available
                if (data.assistant_response_audio) {
                    playAudioResponse(data.assistant_response_audio);
                }
                
                // Refresh conversation list to show the updated conversation
                await loadConversationHistory();
                
                statusElement.textContent = 'Ready';
            } else if (data.status === 'exit') {
                addMessage('assistant', data.assistant_response_text);
                statusElement.textContent = 'Conversation ended';
                recordButton.disabled = true;
                
                // Refresh conversation list
                await loadConversationHistory();
            } else {
                throw new Error(data.message || 'Failed to process audio');
            }
        } catch (error) {
            console.error('Error processing audio:', error);
            statusElement.textContent = 'Error processing audio';
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
            initAudioContext();


            if (audioContext && audioContext.state === 'suspended') {
                console.log('playAudioResponse: AudioContext is suspended, attempting to resume...');
                await audioContext.resume();
                console.log('playAudioResponse: AudioContext resumed. New state:', audioContext.state);
            }
            
            // Stop any currently playing audio
            if (currentAudioSource) {
                currentAudioSource.stop();
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
            const audioBuffer = await audioContext.decodeAudioData(bytes.buffer);
            
            // Create and play audio source
            const source = audioContext.createBufferSource();
            source.buffer = audioBuffer;
            source.connect(audioContext.destination);
            
            // Save reference to current source for potential interruption
            currentAudioSource = source;
            
            // Play audio
            source.start(0);
            
            // Clear reference when playback completes
            source.onended = () => {
                currentAudioSource = null;
            };
        } catch (error) {
            console.error('Error playing audio:', error);
        }
    }
    
    // Add touch support for mobile devices
    recordButton.addEventListener('touchstart', async function(e) {
        e.preventDefault(); // Prevent default touch behavior
        startRecording();
    });
    
    recordButton.addEventListener('touchend', function(e) {
        e.preventDefault(); // Prevent default touch behavior
        stopRecording();
    });
    
    // Initialize the app
    updateStatus('Ready');
}); 