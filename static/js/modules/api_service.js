// API Service Module - Handles all server communication
export class ApiService {
    constructor() {
        this.baseUrl = '';
    }

    async makeRequest(url, options = {}) {
        try {
            const response = await fetch(url, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error(`API request failed for ${url}:`, error);
            throw error;
        }
    }

    async processAudio(audioBlob, voiceId) {
        if (!audioBlob) {
            throw new Error('Audio blob is required');
        }

        if (!voiceId) {
            throw new Error('Voice ID is required');
        }

        try {
            const formData = new FormData();
            formData.append('audio', audioBlob);
            formData.append('voice_id', voiceId);

            console.log(`Sending audio to server with voice_id: ${voiceId}`);
            
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
                has_audio: !!data.assistant_response_audio
            });

            return data;
        } catch (error) {
            console.error('Error processing audio:', error);
            throw error;
        }
    }

    async getSimulations() {
        try {
            return await this.makeRequest('/api/patient-simulations');
        } catch (error) {
            console.error('Error loading simulations:', error);
            throw error;
        }
    }

    async selectSimulation(simulationFile) {
        if (typeof simulationFile !== 'string') {
            throw new Error('Simulation file must be a string');
        }

        try {
            return await this.makeRequest('/api/select-simulation', {
                method: 'POST',
                body: JSON.stringify({ simulation_file: simulationFile })
            });
        } catch (error) {
            console.error('Error selecting simulation:', error);
            throw error;
        }
    }

    async updateVoice(voiceId, conversationId = null) {
        if (!voiceId) {
            throw new Error('Voice ID is required');
        }

        try {
            const body = { voice_id: voiceId };
            if (conversationId) {
                body.conversation_id = conversationId;
            }

            return await this.makeRequest('/api/update-voice', {
                method: 'POST',
                body: JSON.stringify(body)
            });
        } catch (error) {
            console.error('Error updating voice:', error);
            throw error;
        }
    }

    async createNewConversation() {
        try {
            return await this.makeRequest('/api/conversations/new', {
                method: 'POST'
            });
        } catch (error) {
            console.error('Error creating new conversation:', error);
            throw error;
        }
    }

    async getConversations() {
        try {
            return await this.makeRequest('/api/conversations');
        } catch (error) {
            console.error('Error getting conversations:', error);
            throw error;
        }
    }

    async getConversation(conversationId) {
        if (!conversationId) {
            throw new Error('Conversation ID is required');
        }

        try {
            return await this.makeRequest(`/api/conversations/${conversationId}`);
        } catch (error) {
            console.error(`Error getting conversation ${conversationId}:`, error);
            throw error;
        }
    }

    async loadConversation(conversationId) {
        if (!conversationId) {
            throw new Error('Conversation ID is required');
        }

        try {
            return await this.makeRequest(`/api/conversations/${conversationId}/load`, {
                method: 'POST'
            });
        } catch (error) {
            console.error(`Error loading conversation ${conversationId}:`, error);
            throw error;
        }
    }

    async deleteConversation(conversationId) {
        if (!conversationId) {
            throw new Error('Conversation ID is required');
        }

        try {
            return await this.makeRequest(`/api/conversations/${conversationId}`, {
                method: 'DELETE'
            });
        } catch (error) {
            console.error(`Error deleting conversation ${conversationId}:`, error);
            throw error;
        }
    }

    async getCurrentPatientDetails() {
        try {
            return await this.makeRequest('/api/current-patient-details');
        } catch (error) {
            console.error('Error getting patient details:', error);
            throw error;
        }
    }

    async getDiagnostics() {
        try {
            return await this.makeRequest('/api/diagnose');
        } catch (error) {
            console.error('Error getting diagnostics:', error);
            throw error;
        }
    }
} 