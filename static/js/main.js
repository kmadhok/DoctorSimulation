document.addEventListener('DOMContentLoaded', async () => {
    // DOM elements
    const recordButton = document.getElementById('recordButton');
    const statusElement = document.getElementById('status');
    const conversationElement = document.getElementById('conversation');
    const simulationSelect = document.getElementById('simulationSelect');
    
    // Audio recording variables
    let mediaRecorder = null;
    let audioChunks = [];
    let isRecording = false;
    let currentSimulation = null;
    
    // Audio context for playback
    let audioContext;
    let currentAudioSource = null; // Track current audio source for interruption
    
    // Initialize audio context on user interaction
    function initAudioContext() {
        if (!audioContext) {
            audioContext = new (window.AudioContext || window.webkitAudioContext)();
        }
    }
    
    // Load available simulations
    await loadSimulations();
    
    // Set up event listeners
    recordButton.addEventListener('mousedown', startRecording);
    recordButton.addEventListener('mouseup', stopRecording);
    recordButton.addEventListener('mouseleave', stopRecording);
    simulationSelect.addEventListener('change', handleSimulationChange);
    
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
    
    // Load available simulations
    async function loadSimulations() {
        try {
            const response = await fetch('/api/patient-simulations');
            const data = await response.json();
            
            if (data.status === 'success') {
                // Clear loading option
                simulationSelect.innerHTML = '';
                
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
                    recordButton.disabled = false;
                }
            } else {
                throw new Error(data.message || 'Failed to load simulations');
            }
        } catch (error) {
            console.error('Error loading simulations:', error);
            statusElement.textContent = 'Error loading simulations';
        }
    }
    
    // Handle simulation change
    async function handleSimulationChange(event) {
        const selectedSimulation = event.target.value;
        if (!selectedSimulation) return;
        
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
                statusElement.textContent = 'Ready';
                recordButton.disabled = false;
                conversationElement.innerHTML = ''; // Clear conversation
            } else {
                throw new Error(data.message || 'Failed to select simulation');
            }
        } catch (error) {
            console.error('Error selecting simulation:', error);
            statusElement.textContent = 'Error selecting simulation';
            recordButton.disabled = true;
        }
    }
    
    // Start recording
    async function startRecording() {
        if (!currentSimulation) {
            statusElement.textContent = 'Please select a simulation first';
            return;
        }
        
        try {
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
        messageDiv.textContent = content;
        conversationElement.appendChild(messageDiv);
        conversationElement.scrollTop = conversationElement.scrollHeight;
    }
    
    // Play audio response
    function playAudioResponse(base64Audio) {
        const audio = new Audio(`data:audio/wav;base64,${base64Audio}`);
        audio.play();
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