document.addEventListener('DOMContentLoaded', async () => {
    // DOM elements
    const recordButton = document.getElementById('recordButton');
    const statusElement = document.getElementById('status');
    const conversationElement = document.getElementById('conversation');
    const simulationSelect = document.getElementById('simulationSelect');
    const conversationList = document.getElementById('conversationList');
    
    // Audio recording variables
    let mediaRecorder = null;
    let audioChunks = [];
    let isRecording = false;
    let currentSimulation = null;
    let currentConversationId = null;
    
    // Audio context for playback
    let audioContext;
    let currentAudioSource = null; // Track current audio source for interruption
    
    // Initialize audio context on user interaction
    function initAudioContext() {
        if (!audioContext) {
            audioContext = new (window.AudioContext || window.webkitAudioContext)();
        }
    }
    
    // Initialize the application
    async function initializeApp() {
        try {
            // Load available simulations
            const response = await fetch('/api/patient-simulations');
            const data = await response.json();
            
            if (data.status === 'success') {
                simulationSelect.innerHTML = data.simulations
                    .map(sim => `<option value="${sim}">${sim}</option>`)
                    .join('');
                
                if (data.current_simulation) {
                    simulationSelect.value = data.current_simulation;
                    currentSimulation = data.current_simulation;
                    recordButton.disabled = false;
                }
            }
            
            // Load conversations
            await loadConversations();
        } catch (error) {
            console.error('Error initializing app:', error);
            statusElement.textContent = 'Error initializing app';
        }
    }
    
    // Load conversations from the server
    async function loadConversations() {
        try {
            const response = await fetch('/api/conversations');
            const data = await response.json();
            
            if (data.status === 'success') {
                conversationList.innerHTML = data.conversations
                    .map(conv => `
                        <div class="conversation-item" data-id="${conv.id}">
                            <div class="simulation">${conv.patient_simulation || 'No simulation'}</div>
                            <div class="timestamp">${new Date(conv.created_at).toLocaleString()}</div>
                        </div>
                    `)
                    .join('');
                
                // Add click handlers to conversation items
                document.querySelectorAll('.conversation-item').forEach(item => {
                    item.addEventListener('click', () => displayConversation(item.dataset.id, data.conversations));
                });
            }
        } catch (error) {
            console.error('Error loading conversations:', error);
        }
    }
    
    // Display a specific conversation
    function displayConversation(conversationId, conversations) {
        const conversation = conversations.find(c => c.id === parseInt(conversationId));
        if (!conversation) return;
        
        // Update active state
        document.querySelectorAll('.conversation-item').forEach(item => {
            item.classList.toggle('active', item.dataset.id === conversationId);
        });
        
        // Display messages
        conversationElement.innerHTML = conversation.messages
            .map(msg => `
                <div class="message ${msg.role}">
                    <div class="content">${msg.content}</div>
                    <div class="timestamp">${new Date(msg.timestamp).toLocaleString()}</div>
                </div>
            `)
            .join('');
        
        // Scroll to bottom
        conversationElement.scrollTop = conversationElement.scrollHeight;
        
        // Update current conversation ID
        currentConversationId = conversationId;
    }
    
    // Handle simulation selection
    simulationSelect.addEventListener('change', async (e) => {
        try {
            const response = await fetch('/api/select-simulation', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    simulation_file: e.target.value
                })
            });
            
            const data = await response.json();
            if (data.status === 'success') {
                statusElement.textContent = `Selected: ${data.current_simulation}`;
                // Clear conversation display
                conversationElement.innerHTML = '';
                // Reload conversations to get the new one
                await loadConversations();
            }
        } catch (error) {
            console.error('Error selecting simulation:', error);
            statusElement.textContent = 'Error selecting simulation';
        }
    });
    
    // Handle recording
    recordButton.addEventListener('mousedown', startRecording);
    recordButton.addEventListener('mouseup', stopRecording);
    recordButton.addEventListener('mouseleave', stopRecording);
    
    // Touch events for mobile
    recordButton.addEventListener('touchstart', (e) => {
        e.preventDefault();
        startRecording();
    });
    
    recordButton.addEventListener('touchend', (e) => {
        e.preventDefault();
        stopRecording();
    });
    
    // Request microphone access
    async function setupMicrophone() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            
            // Create media recorder
            mediaRecorder = new MediaRecorder(stream);
            
            // Handle data available event
            mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    audioChunks.push(event.data);
                }
            };
            
            // Handle recording stop event
            mediaRecorder.onstop = async () => {
                await processAudio(new Blob(audioChunks, { type: 'audio/wav' }));
            };
            
            return true;
        } catch (error) {
            updateStatus(`Error accessing microphone: ${error.message}`);
            console.error('Error accessing microphone:', error);
            return false;
        }
    }
    
    // Update status message
    function updateStatus(message) {
        statusElement.textContent = message;
    }
    
    // Start recording
    async function startRecording() {
        if (!currentSimulation) {
            statusElement.textContent = 'Please select a simulation first';
            return;
        }
        
        try {
            // Stop any currently playing audio
            if (currentAudioSource) {
                currentAudioSource.stop();
                currentAudioSource = null;
            }
            
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            audioChunks = [];
            
            mediaRecorder.ondataavailable = (event) => {
                audioChunks.push(event.data);
            };
            
            mediaRecorder.onstop = async () => {
                await processAudio(new Blob(audioChunks, { type: 'audio/wav' }));
            };
            
            mediaRecorder.start();
            isRecording = true;
            statusElement.textContent = 'Recording...';
            recordButton.classList.add('recording');
        } catch (error) {
            console.error('Error starting recording:', error);
            statusElement.textContent = 'Error starting recording';
        }
    }
    
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
                
                statusElement.textContent = 'Ready';
                
                // Reload conversations to get the updated one
                await loadConversations();
            } else if (data.status === 'exit') {
                addMessage('assistant', data.assistant_response_text);
                statusElement.textContent = 'Conversation ended';
                recordButton.disabled = true;
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
        messageDiv.innerHTML = `
            <div class="content">${content}</div>
            <div class="timestamp">${new Date().toLocaleString()}</div>
        `;
        conversationElement.appendChild(messageDiv);
        conversationElement.scrollTop = conversationElement.scrollHeight;
    }
    
    // Play audio response
    async function playAudioResponse(base64Audio) {
        try {
            initAudioContext();
            
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
            
            // Create source node
            const source = audioContext.createBufferSource();
            source.buffer = audioBuffer;
            source.connect(audioContext.destination);
            
            // Store current source for potential interruption
            currentAudioSource = source;
            
            // Play audio
            source.start(0);
            
            // Return a promise that resolves when audio finishes playing
            return new Promise(resolve => {
                source.onended = () => {
                    currentAudioSource = null;
                    resolve();
                };
            });
        } catch (error) {
            console.error('Error playing audio:', error);
            throw error;
        }
    }
    
    // Play audio from base64 string
    async function playAudio(base64Audio) {
        if (!base64Audio || base64Audio.length === 0) {
            console.error('Empty base64 audio data');
            return Promise.resolve(); // Resolve immediately for empty audio
        }
        
        try {
            initAudioContext();
            
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
            
            // Create source node
            const source = audioContext.createBufferSource();
            source.buffer = audioBuffer;
            source.connect(audioContext.destination);
            
            // Store current source for potential interruption
            currentAudioSource = source;
            
            // Play audio
            source.start(0);
            
            // Return a promise that resolves when audio finishes playing
            return new Promise(resolve => {
                source.onended = () => {
                    currentAudioSource = null;
                    resolve();
                };
            });
        } catch (error) {
            console.error('Error playing audio:', error);
            throw error;
        }
    }
    
    // Initialize the app
    initializeApp();
}); 