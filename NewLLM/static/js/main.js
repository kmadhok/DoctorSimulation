document.addEventListener('DOMContentLoaded', function() {
    // DOM elements
    const recordButton = document.getElementById('recordButton');
    const statusElement = document.getElementById('status');
    const conversationElement = document.getElementById('conversation');
    
    // Audio recording variables
    let mediaRecorder;
    let audioChunks = [];
    let isRecording = false;
    
    // Audio context for playback
    let audioContext;
    let currentAudioSource = null; // Track current audio source for interruption
    
    // Initialize audio context on user interaction
    function initAudioContext() {
        if (!audioContext) {
            audioContext = new (window.AudioContext || window.webkitAudioContext)();
        }
    }
    
    // Request microphone access
    async function setupMicrophone() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            
            // Create media recorder
            mediaRecorder = new MediaRecorder(stream);
            
            // Handle data available event
            mediaRecorder.addEventListener('dataavailable', event => {
                if (event.data.size > 0) {
                    audioChunks.push(event.data);
                }
            });
            
            // Handle recording stop event
            mediaRecorder.addEventListener('stop', () => {
                processAudio();
            });
            
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
    function startRecording() {
        if (!mediaRecorder) {
            updateStatus('Microphone not available');
            return;
        }
        
        // Initialize audio chunks
        audioChunks = [];
        
        // Update UI
        updateStatus('Listening...');
        recordButton.classList.add('recording');
        isRecording = true;
        
        // Start recording
        mediaRecorder.start();
    }
    
    // Stop recording
    function stopRecording() {
        if (!isRecording) return;
        
        // Update UI
        updateStatus('Processing...');
        recordButton.classList.remove('recording');
        isRecording = false;
        
        // Stop recording
        mediaRecorder.stop();
    }
    
    // Process recorded audio
    async function processAudio() {
        if (audioChunks.length === 0) {
            updateStatus('No audio recorded');
            return;
        }
        
        try {
            // Create audio blob
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            
            // Create form data
            const formData = new FormData();
            formData.append('audio', audioBlob, 'recording.wav');
            
            // Send to server
            updateStatus('Sending to server...');
            
            const response = await fetch('/process_audio', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Handle the response
            if (data.status === 'error') {
                throw new Error(data.message || 'Unknown error');
            } else if (data.status === 'exit') {
                // Handle exit command
                addMessageToConversation('user', data.user_transcription);
                addMessageToConversation('assistant', data.assistant_response_text);
                updateStatus('Conversation ended');
            } else {
                // Add messages to conversation
                addMessageToConversation('user', data.user_transcription);
                addMessageToConversation('assistant', data.assistant_response_text);
                
                // Play audio response if available
                if (data.assistant_response_audio && data.assistant_response_audio.length > 0) {
                    updateStatus('Speaking...');
                    try {
                        await playAudio(data.assistant_response_audio);
                    } catch (error) {
                        console.error('Error playing audio:', error);
                        updateStatus('Error playing audio, but response received');
                    }
                } else {
                    console.log('No audio response received from server');
                }
                
                updateStatus('Ready');
            }
        } catch (error) {
            updateStatus(`Error: ${error.message}`);
            console.error('Error processing audio:', error);
        }
    }
    
    // Add message to conversation
    function addMessageToConversation(role, message) {
        const messageElement = document.createElement('div');
        messageElement.className = `message ${role}`;
        
        const textElement = document.createElement('p');
        textElement.textContent = message;
        
        messageElement.appendChild(textElement);
        conversationElement.appendChild(messageElement);
        
        // Scroll to bottom
        conversationElement.scrollTop = conversationElement.scrollHeight;
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
    
    // Set up button event listeners
    recordButton.addEventListener('mousedown', async function() {
        // Stop any currently playing audio
        if (currentAudioSource) {
            currentAudioSource.stop();
            currentAudioSource = null;
        }
        
        // Initialize audio context on first interaction
        initAudioContext();
        
        // Ensure microphone is set up
        if (!mediaRecorder) {
            const setupSuccess = await setupMicrophone();
            if (!setupSuccess) return;
        }
        
        startRecording();
    });
    
    recordButton.addEventListener('mouseup', function() {
        stopRecording();
    });
    
    recordButton.addEventListener('mouseleave', function() {
        if (isRecording) {
            stopRecording();
        }
    });
    
    // Add touch support for mobile devices
    recordButton.addEventListener('touchstart', async function(e) {
        e.preventDefault(); // Prevent default touch behavior
        
        // Initialize audio context on first interaction
        initAudioContext();
        
        // Ensure microphone is set up
        if (!mediaRecorder) {
            const setupSuccess = await setupMicrophone();
            if (!setupSuccess) return;
        }
        
        startRecording();
    });
    
    recordButton.addEventListener('touchend', function(e) {
        e.preventDefault(); // Prevent default touch behavior
        stopRecording();
    });
    
    // Initialize the app
    updateStatus('Ready');
}); 