import pytest
from app import app
import json
import base64
from unittest.mock import patch, MagicMock

@pytest.fixture
def client():
    """Create a test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_complete_conversation_flow(client, mock_audio_file):
    """Test the complete conversation flow from audio input to audio output"""
    with patch('utils.groq_transcribe.groq') as mock_transcribe, \
         patch('utils.groq_integration.groq') as mock_llm, \
         patch('utils.groq_tts_speech.groq') as mock_tts:
        
        # Mock transcription response
        mock_transcribe_response = MagicMock()
        mock_transcribe_response.text = "Hello, I have a headache"
        mock_transcribe.return_value.audio.transcriptions.create.return_value = mock_transcribe_response

        # Mock LLM response
        mock_llm_response = MagicMock()
        mock_llm_response.choices = [MagicMock(message=MagicMock(content="I understand you have a headache. Can you tell me more about it?"))]
        mock_llm.return_value.chat.completions.create.return_value = mock_llm_response

        # Mock TTS response
        mock_tts_response = MagicMock()
        mock_tts_response.audio = b'test audio response'
        mock_tts.return_value.audio.speech.create.return_value = mock_tts_response

        # Read the mock audio file
        with open(mock_audio_file, 'rb') as f:
            audio_data = f.read()

        # Send POST request to process audio
        response = client.post(
            '/process_audio',
            data={'audio': (audio_data, 'test.wav')},
            content_type='multipart/form-data'
        )

        # Check response
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert data['user_transcription'] == "Hello, I have a headache"
        assert data['assistant_response_text'] == "I understand you have a headache. Can you tell me more about it?"
        assert data['assistant_response_audio'] == base64.b64encode(b'test audio response').decode('utf-8')

def test_conversation_flow_with_patient_simulation(client, mock_audio_file, test_patient_data):
    """Test conversation flow with patient simulation context"""
    with patch('utils.groq_transcribe.groq') as mock_transcribe, \
         patch('utils.groq_integration.groq') as mock_llm, \
         patch('utils.groq_tts_speech.groq') as mock_tts, \
         patch('utils.patient_simulation.load_patient_simulation') as mock_load_patient:
        
        # Mock patient simulation
        mock_load_patient.return_value = test_patient_data

        # Mock transcription response
        mock_transcribe_response = MagicMock()
        mock_transcribe_response.text = "What are my symptoms?"
        mock_transcribe.return_value.audio.transcriptions.create.return_value = mock_transcribe_response

        # Mock LLM response
        mock_llm_response = MagicMock()
        mock_llm_response.choices = [MagicMock(message=MagicMock(content="Based on your records, you have reported headache and fever."))]
        mock_llm.return_value.chat.completions.create.return_value = mock_llm_response

        # Mock TTS response
        mock_tts_response = MagicMock()
        mock_tts_response.audio = b'test audio response'
        mock_tts.return_value.audio.speech.create.return_value = mock_tts_response

        # Read the mock audio file
        with open(mock_audio_file, 'rb') as f:
            audio_data = f.read()

        # Send POST request to process audio
        response = client.post(
            '/process_audio',
            data={'audio': (audio_data, 'test.wav')},
            content_type='multipart/form-data'
        )

        # Check response
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert data['user_transcription'] == "What are my symptoms?"
        assert "headache" in data['assistant_response_text'].lower()
        assert "fever" in data['assistant_response_text'].lower() 