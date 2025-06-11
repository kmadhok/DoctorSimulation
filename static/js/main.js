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
    
    // Load available simulations (now static only)
    async function loadSimulations() {
        // No need to fetch from API anymore - simulation options are static in HTML
        // Just ensure current simulation is properly set if available
        console.log('Simulation loading complete - using static options only');
        
        // Set current simulation if available
        if (currentSimulation) {
            simulationSelect.value = currentSimulation;
        }
    }
    
    // Load available simulations
    console.log('<<<<< MAIN.JS: Awaiting loadSimulations... >>>>>');
    await loadSimulations();
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
    
    // Custom Patient Form Event Listeners
    if (cancelCustomPatientBtn) {
        cancelCustomPatientBtn.addEventListener('click', () => {
            // Reset dropdown to "No simulation" and hide form
            simulationSelect.value = '';
            hideCustomPatientForm();
            updateStatus('Ready');
        });
    }
    
    if (customPatientFormFields) {
        customPatientFormFields.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            // Validate form using new AI validation system
            if (!validateCustomPatientForm()) {
                updateStatus('Please fix the errors in the form');
                return;
            }
            
            // Show loading state with enhanced UI
            setFormLoading(true);
            updateStatus('Generating AI patient case...');
            
            try {
                // Collect form data using new structure
                const customPatientData = collectCustomPatientData();
                console.log('Creating AI patient case with data:', customPatientData);
                
                // Call the backend API to generate custom patient case
                const success = await createCustomPatient(customPatientData);
                
                if (success) {
                    updateStatus('AI patient case generated successfully!');
                    setFormLoading(false);
                    // Hide form and refresh conversation list
                    hideCustomPatientForm();
                    await loadConversationHistory();
                } else {
                    updateStatus('Error generating patient case');
                    setFormLoading(false);
                }
            } catch (error) {
                console.error('Error generating patient case:', error);
                updateStatus('Error generating patient case');
                setFormLoading(false);
            }
        });

        // Enhanced real-time validation feedback
        const formInputs = customPatientFormFields.querySelectorAll('.form-control');
        formInputs.forEach(input => {
            // Blur validation
            input.addEventListener('blur', () => {
                if (formState.realTimeValidation) {
                    validateSingleField(input);
                }
            });
            
            // Input validation (clear errors)
            input.addEventListener('input', () => {
                clearSingleFieldError(input);
            });
        });

        // Specialty change handler for dynamic symptom loading
        if (medicalSpecialtySelect) {
            medicalSpecialtySelect.addEventListener('change', handleSpecialtyChange);
        }
    }

    // Wizard Event Listeners
    const wizardBackBtn = document.getElementById('wizardBackBtn');
    const wizardNextBtn = document.getElementById('wizardNextBtn');
    const wizardGenerateBtn = document.getElementById('wizardGenerateBtn');
    const closeWizardBtn = document.getElementById('closeWizardBtn');
    const wizardBackdrop = document.querySelector('.wizard-backdrop');
    const wizardSpecialtySelect = document.getElementById('wizardSpecialty');

    if (wizardBackBtn) {
        wizardBackBtn.addEventListener('click', previousWizardStep);
    }

    if (wizardNextBtn) {
        wizardNextBtn.addEventListener('click', nextWizardStep);
    }

    if (wizardGenerateBtn) {
        wizardGenerateBtn.addEventListener('click', generatePatientCaseFromWizard);
    }

    if (closeWizardBtn) {
        closeWizardBtn.addEventListener('click', hidePatientWizard);
    }

    if (wizardBackdrop) {
        wizardBackdrop.addEventListener('click', hidePatientWizard);
    }

    if (wizardSpecialtySelect) {
        wizardSpecialtySelect.addEventListener('change', handleWizardSpecialtyChange);
    }

    // Handle Escape key to close wizard
    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape') {
            const wizardModal = document.getElementById('patientCaseWizard');
            if (wizardModal && wizardModal.style.display === 'flex') {
                hidePatientWizard();
            }
        }
    });
   
      
    
    // Create a new empty conversation
    async function createNewConversation() {
        try {
            updateStatus('Creating new conversation...');
            
            // Clear simulation selection and hide custom form
            simulationSelect.value = '';
            currentSimulation = null;
            hideCustomPatientForm();
            
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
                
                // Clear patient details panel
                patientDetailsPanel.innerHTML = '';
                
                // Reset diagnosis panel for new conversation
                resetDiagnosisPanel();
                
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
                
                // Handle different simulation types
                if (data.conversation.simulation_file === '__custom__') {
                    // Custom patient conversation
                    currentSimulation = '__custom__';
                    simulationSelect.value = '__custom__';
                    // Hide custom patient form since we're loading an existing conversation
                    hideCustomPatientForm();
                } else if (data.conversation.simulation_file) {
                    // File-based patient simulation
                    currentSimulation = data.conversation.simulation_file;
                    simulationSelect.value = currentSimulation;
                    hideCustomPatientForm();
                } else {
                    // No simulation associated
                    currentSimulation = null;
                    simulationSelect.value = '';
                    hideCustomPatientForm();
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
                
                // Load patient details for any type of patient simulation
                if (data.conversation.simulation_file) {
                    await loadPatientDetails();
                } else {
                    // Clear patient details panel if no simulation
                    patientDetailsPanel.innerHTML = '';
                }
                
                // Update UI
                updateStatus('Ready');
                
                // Reset diagnosis panel for loaded conversation
                resetDiagnosisPanel();
                
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
        
        // Check if custom patient is selected
        if (selectedSimulation === '__custom__') {
            console.log('Custom patient selected - showing wizard');
            showPatientWizard();
            statusElement.textContent = 'Create your custom patient';
            patientDetailsPanel.innerHTML = '';
            return;
        }
        
        // Hide wizard if it was shown
        hidePatientWizard();
        
        // Hide custom patient form if it was shown
        hideCustomPatientForm();
        
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
                
                // Reset diagnosis panel for new simulation
                resetDiagnosisPanel();
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
    
    // ========== CUSTOM PATIENT FORM FUNCTIONS ==========
    
    function showCustomPatientForm() {
        if (customPatientForm) {
            customPatientForm.style.display = 'block';
            customPatientForm.classList.add('show');
            clearCustomPatientForm(); // Start with a clean form
        }
    }
    
    function hideCustomPatientForm() {
        if (customPatientForm) {
            customPatientForm.style.display = 'none';
            customPatientForm.classList.remove('show');
            clearAllErrorMessages();
        }
    }
    
    function validateCustomPatientForm() {
        let isValid = true;
        const errors = [];

        // Clear previous validation
        clearAllErrors();

        // Get form data
        const formData = new FormData(customPatientFormFields);
        const data = Object.fromEntries(formData.entries());

        // Age validation
        const age = parseInt(data.age);
        if (!data.age || isNaN(age) || age < 1 || age > 120) {
            showFieldError('ageError', 'Age must be between 1 and 120');
            errors.push('Valid age is required');
            isValid = false;
        }

        // Gender validation
        if (!data.gender) {
            showFieldError('genderError', 'Gender selection is required');
            errors.push('Gender selection is required');
            isValid = false;
        }

        // Occupation validation
        if (!data.occupation || data.occupation.trim().length < 2) {
            showFieldError('occupationError', 'Occupation is required (at least 2 characters)');
            errors.push('Occupation is required');
            isValid = false;
        }

        // Specialty validation
        if (!formState.selectedSpecialty) {
            showFieldError('specialtyError', 'Medical specialty selection is required');
            errors.push('Medical specialty selection is required');
            isValid = false;
        }

        // Symptoms validation
        if (formState.selectedSymptoms.length === 0) {
            showFieldError('symptomsError', 'At least one symptom must be selected');
            errors.push('At least one symptom must be selected');
            isValid = false;
        }

        // Severity validation
        const severity = document.getElementById('symptomSeverity')?.value;
        if (!severity) {
            showFieldError('severityError', 'Symptom severity selection is required');
            errors.push('Symptom severity selection is required');
            isValid = false;
        }

        // Show validation summary if there are errors
        if (!isValid) {
            showValidationSummary(errors);
        } else {
            hideValidationSummary();
        }

        return isValid;
    }
    
    function showFormErrors(errors) {
        // Clear all previous errors
        clearAllErrorMessages();
        
        // Show new errors
        Object.keys(errors).forEach(fieldName => {
            const errorElement = document.getElementById(fieldName + 'Error');
            const inputElement = document.getElementById('patient' + fieldName.charAt(0).toUpperCase() + fieldName.slice(1));
            
            if (errorElement) {
                errorElement.textContent = errors[fieldName];
            }
            
            if (inputElement) {
                inputElement.classList.add('error');
            }
        });
    }
    
    function clearAllErrorMessages() {
        const errorElements = customPatientForm.querySelectorAll('.error-message');
        errorElements.forEach(element => {
            element.textContent = '';
        });
        
        const inputElements = customPatientForm.querySelectorAll('.form-control');
        inputElements.forEach(element => {
            element.classList.remove('error');
        });
    }
    
    // Updated data collection for AI case generation
    function collectCustomPatientData() {
        const formData = new FormData(customPatientFormFields);
        const data = Object.fromEntries(formData.entries());
        
        // Structure the data for AI case generation API
        // Backend expects all fields in case_parameters
        return {
            type: 'ai_generated',
            case_parameters: {
                age: parseInt(data.age),
                gender: data.gender,
                occupation: data.occupation,
                medical_history: data.medical_history || '',
                specialty: formState.selectedSpecialty,
                symptoms: formState.selectedSymptoms,
                severity: data.severity
            }
        };
    }
    
    function clearCustomPatientForm() {
        if (customPatientFormFields) {
            customPatientFormFields.reset();
            
            // Reset form state
            formState.selectedSpecialty = null;
            formState.selectedSymptoms = [];
            
            // Clear specialty-related UI
            if (specialtyDescription) {
                specialtyDescription.textContent = '';
                specialtyDescription.style.display = 'none';
            }
            
            if (symptomsContainer) {
                symptomsContainer.style.display = 'none';
                symptomsContainer.innerHTML = '';
            }
            
            if (symptomsInstructions) {
                symptomsInstructions.style.display = 'block';
                symptomsInstructions.textContent = 'Select a specialty above to see available symptoms';
                symptomsInstructions.style.color = '';
            }
            
            clearAllErrors();
        }
    }
    
    function setFormLoading(isLoading) {
        formState.isLoading = isLoading;
        
        const submitBtn = createCustomPatientBtn;
        const cancelBtn = cancelCustomPatientBtn;
        const loadingDiv = aiGenerationLoading;
        const formFields = customPatientFormFields;
        const buttonText = submitBtn?.querySelector('.button-text');
        const buttonSpinner = submitBtn?.querySelector('.button-spinner');

        if (isLoading) {
            // Show loading overlay
            if (loadingDiv) loadingDiv.style.display = 'block';
            
            // Disable form
            if (formFields) {
                formFields.style.opacity = '0.6';
                formFields.style.pointerEvents = 'none';
            }
            
            // Update button states
            if (submitBtn) {
                submitBtn.disabled = true;
                if (buttonText) buttonText.style.display = 'none';
                if (buttonSpinner) buttonSpinner.style.display = 'inline';
            }
            if (cancelBtn) cancelBtn.disabled = true;
        } else {
            // Hide loading overlay
            if (loadingDiv) loadingDiv.style.display = 'none';
            
            // Enable form
            if (formFields) {
                formFields.style.opacity = '1';
                formFields.style.pointerEvents = 'auto';
            }
            
            // Update button states
            if (submitBtn) {
                submitBtn.disabled = false;
                if (buttonText) buttonText.style.display = 'inline';
                if (buttonSpinner) buttonSpinner.style.display = 'none';
            }
            if (cancelBtn) cancelBtn.disabled = false;
        }
    }
    
    function validateSingleField(input) {
        const fieldName = input.name;
        const value = input.value.trim();
        let error = '';
        
        switch (fieldName) {
            case 'age':
                const age = parseInt(value);
                if (!value || isNaN(age) || age < 1 || age > 120) {
                    error = 'Please enter a valid age between 1 and 120';
                }
                break;
            case 'gender':
                if (!value) {
                    error = 'Please select a gender';
                }
                break;
            case 'occupation':
                if (!value || value.length < 2) {
                    error = 'Please enter an occupation (at least 2 characters)';
                }
                break;
            case 'specialty':
                if (!formState.selectedSpecialty) {
                    error = 'Please select a medical specialty';
                }
                break;
            case 'severity':
                if (!value) {
                    error = 'Please select symptom severity';
                }
                break;
            // medical_history is optional, so no validation needed
        }
        
        // Show/hide error for this field
        if (error) {
            showFieldError(fieldName + 'Error', error);
            return false;
        } else {
            clearFieldError(fieldName + 'Error');
            return true;
        }
    }
    
    async function createCustomPatient(customPatientData) {
        try {
            console.log('Sending AI patient case data to backend:', customPatientData);
            
            const response = await fetch('/api/generate-patient-case', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(customPatientData)
            });
            
            const data = await response.json();
            console.log('Backend response:', data);
            
            if (data.status === 'success') {
                // Update global state
                currentConversationId = data.conversation_id;
                currentSimulation = '__custom__';
                
                // Keep track of current voice selection and update for this conversation
                currentVoiceId = voiceSelect.value;
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
                
                // Display patient details (excluding diagnosis for UI)
                if (data.patient_details) {
                    displayPatientDetails(data.patient_details);
                }
                
                // Clear conversation display for new conversation
                conversationElement.innerHTML = '';
                
                // Reset diagnosis panel for new AI patient case
                resetDiagnosisPanel();
                
                console.log('AI patient case generated successfully with conversation ID:', currentConversationId);
                return true;
            } else {
                console.error('Backend error:', data.message);
                updateStatus(`Error: ${data.message}`);
                
                // Show specific validation errors if available
                if (data.validation_errors) {
                    showValidationSummary(data.validation_errors);
                }
                
                return false;
            }
            
        } catch (error) {
            console.error('Network error generating patient case:', error);
            updateStatus('Network error - please check your connection');
            showFormError('Network error occurred. Please check your connection and try again.');
            return false;
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
            formData.append('conversation_id', currentConversationId);
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
    
    // Initialize medical knowledge for AI case generation
    initializeMedicalKnowledge();
    
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

    // Initialize medical knowledge and form functionality
    async function initializeMedicalKnowledge() {
        try {
            const response = await fetch('/api/medical-knowledge');
            const data = await response.json();
            
            if (data.status === 'success') {
                medicalKnowledge = data;
                populateSpecialtySelector();
                console.log('Medical knowledge loaded:', medicalKnowledge);
            } else {
                console.error('Failed to load medical knowledge:', data.message);
                showFormError('Failed to load medical specialties. Please refresh the page.');
            }
        } catch (error) {
            console.error('Error loading medical knowledge:', error);
            showFormError('Failed to load medical specialties. Please check your connection and refresh.');
        }
    }

    // Populate specialty selector with options
    function populateSpecialtySelector() {
        if (!medicalSpecialtySelect) return;

        // Clear existing options (except the first one)
        while (medicalSpecialtySelect.options.length > 1) {
            medicalSpecialtySelect.removeChild(medicalSpecialtySelect.lastChild);
        }

        // Add specialty options
        Object.entries(medicalKnowledge.specialties).forEach(([key, specialty]) => {
            const option = document.createElement('option');
            option.value = key;
            option.textContent = specialty.name;
            option.dataset.description = specialty.description;
            medicalSpecialtySelect.appendChild(option);
        });
    }

    // Handle specialty selection change for dynamic symptom loading
    function handleSpecialtyChange(event) {
        const selectedKey = event.target.value;
        
        formState.selectedSpecialty = selectedKey;
        formState.selectedSymptoms = []; // Reset selected symptoms

        if (selectedKey && medicalKnowledge.specialties[selectedKey]) {
            const specialty = medicalKnowledge.specialties[selectedKey];
            
            // Show specialty description
            if (specialtyDescription) {
                specialtyDescription.textContent = specialty.description;
                specialtyDescription.style.display = 'block';
            }
            
            // Populate symptoms for this specialty
            populateSymptoms(specialty.symptoms);
            
            // Show symptoms container
            if (symptomsInstructions) symptomsInstructions.style.display = 'none';
            if (symptomsContainer) symptomsContainer.style.display = 'block';
        } else {
            // Clear everything
            if (specialtyDescription) {
                specialtyDescription.textContent = '';
                specialtyDescription.style.display = 'none';
            }
            if (symptomsContainer) symptomsContainer.style.display = 'none';
            if (symptomsInstructions) {
                symptomsInstructions.style.display = 'block';
                symptomsInstructions.textContent = 'Select a specialty above to see available symptoms';
            }
        }

        // Clear any previous validation errors
        clearFieldError('specialtyError');
        clearFieldError('symptomsError');
    }

    // Populate symptoms checkboxes for selected specialty
    function populateSymptoms(symptomKeys) {
        if (!symptomsContainer) return;

        // Clear existing checkboxes
        symptomsContainer.innerHTML = '';

        // Add instructions and controls
        const controlsDiv = document.createElement('div');
        controlsDiv.className = 'symptoms-controls';
        controlsDiv.innerHTML = `
            <div class="symptoms-instructions">
                <small>Select one or more symptoms that the patient should present with:</small>
            </div>
            <div class="symptoms-actions">
                <button type="button" class="btn-link" id="selectAllSymptoms">Select All</button>
                <button type="button" class="btn-link" id="clearAllSymptoms">Clear All</button>
            </div>
        `;
        symptomsContainer.appendChild(controlsDiv);

        // Create symptom checkboxes
        const checkboxesDiv = document.createElement('div');
        checkboxesDiv.className = 'symptoms-checkboxes';
        
        symptomKeys.forEach(symptomKey => {
            const symptomName = medicalKnowledge.all_symptoms[symptomKey] || symptomKey;
            
            const checkboxDiv = document.createElement('div');
            checkboxDiv.className = 'symptom-checkbox';
            
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.id = `symptom_${symptomKey}`;
            checkbox.value = symptomKey;
            checkbox.addEventListener('change', handleSymptomChange);
            
            const label = document.createElement('label');
            label.htmlFor = `symptom_${symptomKey}`;
            label.textContent = symptomName;
            
            checkboxDiv.appendChild(checkbox);
            checkboxDiv.appendChild(label);
            checkboxesDiv.appendChild(checkboxDiv);
        });

        symptomsContainer.appendChild(checkboxesDiv);

        // Add event listeners for Select All / Clear All
        const selectAllBtn = document.getElementById('selectAllSymptoms');
        const clearAllBtn = document.getElementById('clearAllSymptoms');

        if (selectAllBtn) {
            selectAllBtn.addEventListener('click', () => {
                const checkboxes = symptomsContainer.querySelectorAll('input[type="checkbox"]');
                checkboxes.forEach(checkbox => {
                    checkbox.checked = true;
                    handleSymptomChange({ target: checkbox });
                });
            });
        }

        if (clearAllBtn) {
            clearAllBtn.addEventListener('click', () => {
                const checkboxes = symptomsContainer.querySelectorAll('input[type="checkbox"]');
                checkboxes.forEach(checkbox => {
                    checkbox.checked = false;
                    handleSymptomChange({ target: checkbox });
                });
            });
        }
    }

    // Handle symptom checkbox changes
    function handleSymptomChange(event) {
        const symptomKey = event.target.value;
        
        if (event.target.checked) {
            if (!formState.selectedSymptoms.includes(symptomKey)) {
                formState.selectedSymptoms.push(symptomKey);
            }
        } else {
            formState.selectedSymptoms = formState.selectedSymptoms.filter(s => s !== symptomKey);
        }

        console.log('Selected symptoms:', formState.selectedSymptoms);
        
        // Clear symptoms validation error if at least one selected
        if (formState.selectedSymptoms.length > 0) {
            clearFieldError('symptomsError');
        }

        // Real-time validation feedback
        if (formState.realTimeValidation) {
            validateSymptomSelection();
        }
    }

    // Validate symptom selection in real-time
    function validateSymptomSelection() {
        if (formState.selectedSymptoms.length === 0 && formState.selectedSpecialty) {
            showFieldError('symptomsError', 'At least one symptom must be selected');
            return false;
        } else {
            clearFieldError('symptomsError');
            return true;
        }
    }

    // Show form error message
    function showFormError(message) {
        if (symptomsInstructions) {
            symptomsInstructions.textContent = message;
            symptomsInstructions.style.color = 'red';
        }
    }

    // Clear all validation errors
    function clearAllErrors() {
        clearAllErrorMessages();
        hideValidationSummary();
    }

    // Show individual field error
    function showFieldError(elementId, message) {
        const errorElement = document.getElementById(elementId);
        if (errorElement) {
            errorElement.textContent = message;
            errorElement.style.display = 'block';
        }

        // Also add error class to corresponding input
        const fieldName = elementId.replace('Error', '');
        const inputElement = document.getElementById('patient' + fieldName.charAt(0).toUpperCase() + fieldName.slice(1)) ||
                           document.getElementById(fieldName) ||
                           document.querySelector(`[name="${fieldName}"]`);
        if (inputElement) {
            inputElement.classList.add('error');
        }
    }

    // Clear individual field error
    function clearFieldError(elementId) {
        const errorElement = document.getElementById(elementId);
        if (errorElement) {
            errorElement.textContent = '';
            errorElement.style.display = 'none';
        }

        // Also remove error class from corresponding input
        const fieldName = elementId.replace('Error', '');
        const inputElement = document.getElementById('patient' + fieldName.charAt(0).toUpperCase() + fieldName.slice(1)) ||
                           document.getElementById(fieldName) ||
                           document.querySelector(`[name="${fieldName}"]`);
        if (inputElement) {
            inputElement.classList.remove('error');
        }
    }

    // Clear single field error (used in real-time validation)
    function clearSingleFieldError(input) {
        const fieldName = input.name;
        const errorElement = document.getElementById(fieldName + 'Error');
        if (errorElement && errorElement.textContent) {
            errorElement.textContent = '';
            errorElement.style.display = 'none';
            input.classList.remove('error');
        }
    }

    // Show validation summary
    function showValidationSummary(errors) {
        if (formValidationSummary && validationErrorsList) {
            validationErrorsList.innerHTML = '';
            errors.forEach(error => {
                const li = document.createElement('li');
                li.textContent = error;
                validationErrorsList.appendChild(li);
            });
            formValidationSummary.style.display = 'block';
            formValidationSummary.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
    }

    // Hide validation summary
    function hideValidationSummary() {
        if (formValidationSummary) {
            formValidationSummary.style.display = 'none';
        }
    }

    // Initialize diagnosis panel functionality
    // NEW: Diagnosis Panel Functions (moved inside DOMContentLoaded for proper scope access)

    function initializeDiagnosisPanel() {
        const submitBtn = document.getElementById('submitDiagnosisBtn');
        const clearBtn = document.getElementById('clearDiagnosisBtn');
        const tryAgainBtn = document.getElementById('tryAgainBtn');
        const showAnswerBtn = document.getElementById('showAnswerBtn');
        const diagnosisToggle = document.getElementById('diagnosisToggle');
        
        // Event listeners
        if (diagnosisToggle) {
            diagnosisToggle.addEventListener('click', toggleDiagnosisPanel);
        }
        
        if (submitBtn) {
            submitBtn.addEventListener('click', submitDiagnosis);
        }
        
        if (clearBtn) {
            clearBtn.addEventListener('click', clearDiagnosis);
        }
        
        if (tryAgainBtn) {
            tryAgainBtn.addEventListener('click', resetDiagnosisForm);
        }
        
        if (showAnswerBtn) {
            showAnswerBtn.addEventListener('click', showCorrectAnswer);
        }
        
        // Enable Enter key submission in textarea
        const diagnosisInput = document.getElementById('diagnosisInput');
        if (diagnosisInput) {
            diagnosisInput.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' && e.ctrlKey) {
                    e.preventDefault();
                    submitDiagnosis();
                }
            });
        }
    }

    function toggleDiagnosisPanel() {
        const panel = document.getElementById('diagnosisPanel');
        const container = document.querySelector('.container');
        const toggle = document.getElementById('diagnosisToggle');
        
        if (!panel || !container || !toggle) return;
        
        if (diagnosisPanelVisible) {
            // Hide panel
            panel.style.display = 'none';
            container.classList.remove('with-diagnosis');
            toggle.classList.remove('panel-open');
            toggle.textContent = 'Submit Diagnosis';
            diagnosisPanelVisible = false;
        } else {
            // Show panel
            panel.style.display = 'flex';
            container.classList.add('with-diagnosis');
            toggle.classList.add('panel-open');
            toggle.textContent = 'Hide Panel';
            diagnosisPanelVisible = true;
            
            // Update patient details and reset form
            updatePatientDetailsInDiagnosis();
            resetDiagnosisAttempts();
        }
    }

    async function submitDiagnosis() {
        const diagnosisInput = document.getElementById('diagnosisInput');
        const submitBtn = document.getElementById('submitDiagnosisBtn');
        const buttonText = submitBtn.querySelector('.button-text');
        const buttonSpinner = submitBtn.querySelector('.button-spinner');
        
        if (!diagnosisInput || !submitBtn) return;
        
        const userDiagnosis = diagnosisInput.value.trim();
        
        // Validation
        if (!userDiagnosis) {
            showDiagnosisFeedback('Please enter a diagnosis before submitting.', 'incorrect');
            diagnosisInput.focus();
            return;
        }
        
        if (!currentConversationId) {
            showDiagnosisFeedback('No active conversation. Please start a conversation first.', 'incorrect');
            return;
        }
        
        // Check attempt limit
        if (diagnosisAttemptCount >= maxDiagnosisAttempts) {
            showDiagnosisFeedback('Maximum attempts reached. Please see the correct answer.', 'incorrect');
            return;
        }
        
        // Update UI - loading state
        submitBtn.disabled = true;
        buttonText.textContent = 'Checking...';
        buttonSpinner.style.display = 'inline';
        
        try {
            const response = await fetch('/api/submit-diagnosis', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    conversation_id: currentConversationId,
                    user_diagnosis: userDiagnosis
                })
            });
            
            const result = await response.json();
            
            diagnosisAttemptCount++;
            
            if (response.ok && result.status === 'success') {
                displayDiagnosisResult(result);
            } else {
                showDiagnosisFeedback(result.message || 'Error checking diagnosis', 'incorrect');
            }
        } catch (error) {
            console.error('Error submitting diagnosis:', error);
            showDiagnosisFeedback('Network error. Please try again.', 'incorrect');
        } finally {
            // Reset UI
            submitBtn.disabled = false;
            buttonText.textContent = 'Submit Diagnosis';
            buttonSpinner.style.display = 'none';
        }
    }

    function displayDiagnosisResult(result) {
        const feedbackDiv = document.getElementById('diagnosisFeedback');
        const messageDiv = document.getElementById('feedbackMessage');
        const detailsDiv = document.getElementById('feedbackDetails');
        
        if (!feedbackDiv || !messageDiv || !detailsDiv) return;
        
        // Show feedback section
        feedbackDiv.style.display = 'block';
        
        // Clear previous classes
        feedbackDiv.className = 'diagnosis-feedback';
        
        // Set feedback based on result
        let message = '';
        let details = '';
        
        if (result.is_correct) {
            feedbackDiv.classList.add('correct');
            message = '🎉 Correct! Well done!';
            details = 'You successfully identified the condition.';
            
            // Disable further submissions
            disableDiagnosisInput();
            
        } else if (result.is_close) {
            feedbackDiv.classList.add('close');
            message = '⚠️ Close! You\'re on the right track.';
            details = `Similarity: ${Math.round(result.similarity_score * 100)}%\n${result.feedback || ''}`;
            
        } else {
            feedbackDiv.classList.add('incorrect');
            message = '❌ Not quite right.';
            details = result.feedback || 'Try again or consider other possibilities.';
        }
        
        // Add attempt info
        const remainingAttempts = maxDiagnosisAttempts - diagnosisAttemptCount;
        if (!result.is_correct && remainingAttempts > 0) {
            details += `\n\nAttempts remaining: ${remainingAttempts}`;
        } else if (!result.is_correct && remainingAttempts === 0) {
            details += '\n\nNo more attempts remaining.';
            disableDiagnosisInput();
        }
        
        messageDiv.textContent = message;
        detailsDiv.textContent = details;
        
        // Store the correct diagnosis for potential reveal
        currentPatientDiagnosis = result.correct_diagnosis;
        
        // Update button visibility
        updateFeedbackButtons(result.is_correct, remainingAttempts === 0);
    }

    function showDiagnosisFeedback(message, type) {
        const feedbackDiv = document.getElementById('diagnosisFeedback');
        const messageDiv = document.getElementById('feedbackMessage');
        const detailsDiv = document.getElementById('feedbackDetails');
        
        if (!feedbackDiv || !messageDiv || !detailsDiv) return;
        
        feedbackDiv.style.display = 'block';
        feedbackDiv.className = `diagnosis-feedback ${type}`;
        messageDiv.textContent = message;
        detailsDiv.textContent = '';
        
        // Show only try again button for simple feedback
        updateFeedbackButtons(false, false);
    }

    function updateFeedbackButtons(isCorrect, maxAttemptsReached) {
        const tryAgainBtn = document.getElementById('tryAgainBtn');
        const showAnswerBtn = document.getElementById('showAnswerBtn');
        
        if (!tryAgainBtn || !showAnswerBtn) return;
        
        if (isCorrect) {
            // Hide both buttons if correct
            tryAgainBtn.style.display = 'none';
            showAnswerBtn.style.display = 'none';
        } else if (maxAttemptsReached) {
            // Hide try again, show answer
            tryAgainBtn.style.display = 'none';
            showAnswerBtn.style.display = 'inline-block';
        } else {
            // Show both buttons
            tryAgainBtn.style.display = 'inline-block';
            showAnswerBtn.style.display = 'inline-block';
        }
    }

    function clearDiagnosis() {
        const diagnosisInput = document.getElementById('diagnosisInput');
        const feedbackDiv = document.getElementById('diagnosisFeedback');
        
        if (diagnosisInput) {
            diagnosisInput.value = '';
            diagnosisInput.disabled = false;
        }
        
        if (feedbackDiv) {
            feedbackDiv.style.display = 'none';
        }
        
        // Re-enable submit button
        const submitBtn = document.getElementById('submitDiagnosisBtn');
        if (submitBtn) {
            submitBtn.disabled = false;
        }
    }

    function resetDiagnosisForm() {
        clearDiagnosis();
        const diagnosisInput = document.getElementById('diagnosisInput');
        if (diagnosisInput) {
            diagnosisInput.focus();
        }
    }

    function resetDiagnosisAttempts() {
        diagnosisAttemptCount = 0;
        currentPatientDiagnosis = null;
        clearDiagnosis();
    }

    function resetDiagnosisPanel() {
        // Reset all diagnosis panel state
        diagnosisAttemptCount = 0;
        currentPatientDiagnosis = null;
        
        // Clear the diagnosis input and feedback
        clearDiagnosis();
        
        // Update patient details for the current conversation
        if (currentConversationId) {
            updatePatientDetailsInDiagnosis();
        }
        
        // Note: We don't auto-hide the panel since user might want to keep it open
        
        console.log('Diagnosis panel state reset for new conversation');
    }

    function disableDiagnosisInput() {
        const diagnosisInput = document.getElementById('diagnosisInput');
        const submitBtn = document.getElementById('submitDiagnosisBtn');
        
        if (diagnosisInput) {
            diagnosisInput.disabled = true;
        }
        
        if (submitBtn) {
            submitBtn.disabled = true;
        }
    }

    function showCorrectAnswer() {
        if (currentPatientDiagnosis) {
            const detailsDiv = document.getElementById('feedbackDetails');
            if (detailsDiv) {
                const currentText = detailsDiv.textContent;
                detailsDiv.innerHTML = `${currentText}<br><br><strong>Correct Answer:</strong> ${currentPatientDiagnosis}`;
            }
            
            // Hide the show answer button
            const showAnswerBtn = document.getElementById('showAnswerBtn');
            if (showAnswerBtn) {
                showAnswerBtn.style.display = 'none';
            }
        }
    }

    function updatePatientDetailsInDiagnosis() {
        const summaryDiv = document.getElementById('patientSummary');
        if (!summaryDiv) return;
        
        // Clear existing content
        summaryDiv.innerHTML = '';
        
        // Check if we have an active conversation with patient data
        if (currentConversationId) {
            // Try to get current patient details from the main panel
            const mainPatientPanel = document.querySelector('.patient-details-panel');
            
            if (mainPatientPanel && mainPatientPanel.innerHTML.trim() !== '') {
                // Clone the content but exclude any illness/diagnosis information
                const clonedContent = mainPatientPanel.cloneNode(true);
                
                // Remove any elements that might contain diagnosis info
                const diagnosisElements = clonedContent.querySelectorAll('*');
                diagnosisElements.forEach(el => {
                    const text = el.textContent.toLowerCase();
                    if (text.includes('illness') || text.includes('diagnosis') || text.includes('condition')) {
                        // Don't include diagnosis-related info
                        if (el.parentNode) {
                            el.parentNode.removeChild(el);
                        }
                    }
                });
                
                summaryDiv.appendChild(clonedContent);
            } else {
                // Fallback: show basic info if available
                summaryDiv.innerHTML = '<p>Patient simulation active - details available during conversation</p>';
            }
        } else {
            summaryDiv.innerHTML = '<p>No patient simulation active</p>';
        }
    }

    // Initialize the diagnosis panel functionality
    initializeDiagnosisPanel();

    // ========== CUSTOM PATIENT FORM FUNCTIONS ==========
    
    function showCustomPatientForm() {
        if (customPatientForm) {
            customPatientForm.style.display = 'block';
            customPatientForm.classList.add('show');
            clearCustomPatientForm(); // Start with a clean form
        }
    }
    
    function hideCustomPatientForm() {
        if (customPatientForm) {
            customPatientForm.style.display = 'none';
            customPatientForm.classList.remove('show');
            clearAllErrorMessages();
        }
    }

    // ========== WIZARD FUNCTIONS ==========
    
    function showPatientWizard() {
        const wizardModal = document.getElementById('patientCaseWizard');
        if (wizardModal) {
            // Reset wizard state
            resetWizardState();
            
            // Show modal with animation
            wizardModal.style.display = 'flex';
            document.body.style.overflow = 'hidden'; // Prevent background scrolling
            
            // Populate specialty options
            populateWizardSpecialtySelector();
            
            // Initialize first step
            updateWizardStep();
            
            console.log('Patient wizard opened');
        }
    }
    
    function hidePatientWizard() {
        const wizardModal = document.getElementById('patientCaseWizard');
        if (wizardModal) {
            wizardModal.style.display = 'none';
            document.body.style.overflow = ''; // Restore scrolling
            
            // Reset simulation selection
            simulationSelect.value = '';
            
            console.log('Patient wizard closed');
        }
    }
    
    function resetWizardState() {
        wizardState = {
            currentStep: 1,
            totalSteps: 4,
            formData: {},
            selectedSpecialty: null,
            selectedSymptoms: []
        };
        
        // Clear all form fields
        const wizardForm = document.getElementById('wizardForm');
        if (wizardForm) {
            wizardForm.reset();
        }
        
        // Clear error messages
        clearAllWizardErrors();
        
        // Hide loading state
        const loadingDiv = document.getElementById('wizardLoading');
        if (loadingDiv) {
            loadingDiv.style.display = 'none';
        }
    }
    
    function updateWizardStep() {
        const steps = document.querySelectorAll('.wizard-step');
        const progressFill = document.getElementById('wizardProgress');
        const stepText = document.getElementById('currentStepText');
        const backBtn = document.getElementById('wizardBackBtn');
        const nextBtn = document.getElementById('wizardNextBtn');
        const generateBtn = document.getElementById('wizardGenerateBtn');
        
        // Update step visibility
        steps.forEach((step, index) => {
            step.classList.toggle('active', index + 1 === wizardState.currentStep);
        });
        
        // Update progress bar
        const progressPercent = (wizardState.currentStep / wizardState.totalSteps) * 100;
        if (progressFill) {
            progressFill.style.width = progressPercent + '%';
        }
        
        // Update step text
        const stepTitles = [
            'Patient Demographics',
            'Medical Specialty',
            'Presenting Symptoms',
            'Case Parameters'
        ];
        
        if (stepText) {
            stepText.textContent = `Step ${wizardState.currentStep} of ${wizardState.totalSteps}: ${stepTitles[wizardState.currentStep - 1]}`;
        }
        
        // Update navigation buttons
        if (backBtn) {
            backBtn.disabled = wizardState.currentStep === 1;
        }
        
        if (nextBtn && generateBtn) {
            if (wizardState.currentStep === wizardState.totalSteps) {
                nextBtn.style.display = 'none';
                generateBtn.style.display = 'inline-block';
            } else {
                nextBtn.style.display = 'inline-block';
                generateBtn.style.display = 'none';
            }
        }
        
        // Update case preview if on last step
        if (wizardState.currentStep === wizardState.totalSteps) {
            updateCasePreview();
        }
    }
    
    function nextWizardStep() {
        // Validate current step
        if (!validateWizardStep(wizardState.currentStep)) {
            return false;
        }
        
        // Save current step data
        saveCurrentStepData();
        
        // Move to next step
        if (wizardState.currentStep < wizardState.totalSteps) {
            wizardState.currentStep++;
            updateWizardStep();
            
            // Handle specialty change for symptoms step
            if (wizardState.currentStep === 3) {
                handleWizardSpecialtyChange();
            }
        }
        
        return true;
    }
    
    function previousWizardStep() {
        if (wizardState.currentStep > 1) {
            wizardState.currentStep--;
            updateWizardStep();
        }
    }
    
    function validateWizardStep(stepNumber) {
        clearAllWizardErrors();
        let isValid = true;
        
        switch (stepNumber) {
            case 1: // Demographics
                isValid = validateWizardDemographics();
                break;
            case 2: // Specialty
                isValid = validateWizardSpecialty();
                break;
            case 3: // Symptoms
                isValid = validateWizardSymptoms();
                break;
            case 4: // Parameters
                isValid = validateWizardParameters();
                break;
        }
        
        return isValid;
    }
    
    function validateWizardDemographics() {
        let isValid = true;
        
        const age = document.getElementById('wizardAge').value;
        const gender = document.getElementById('wizardGender').value;
        const occupation = document.getElementById('wizardOccupation').value;
        
        if (!age || age < 1 || age > 120) {
            showWizardFieldError('wizardAgeError', 'Age must be between 1 and 120');
            isValid = false;
        }
        
        if (!gender) {
            showWizardFieldError('wizardGenderError', 'Gender selection is required');
            isValid = false;
        }
        
        if (!occupation || occupation.trim().length < 2) {
            showWizardFieldError('wizardOccupationError', 'Occupation is required (at least 2 characters)');
            isValid = false;
        }
        
        return isValid;
    }
    
    function validateWizardSpecialty() {
        const specialty = document.getElementById('wizardSpecialty').value;
        
        if (!specialty) {
            showWizardFieldError('wizardSpecialtyError', 'Medical specialty selection is required');
            return false;
        }
        
        wizardState.selectedSpecialty = specialty;
        return true;
    }
    
    function validateWizardSymptoms() {
        if (wizardState.selectedSymptoms.length === 0) {
            showWizardFieldError('wizardSymptomsError', 'At least one symptom must be selected');
            return false;
        }
        
        return true;
    }
    
    function validateWizardParameters() {
        const severity = document.getElementById('wizardSeverity').value;
        
        if (!severity) {
            showWizardFieldError('wizardSeverityError', 'Symptom severity selection is required');
            return false;
        }
        
        return true;
    }
    
    function saveCurrentStepData() {
        switch (wizardState.currentStep) {
            case 1:
                wizardState.formData.age = document.getElementById('wizardAge').value;
                wizardState.formData.gender = document.getElementById('wizardGender').value;
                wizardState.formData.occupation = document.getElementById('wizardOccupation').value;
                wizardState.formData.medical_history = document.getElementById('wizardMedicalHistory').value;
                break;
            case 2:
                wizardState.formData.specialty = document.getElementById('wizardSpecialty').value;
                wizardState.selectedSpecialty = wizardState.formData.specialty;
                break;
            case 3:
                wizardState.formData.symptoms = [...wizardState.selectedSymptoms];
                break;
            case 4:
                wizardState.formData.severity = document.getElementById('wizardSeverity').value;
                break;
        }
    }
    
    function updateCasePreview() {
        const previewContainer = document.getElementById('casePreviewContent');
        if (!previewContainer) return;
        
        const previewData = [
            { label: 'Age', value: wizardState.formData.age || '-' },
            { label: 'Gender', value: wizardState.formData.gender || '-' },
            { label: 'Occupation', value: wizardState.formData.occupation || '-' },
            { label: 'Specialty', value: getSpecialtyDisplayName(wizardState.formData.specialty) || '-' },
            { label: 'Symptoms', value: getSelectedSymptomsDisplay() || '-' },
            { label: 'Severity', value: wizardState.formData.severity || '-' }
        ];
        
        if (previewData.every(item => item.value !== '-')) {
            previewContainer.innerHTML = previewData.map(item => 
                `<div class="case-preview-item">
                    <span class="preview-label">${item.label}:</span>
                    <span class="preview-value">${item.value}</span>
                </div>`
            ).join('');
        } else {
            previewContainer.innerHTML = '<p class="preview-placeholder">Complete all steps to see a preview of your case</p>';
        }
    }
    
    function getSpecialtyDisplayName(specialtyKey) {
        if (!specialtyKey || !medicalKnowledge.specialties[specialtyKey]) {
            return specialtyKey;
        }
        return medicalKnowledge.specialties[specialtyKey].name || specialtyKey;
    }
    
    function getSelectedSymptomsDisplay() {
        if (wizardState.selectedSymptoms.length === 0) {
            return '';
        }
        
        return wizardState.selectedSymptoms.map(symptomKey => 
            medicalKnowledge.all_symptoms[symptomKey] || symptomKey
        ).join(', ');
    }
    
    function populateWizardSpecialtySelector() {
        const specialtySelect = document.getElementById('wizardSpecialty');
        if (!specialtySelect || !medicalKnowledge.specialties) return;

        // Clear existing options (except the first one)
        while (specialtySelect.options.length > 1) {
            specialtySelect.removeChild(specialtySelect.lastChild);
        }

        // Add specialty options
        Object.entries(medicalKnowledge.specialties).forEach(([key, specialty]) => {
            const option = document.createElement('option');
            option.value = key;
            option.textContent = specialty.name;
            option.dataset.description = specialty.description;
            specialtySelect.appendChild(option);
        });
    }
    
    function handleWizardSpecialtyChange() {
        const specialtySelect = document.getElementById('wizardSpecialty');
        const selectedKey = specialtySelect?.value || wizardState.selectedSpecialty;
        
        if (selectedKey && medicalKnowledge.specialties[selectedKey]) {
            const specialty = medicalKnowledge.specialties[selectedKey];
            
            // Show specialty description
            const descriptionDiv = document.getElementById('wizardSpecialtyDescription');
            if (descriptionDiv) {
                descriptionDiv.textContent = specialty.description || specialty.name;
                descriptionDiv.style.display = 'block';
            }
            
            // Populate symptoms for this specialty if we're on the symptoms step
            if (wizardState.currentStep === 3) {
                populateWizardSymptoms(specialty.symptoms);
            }
        }
    }
    
    function populateWizardSymptoms(symptomKeys) {
        const container = document.getElementById('wizardSymptomsContainer');
        const instructionsDiv = document.getElementById('wizardSymptomsInstructions');
        
        if (!container) return;

        // Clear existing symptoms
        wizardState.selectedSymptoms = [];
        
        if (!symptomKeys || symptomKeys.length === 0) {
            container.style.display = 'none';
            if (instructionsDiv) {
                instructionsDiv.textContent = 'No symptoms available for this specialty';
            }
            return;
        }

        // Show container and update instructions
        container.style.display = 'block';
        if (instructionsDiv) {
            instructionsDiv.textContent = 'Select one or more symptoms that the patient will present with:';
        }

        // Create symptom checkboxes
        container.innerHTML = symptomKeys.map(symptomKey => {
            const symptomName = medicalKnowledge.all_symptoms[symptomKey] || symptomKey;
            return `
                <div class="symptom-checkbox">
                    <input type="checkbox" 
                           id="wizardSymptom_${symptomKey}" 
                           value="${symptomKey}"
                           onchange="handleWizardSymptomChange(this)">
                    <label for="wizardSymptom_${symptomKey}">${symptomName}</label>
                </div>
            `;
        }).join('');
    }
    
    function handleWizardSymptomChange(checkbox) {
        const symptomKey = checkbox.value;
        
        if (checkbox.checked) {
            if (!wizardState.selectedSymptoms.includes(symptomKey)) {
                wizardState.selectedSymptoms.push(symptomKey);
            }
        } else {
            wizardState.selectedSymptoms = wizardState.selectedSymptoms.filter(s => s !== symptomKey);
        }
        
        // Clear symptoms validation error if at least one selected
        if (wizardState.selectedSymptoms.length > 0) {
            clearWizardFieldError('wizardSymptomsError');
        }
        
        console.log('Selected symptoms:', wizardState.selectedSymptoms);
    }
    
    function showWizardFieldError(elementId, message) {
        const errorElement = document.getElementById(elementId);
        if (errorElement) {
            errorElement.textContent = message;
            errorElement.style.display = 'block';
        }
    }
    
    function clearWizardFieldError(elementId) {
        const errorElement = document.getElementById(elementId);
        if (errorElement) {
            errorElement.textContent = '';
            errorElement.style.display = 'none';
        }
    }
    
    function clearAllWizardErrors() {
        const errorElements = document.querySelectorAll('#patientCaseWizard .error-message');
        errorElements.forEach(element => {
            element.textContent = '';
            element.style.display = 'none';
        });
    }
    
    async function generatePatientCaseFromWizard() {
        // Final validation
        if (!validateWizardStep(wizardState.currentStep)) {
            return;
        }
        
        // Save final step data
        saveCurrentStepData();
        
        // Show loading state
        const loadingDiv = document.getElementById('wizardLoading');
        const generateBtn = document.getElementById('wizardGenerateBtn');
        const buttonText = generateBtn?.querySelector('.button-text');
        const buttonSpinner = generateBtn?.querySelector('.button-spinner');
        
        if (loadingDiv) loadingDiv.style.display = 'flex';
        if (generateBtn) generateBtn.disabled = true;
        if (buttonText) buttonText.style.display = 'none';
        if (buttonSpinner) buttonSpinner.style.display = 'inline';
        
        try {
            // Prepare data for backend
            const caseData = {
                type: 'ai_generated',
                case_parameters: {
                    age: parseInt(wizardState.formData.age),
                    gender: wizardState.formData.gender,
                    occupation: wizardState.formData.occupation,
                    medical_history: wizardState.formData.medical_history || '',
                    specialty: wizardState.formData.specialty,
                    symptoms: wizardState.formData.symptoms,
                    severity: wizardState.formData.severity
                }
            };
            
            console.log('Generating AI patient case with data:', caseData);
            
            // Call the backend API
            const response = await fetch('/api/generate-patient-case', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(caseData)
            });
            
            const result = await response.json();
            
            if (result.status === 'success') {
                // Success! Close wizard and update UI
                hidePatientWizard();
                
                // Update global state
                currentConversationId = result.conversation_id;
                currentSimulation = '__custom__';
                
                // Update voice preference
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
                
                // Display patient details
                if (result.patient_details) {
                    displayPatientDetails(result.patient_details);
                }
                
                // Clear conversation display for new conversation
                conversationElement.innerHTML = '';
                
                // Reset diagnosis panel for new AI patient case
                resetDiagnosisPanel();
                
                // Refresh conversation list
                await loadConversationHistory();
                
                updateStatus('AI patient case generated successfully!');
                
            } else {
                throw new Error(result.message || 'Failed to generate patient case');
            }
            
        } catch (error) {
            console.error('Error generating patient case:', error);
            updateStatus('Error generating patient case');
            
            // Show error message in wizard
            alert('Error generating patient case: ' + error.message);
            
        } finally {
            // Hide loading state
            if (loadingDiv) loadingDiv.style.display = 'none';
            if (generateBtn) generateBtn.disabled = false;
            if (buttonText) buttonText.style.display = 'inline';
            if (buttonSpinner) buttonSpinner.style.display = 'none';
        }
    }

    // ========== END WIZARD FUNCTIONS ==========

    // Make wizard functions globally accessible for dynamic HTML
    window.handleWizardSymptomChange = function(checkbox) {
        const symptomKey = checkbox.value;
        
        if (checkbox.checked) {
            if (!wizardState.selectedSymptoms.includes(symptomKey)) {
                wizardState.selectedSymptoms.push(symptomKey);
            }
        } else {
            wizardState.selectedSymptoms = wizardState.selectedSymptoms.filter(s => s !== symptomKey);
        }
        
        // Clear symptoms validation error if at least one selected
        if (wizardState.selectedSymptoms.length > 0) {
            clearWizardFieldError('wizardSymptomsError');
        }
        
        console.log('Selected symptoms:', wizardState.selectedSymptoms);
    };
}); 