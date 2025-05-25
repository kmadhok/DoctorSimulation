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
    const sensitivitySlider = document.getElementById('sensitivitySlider');
    const sensitivityValue = document.getElementById('sensitivityValue');
    
    // Add debug overlay for monitoring voice levels
    const debugOverlay = document.createElement('div');
    debugOverlay.id = 'debugOverlay';
    debugOverlay.style.position = 'fixed';
    debugOverlay.style.bottom = '10px';
    debugOverlay.style.right = '10px';
    debugOverlay.style.backgroundColor = 'rgba(0,0,0,0.7)';
    debugOverlay.style.color = 'white';
    debugOverlay.style.padding = '10px';
    debugOverlay.style.borderRadius = '5px';
    debugOverlay.style.zIndex = '9999';
    debugOverlay.style.fontSize = '12px';
    debugOverlay.style.fontFamily = 'monospace';
    debugOverlay.style.maxWidth = '300px';
    debugOverlay.style.maxHeight = '200px';
    debugOverlay.style.overflow = 'auto';
    document.body.appendChild(debugOverlay);
    
    // Debug logging function
    function debugLog(message) {
        console.log(`[DEBUG] ${message}`);
        const timestamp = new Date().toLocaleTimeString();
        const logEntry = document.createElement('div');
        logEntry.textContent = `${timestamp}: ${message}`;
        debugOverlay.appendChild(logEntry);
        
        // Keep only last 20 messages
        while (debugOverlay.childNodes.length > 20) {
            debugOverlay.removeChild(debugOverlay.firstChild);
        }
        
        // Auto-scroll to bottom
        debugOverlay.scrollTop = debugOverlay.scrollHeight;
    }
    
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
    
    // Voice activity detection variables
    let vadActive = false;
    let voiceDetected = false;
    let silenceTimer = null;
    let vadAnalyser = null;
    let vadDataArray = null;
    let vadAnimationFrame = null;
    let vadStream = null;
    let VAD_THRESHOLD = parseInt(sensitivitySlider.value); // Voice detection threshold - make this configurable
    const SILENCE_TIMEOUT = 1500; // Time of silence before stopping (ms)
    let lastAudioLevel = 0;
    
    // Set up sensitivity slider handler
    sensitivitySlider.addEventListener('input', function() {
        VAD_THRESHOLD = parseInt(this.value);
        sensitivityValue.textContent = VAD_THRESHOLD;
        debugLog(`Voice detection threshold changed to ${VAD_THRESHOLD}`);
    });
    
    // Add a debug toggle button
    const debugToggle = document.createElement('button');
    debugToggle.textContent = 'Toggle Debug';
    debugToggle.style.position = 'fixed';
    debugToggle.style.bottom = '10px';
    debugToggle.style.left = '10px';
    debugToggle.style.zIndex = '9999';
    debugToggle.addEventListener('click', () => {
        if (debugOverlay.style.display === 'none') {
            debugOverlay.style.display = 'block';
            debugLog('Debug overlay enabled');
        } else {
            debugOverlay.style.display = 'none';
        }
    });
    document.body.appendChild(debugToggle);
    
    // Initialize audio context on user interaction
    function initAudioContext() {
        if (!audioContext) {
            audioContext = new (window.AudioContext || window.webkitAudioContext)();
            debugLog(`AudioContext initialized. Initial state: ${audioContext.state}`);
        }
    }
    
    // Load available simulations
    await loadSimulations();
    
    // Load conversation history
    await loadConversationHistory();
    
    // Replace mouse events with toggle functionality for the record button
    recordButton.removeEventListener('mousedown', startRecording);
    recordButton.removeEventListener('mouseup', stopRecording);
    recordButton.removeEventListener('mouseleave', stopRecording);
    recordButton.addEventListener('click', toggleVoiceActivityDetection);
    
    simulationSelect.addEventListener('change', handleSimulationChange);
    voiceSelect.addEventListener('change', handleVoiceChange);
    refreshConversationsBtn.addEventListener('click', loadConversationHistory);
    newConversationBtn.addEventListener('click', createNewConversation);
    
    // Request microphone access on first recording attempt rather than on page load
    let microphoneSetup = false;
    
    // Toggle voice activity detection
    async function toggleVoiceActivityDetection() {
        debugLog(`Toggle VAD called. Current state: vadActive=${vadActive}`);
        if (!vadActive) {
            // Start voice detection
            debugLog('Attempting to start voice detection');
            recordButton.textContent = 'Voice Detection Active (Click to Stop)';
            recordButton.classList.add('vad-active');
            try {
                await setupVoiceActivityDetection();
                vadActive = true;
                updateStatus('Listening for voice...');
                debugLog('Voice detection activated successfully');
            } catch (error) {
                debugLog(`Failed to start voice detection: ${error.message}`);
                recordButton.textContent = 'Start Voice Detection (Error)';
                recordButton.classList.remove('vad-active');
                updateStatus(`Error: ${error.message}`);
            }
        } else {
            // Stop voice detection
            debugLog('Stopping voice detection');
            recordButton.textContent = 'Start Voice Detection';
            recordButton.classList.remove('vad-active');
            stopVoiceActivityDetection();
            vadActive = false;
            updateStatus('Ready');
            debugLog('Voice detection deactivated');
        }
    }
    
    // Setup voice activity detection
    async function setupVoiceActivityDetection() {
        try {
            debugLog('Setting up voice activity detection');
            
            // Initialize AudioContext
            if (!audioContext) {
                debugLog('Creating new AudioContext');
                audioContext = new (window.AudioContext || window.webkitAudioContext)();
                debugLog(`New AudioContext created with state: ${audioContext.state}`);
                await audioContext.resume();
                debugLog(`AudioContext resumed with state: ${audioContext.state}`);
            } else if (audioContext.state === 'suspended') {
                debugLog('Resuming suspended AudioContext');
                await audioContext.resume();
                debugLog(`AudioContext resumed with state: ${audioContext.state}`);
            }
            
            // Setup microphone access if not already done
            debugLog('Setting up microphone');
            if (!await setupMicrophone()) {
                debugLog('Failed to set up microphone');
                throw new Error('Failed to set up microphone');
            }
            debugLog('Microphone setup successful');
            
            // Create a new conversation if none exists
            if (!currentConversationId) {
                debugLog('No active conversation, creating new one');
                await createNewConversation();
                debugLog(`New conversation created with ID: ${currentConversationId}`);
            }
            
            // Get media stream with specific constraints
            debugLog('Requesting media stream with constraints');
            vadStream = await navigator.mediaDevices.getUserMedia({
                audio: {
                    echoCancellation: true,
                    noiseSuppression: true,
                    autoGainControl: true,
                    sampleRate: 44100,
                }
            });
            debugLog(`Media stream obtained: ${vadStream.id}`);
            
            // Set up analyzer for voice detection
            debugLog('Setting up audio analyzer');
            vadAnalyser = audioContext.createAnalyser();
            const source = audioContext.createMediaStreamSource(vadStream);
            source.connect(vadAnalyser);
            
            vadAnalyser.fftSize = 256;
            const bufferLength = vadAnalyser.frequencyBinCount;
            vadDataArray = new Uint8Array(bufferLength);
            debugLog(`Analyzer setup complete: fftSize=${vadAnalyser.fftSize}, bufferLength=${bufferLength}`);
            
            // Start monitoring audio levels
            debugLog('Starting voice activity monitoring');
            checkVoiceActivity();
            
            debugLog('Voice activity detection setup complete');
        } catch (error) {
            debugLog(`Error setting up voice activity detection: ${error.message}`);
            console.error('Error setting up voice activity detection:', error);
            updateStatus(`Error: ${error.message}`);
            vadActive = false;
            recordButton.classList.remove('vad-active');
            recordButton.textContent = 'Start Voice Detection';
            throw error; // Re-throw to handle in the caller
        }
    }
    
    // Check for voice activity
    function checkVoiceActivity() {
        if (!vadActive) {
            debugLog('Voice activity check called but VAD not active');
            return;
        }
        
        try {
            vadAnalyser.getByteFrequencyData(vadDataArray);
            let sum = 0;
            for (let i = 0; i < vadDataArray.length; i++) {
                sum += vadDataArray[i];
            }
            const average = sum / vadDataArray.length;
            lastAudioLevel = average;
            
            // Log audio level less frequently to avoid flooding
            if (Math.random() < 0.1) { // Log roughly 10% of the time
                debugLog(`Audio level: ${average.toFixed(2)} (threshold: ${VAD_THRESHOLD})`);
            }
            
            // Visual feedback on voice level
            updateVoiceActivityVisual(average);
            
            if (average > VAD_THRESHOLD) {
                // Voice detected
                if (!voiceDetected && !isRecording) {
                    debugLog(`Voice detected (level: ${average.toFixed(2)}) - starting recording`);
                    voiceDetected = true;
                    startRecording();
                }
                
                // Reset silence timer on voice activity
                clearTimeout(silenceTimer);
                silenceTimer = setTimeout(() => {
                    if (isRecording) {
                        debugLog('Silence detected - stopping recording after timeout');
                        stopRecording();
                        voiceDetected = false;
                    }
                }, SILENCE_TIMEOUT);
            }
            
            vadAnimationFrame = requestAnimationFrame(checkVoiceActivity);
        } catch (error) {
            debugLog(`Error in voice activity check: ${error.message}`);
            console.error('Error in voice activity check:', error);
        }
    }
    
    // Update visual feedback for voice activity
    function updateVoiceActivityVisual(level) {
        // Create or update visualization element
        let visualizer = document.querySelector('.vad-visualizer');
        if (!visualizer) {
            visualizer = document.createElement('div');
            visualizer.className = 'vad-visualizer';
            recordButton.appendChild(visualizer);
            debugLog('Created voice activity visualizer');
        }
        
        // Update visualization level
        const height = Math.min(100, level * 3);
        visualizer.style.height = `${height}%`;
        
        // Change color based on activity level
        if (level > VAD_THRESHOLD) {
            visualizer.style.backgroundColor = '#4CAF50'; // Green for active voice
        } else {
            visualizer.style.backgroundColor = '#9E9E9E'; // Gray for silence
        }
    }
    
    // Stop voice activity detection
    function stopVoiceActivityDetection() {
        debugLog('Stopping voice activity detection');
        
        // Cancel animation frame
        if (vadAnimationFrame) {
            cancelAnimationFrame(vadAnimationFrame);
            vadAnimationFrame = null;
            debugLog('Cancelled animation frame');
        }
        
        // Clear silence timer
        if (silenceTimer) {
            clearTimeout(silenceTimer);
            silenceTimer = null;
            debugLog('Cleared silence timer');
        }
        
        // Stop recording if active
        if (isRecording) {
            debugLog('Recording was active - stopping it');
            stopRecording();
        }
        
        // Stop media stream tracks
        if (vadStream) {
            debugLog('Stopping media stream tracks');
            vadStream.getTracks().forEach(track => {
                track.stop();
                debugLog(`Stopped track: ${track.kind}`);
            });
            vadStream = null;
        }
        
        // Remove visualizer
        const visualizer = document.querySelector('.vad-visualizer');
        if (visualizer) {
            visualizer.remove();
            debugLog('Removed visualizer');
        }
        
        voiceDetected = false;
        vadActive = false;
        debugLog('Voice activity detection stopped completely');
    }
    
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
        debugLog(`Status updated: ${message}`);
        
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
    
    // Setup microphone access
    async function setupMicrophone() {
        if (microphoneSetup) {
            debugLog('Microphone already set up');
            return true;
        }
        
        try {
            debugLog('Requesting microphone access');
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            debugLog('Microphone access granted');
            
            // Check if we actually got audio tracks
            if (stream.getAudioTracks().length > 0) {
                debugLog(`Got ${stream.getAudioTracks().length} audio tracks`);
                const track = stream.getAudioTracks()[0];
                debugLog(`Track details: enabled=${track.enabled}, muted=${track.muted}, readyState=${track.readyState}`);
                
                // Get capabilities if supported
                if (track.getCapabilities) {
                    const capabilities = track.getCapabilities();
                    debugLog(`Microphone capabilities: ${JSON.stringify(capabilities)}`);
                }
            } else {
                debugLog('WARNING: No audio tracks in stream!');
            }
            
            // Stop this test stream since we'll create a new one for actual recording
            stream.getTracks().forEach(track => track.stop());
            
            microphoneSetup = true;
            return true;
        } catch (error) {
            debugLog(`Error accessing microphone: ${error.name} - ${error.message}`);
            updateStatus(`Error accessing microphone: ${error.message}`);
            console.error('Error accessing microphone:', error);
            return false;
        }
    }
    
    // Function setupVisualization remains unchanged but is used differently now
    function setupVisualization(stream) {
        if (!audioContext) return;
        
        // Create a visualization container
        const visualizer = document.createElement('div');
        visualizer.className = 'audio-visualizer';
        recordButton.appendChild(visualizer);
        
        // Create analyzer
        const analyser = audioContext.createAnalyser();
        const source = audioContext.createMediaStreamSource(stream);
        source.connect(analyser);
        
        analyser.fftSize = 32;
        const bufferLength = analyser.frequencyBinCount;
        const dataArray = new Uint8Array(bufferLength);
        
        // Create visualization bars
        for (let i = 0; i < bufferLength; i++) {
            const bar = document.createElement('div');
            bar.className = 'visualizer-bar';
            visualizer.appendChild(bar);
        }
        
        // Update visualization
        function updateVisualization() {
            if (!isRecording) {
                visualizer.remove();
                return;
            }
            
            analyser.getByteFrequencyData(dataArray);
            const bars = visualizer.querySelectorAll('.visualizer-bar');
            
            for (let i = 0; i < bars.length; i++) {
                const barHeight = dataArray[i] / 255 * 100;
                bars[i].style.height = barHeight + '%';
            }
            
            requestAnimationFrame(updateVisualization);
        }
        
        updateVisualization();
    }
    
    // Modify startRecording to work with voice detection
    async function startRecording() {
        try {
            debugLog('==== START RECORDING CALLED ====');
            
            // Initialize AudioContext as early as possible upon user interaction
            if (!audioContext) {
                debugLog('Creating new AudioContext in startRecording');
                audioContext = new (window.AudioContext || window.webkitAudioContext)();
                debugLog(`AudioContext initialized with state: ${audioContext.state}`);
            }
    
            if (audioContext && audioContext.state === 'suspended') {
                debugLog('Resuming suspended AudioContext');
                try {
                    await audioContext.resume();
                    debugLog(`AudioContext resumed. New state: ${audioContext.state}`);
                } catch (resumeError) {
                    debugLog(`Error resuming AudioContext: ${resumeError.message}`);
                    console.error('startRecording: Error resuming AudioContext:', resumeError);
                }
            }
    
            // If we're already recording, don't start a new recording
            if (isRecording) {
                debugLog('Already recording, ignoring start request');
                return;
            }
    
            // Setup Microphone
            if (!await setupMicrophone()) {
                debugLog('Failed to set up microphone');
                return;
            }
            debugLog('Microphone setup complete');
            
            // Create a new conversation if none exists
            if (!currentConversationId) {
                debugLog('No active conversation, creating new one');
                await createNewConversation();
            }
            
            // Stop any currently playing audio
            if (currentAudioSource) {
                debugLog('Stopping previous audio before recording');
                currentAudioSource.stop();
                if (currentAudioSource.onended) {
                    currentAudioSource.onended = null; // Clear handler
                }
                currentAudioSource = null;
            }
            
            // Use the existing stream from VAD if available, otherwise get a new one
            let stream;
            if (vadActive && vadStream) {
                stream = vadStream;
                debugLog('Using existing VAD stream for recording');
            } else {
                // Get User Media Stream with explicit constraints for audio quality
                debugLog('Requesting new media stream');
                stream = await navigator.mediaDevices.getUserMedia({
                    audio: {
                        echoCancellation: true,
                        noiseSuppression: true,
                        autoGainControl: true,
                        sampleRate: 44100,
                    }
                });
                debugLog(`Media stream obtained: ${stream.id}`);
            }
            
            // Verify stream has audio tracks
            if (stream.getAudioTracks().length === 0) {
                debugLog('ERROR: Stream has no audio tracks!');
                throw new Error('No audio tracks in stream');
            } else {
                const track = stream.getAudioTracks()[0];
                debugLog(`Using audio track: enabled=${track.enabled}, muted=${track.muted}, readyState=${track.readyState}`);
            }
            
            // MediaRecorder Setup with MIME Type
            debugLog('Setting up MediaRecorder');
            const options = { mimeType: 'audio/webm; codecs=opus' };
            if (!MediaRecorder.isTypeSupported(options.mimeType)) {
                debugLog(`${options.mimeType} is not Supported, trying audio/webm`);
                options.mimeType = 'audio/webm'; 
                if (!MediaRecorder.isTypeSupported(options.mimeType)) {
                    debugLog(`${options.mimeType} is not Supported, browser default will be used`);
                    delete options.mimeType; 
                }
            }
            
            try {
                mediaRecorder = new MediaRecorder(stream, options);
                recordedMimeType = mediaRecorder.mimeType; // Store the actual MIME type
                debugLog(`MediaRecorder initialized with MIME type: ${recordedMimeType}`);
            } catch (recorderError) {
                debugLog(`Error creating MediaRecorder: ${recorderError.message}`);
                throw recorderError;
            }
    
            audioChunks = [];
            
            mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    audioChunks.push(event.data);
                    debugLog(`Audio chunk received: ${event.data.size} bytes`);
                } else {
                    debugLog('Empty audio chunk received (ignoring)');
                }
            };
            
            mediaRecorder.onstop = async () => {
                debugLog(`MediaRecorder stopped, processing ${audioChunks.length} chunks`);
                
                // Only process audio if we have actual content
                if (audioChunks.length > 0 && audioChunks.some(chunk => chunk.size > 0)) {
                    const totalBytes = audioChunks.reduce((sum, chunk) => sum + chunk.size, 0);
                    debugLog(`Processing audio: ${totalBytes} total bytes`);
                    // Use the stored, correct MIME type here
                    await processAudio(new Blob(audioChunks, { type: recordedMimeType || 'audio/webm' }));
                } else {
                    debugLog('No audio data to process (empty chunks)');
                    updateStatus(vadActive ? 'Listening for voice...' : 'Ready');
                }
            };
            
            try {
                mediaRecorder.start();
                debugLog('MediaRecorder started successfully');
                isRecording = true;
                updateStatus('Recording...');
                recordButton.classList.add('recording');
            } catch (startError) {
                debugLog(`Error starting MediaRecorder: ${startError.message}`);
                throw startError;
            }
    
            // Add visualization for audio feedback only in non-VAD mode
            if (!vadActive) {
                setupVisualization(mediaRecorder.stream);
            }
    
        } catch (error) {
            debugLog(`ERROR starting recording: ${error.name} - ${error.message}`);
            console.error('startRecording: Error starting recording:', error);
            // Provide more specific error message to the user if possible
            if (error.name === 'NotAllowedError' || error.name === 'PermissionDeniedError') {
                statusElement.textContent = 'Microphone access denied.';
            } else if (error.name === 'NotFoundError') {
                statusElement.textContent = 'No microphone found.';
            } else {
                statusElement.textContent = `Error starting recording: ${error.message}`;
            }
        }
    }
    
    // Stop recording
    function stopRecording() {
        debugLog('==== STOP RECORDING CALLED ====');
        if (isRecording && mediaRecorder) {
            try {
                debugLog(`Stopping MediaRecorder (state: ${mediaRecorder.state})`);
                mediaRecorder.stop();
                debugLog('MediaRecorder stopped');
                isRecording = false;
                updateStatus('Processing...');
                recordButton.classList.remove('recording');
                
                // Only stop tracks if not using VAD
                if (!vadActive) {
                    debugLog('Stopping audio tracks (non-VAD mode)');
                    mediaRecorder.stream.getTracks().forEach(track => {
                        track.stop();
                        debugLog(`Stopped track: ${track.kind}`);
                    });
                } else {
                    debugLog('Keeping audio tracks active (VAD mode)');
                }
            } catch (error) {
                debugLog(`Error stopping recording: ${error.message}`);
                console.error('Error stopping recording:', error);
            }
        } else {
            debugLog(`Not recording or no mediaRecorder (isRecording=${isRecording})`);
        }
    }
    
    // Process audio
    async function processAudio(audioBlob) {
        try {
            debugLog(`Processing audio blob: size=${audioBlob.size} bytes, type=${audioBlob.type}`);
            updateStatus('Processing...');
            
            const formData = new FormData();
            formData.append('audio', audioBlob);
            formData.append('voice_id', currentVoiceId);
            debugLog(`Using voice_id: ${currentVoiceId}`);
            
            debugLog('Sending audio to server...');
            const startTime = performance.now();
            const response = await fetch('/process_audio', {
                method: 'POST',
                body: formData
            });
            const elapsed = (performance.now() - startTime) / 1000;
            debugLog(`Server response received in ${elapsed.toFixed(2)}s with status: ${response.status}`);
            
            if (!response.ok) {
                debugLog(`Server error: ${response.status} ${response.statusText}`);
                throw new Error(`Server returned status: ${response.status}`);
            }
            
            const data = await response.json();
            debugLog(`Response data received: status=${data.status}`);
            if (data.user_transcription) {
                debugLog(`Transcription: "${data.user_transcription.substring(0, 50)}${data.user_transcription.length > 50 ? '...' : ''}"`);
            } else {
                debugLog('No transcription received');
            }
            
            if (data.status === 'success') {
                // Add user message
                addMessage('user', data.user_transcription);
                
                // Add assistant message
                addMessage('assistant', data.assistant_response_text);
                
                // Play audio response if available
                if (data.assistant_response_audio) {
                    debugLog(`Audio response received: ${data.assistant_response_audio.length} bytes`);
                    playAudioResponse(data.assistant_response_audio);
                } else {
                    debugLog('No audio response received from server');
                }
                
                // Refresh conversation list to show the updated conversation
                await loadConversationHistory();
                
                updateStatus('Ready');
            } else if (data.status === 'exit') {
                debugLog('Exit command detected');
                addMessage('assistant', data.assistant_response_text);
                updateStatus('Conversation ended');
                recordButton.disabled = true;
                
                // Refresh conversation list
                await loadConversationHistory();
            } else {
                throw new Error(data.message || 'Failed to process audio');
            }
        } catch (error) {
            debugLog(`Error processing audio: ${error.message}`);
            console.error('processAudio: Error processing audio:', error);
            updateStatus(`Error: ${error.message || 'Failed to process audio'}`);
            
            // Enable the record button again so users can retry
            recordButton.disabled = false;
            recordButton.classList.remove('recording');
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
            debugLog('playAudioResponse: Called with audio length:', base64Audio ? base64Audio.length : 0);
            
            if (!base64Audio || base64Audio.length === 0) {
                debugLog('playAudioResponse: Empty audio data received');
                return;
            }

            // Initialize audio context if not already done
            if (!audioContext) {
                audioContext = new (window.AudioContext || window.webkitAudioContext)();
                debugLog('playAudioResponse: AudioContext initialized with state:', audioContext.state);
            }

            // Resume AudioContext - this is critical for browsers that suspend by default
            if (audioContext.state === 'suspended') {
                debugLog('playAudioResponse: AudioContext is suspended, attempting to resume...');
                await audioContext.resume();
                debugLog('playAudioResponse: AudioContext resume attempt completed. New state:', audioContext.state);
            }
            
            if (audioContext.state !== 'running') {
                debugLog('playAudioResponse: AudioContext is NOT running after attempt to resume. State:', audioContext.state);
                // Try to create a fresh audio context as a fallback
                debugLog('playAudioResponse: Attempting to create new AudioContext as fallback');
                audioContext = new (window.AudioContext || window.webkitAudioContext)();
                await audioContext.resume();
                debugLog('playAudioResponse: New AudioContext state:', audioContext.state);
            }
            
            // Stop any currently playing audio
            if (currentAudioSource) {
                debugLog('playAudioResponse: Stopping existing audio source');
                currentAudioSource.stop();
                currentAudioSource.onended = null; // Clear previous handler
                currentAudioSource = null;
            }
            
            // Convert base64 to ArrayBuffer
            debugLog('playAudioResponse: Converting base64 to ArrayBuffer');
            const binaryString = atob(base64Audio);
            const len = binaryString.length;
            const bytes = new Uint8Array(len);
            
            for (let i = 0; i < len; i++) {
                bytes[i] = binaryString.charCodeAt(i);
            }
            
            debugLog(`playAudioResponse: Created bytes array of length ${bytes.length}`);
            
            // Decode audio data
            debugLog('playAudioResponse: Decoding audio data...');
            let audioBuffer;
            try {
                audioBuffer = await audioContext.decodeAudioData(bytes.buffer);
                debugLog(`playAudioResponse: Audio successfully decoded, duration: ${audioBuffer.duration}s, channels: ${audioBuffer.numberOfChannels}`);
            } catch (decodeError) {
                debugLog('playAudioResponse: Failed to decode audio:');
                console.error('playAudioResponse: Failed to decode audio:', decodeError);
                // Try playing as a regular HTML5 audio element as fallback
                debugLog('playAudioResponse: Attempting HTML5 Audio fallback');
                const audioElement = new Audio(`data:audio/mp3;base64,${base64Audio}`);
                audioElement.play().then(() => {
                    debugLog('playAudioResponse: HTML5 Audio fallback successful');
                }).catch(htmlAudioError => {
                    debugLog('playAudioResponse: HTML5 Audio fallback failed:');
                    console.error('playAudioResponse: HTML5 Audio fallback failed:', htmlAudioError);
                });
                return;
            }
            
            // Create and play audio source
            debugLog('playAudioResponse: Creating audio source');
            const source = audioContext.createBufferSource();
            source.buffer = audioBuffer;
            source.connect(audioContext.destination);
            
            // Save reference to current source for potential interruption
            currentAudioSource = source;
            
            // Add event handlers
            source.onended = () => {
                debugLog('playAudioResponse: Audio playback completed naturally');
                currentAudioSource = null;
            };
            
            // Actually play the audio
            debugLog('playAudioResponse: Starting audio playback');
            source.start(0);
            debugLog('playAudioResponse: Audio playback started');
            
        } catch (error) {
            debugLog('playAudioResponse: Error playing audio:');
            console.error('playAudioResponse: Error playing audio:', error);
            // Try one more fallback approach with vanilla HTML audio
            try {
                debugLog('playAudioResponse: Attempting final HTML5 Audio fallback');
                const audioBlob = new Blob(
                    [Uint8Array.from(atob(base64Audio), c => c.charCodeAt(0))], 
                    {type: 'audio/mp3'}
                );
                const audioUrl = URL.createObjectURL(audioBlob);
                const audio = new Audio(audioUrl);
                audio.play();
                debugLog('playAudioResponse: Final HTML5 Audio fallback attempted');
            } catch (fallbackError) {
                debugLog('playAudioResponse: All audio playback attempts failed:');
                console.error('playAudioResponse: All audio playback attempts failed:', fallbackError);
            }
        }
    }
    
    // Add touch support for mobile devices - convert to toggle for VAD
    recordButton.addEventListener('touchstart', function(e) {
        e.preventDefault(); // Prevent default touch behavior
        toggleVoiceActivityDetection();
    });
    
    // Remove touchend handler since we're using toggle now
    recordButton.removeEventListener('touchend', stopRecording);
    
    // Add diagnostic function to test audio system
    async function testAudioSystem() {
        debugLog('==== AUDIO SYSTEM DIAGNOSTIC ====');
        
        // Check if browser supports necessary audio APIs
        debugLog('1. Browser capability check:');
        debugLog(` - AudioContext supported: ${typeof AudioContext !== 'undefined' || typeof webkitAudioContext !== 'undefined'}`);
        debugLog(` - MediaRecorder supported: ${typeof MediaRecorder !== 'undefined'}`);
        debugLog(` - getUserMedia supported: ${!!(navigator.mediaDevices && typeof navigator.mediaDevices.getUserMedia !== 'undefined')}`);
        debugLog(' - Supported MIME types for recording:');
        
        const testMimeTypes = [
            'audio/webm', 
            'audio/webm;codecs=opus', 
            'audio/mp4',
            'audio/wav',
            'audio/ogg'
        ];
        
        testMimeTypes.forEach(type => {
            if (typeof MediaRecorder !== 'undefined') {
                debugLog(`   - ${type}: ${MediaRecorder.isTypeSupported(type)}`);
            }
        });
        
        // Test AudioContext creation
        debugLog('2. AudioContext creation test:');
        try {
            const testContext = new (window.AudioContext || window.webkitAudioContext)();
            debugLog(' - AudioContext created successfully');
            debugLog(` - Sample rate: ${testContext.sampleRate}`);
            debugLog(` - Initial state: ${testContext.state}`);
            
            // Test resume capability
            if (testContext.state === 'suspended') {
                try {
                    debugLog(' - Attempting to resume AudioContext...');
                    await testContext.resume();
                    debugLog(` - Resume successful, new state: ${testContext.state}`);
                } catch (resumeError) {
                    debugLog(` - Error resuming AudioContext: ${resumeError.message}`);
                }
            }
            
            // Clean up
            testContext.close();
        } catch (contextError) {
            debugLog(` - Error creating AudioContext: ${contextError.message}`);
        }
        
        // Test audio decoding with a minimal audio
        debugLog('3. Audio decoding capability test:');
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
            debugLog(' - Audio decoding successful');
            debugLog(` - Decoded audio duration: ${result.duration}`);
            debugLog(` - Decoded audio channels: ${result.numberOfChannels}`);
            
        } catch (decodeError) {
            debugLog(` - Audio decoding failed: ${decodeError.message}`);
        }
        
        debugLog('==== DIAGNOSTIC COMPLETE ====');
    }

    // Initialize the app
    updateStatus('Ready');
    debugLog('Application initialized');
    
    // Update button text for new functionality
    recordButton.textContent = 'Start Voice Detection';
    
    // Run audio system diagnostic
    testAudioSystem().catch(err => console.error('Audio diagnostic error:', err));

    // Style record button for new functionality
    function styleRecordButton() {
        recordButton.innerHTML = `
            <div class="record-button-inner">
                <div class="record-icon"></div>
                <span>Start Voice Detection</span>
            </div>
        `;
    }
    styleRecordButton();

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