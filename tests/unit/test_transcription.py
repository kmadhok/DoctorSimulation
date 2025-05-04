import pytest
from utils.groq_transcribe import transcribe_audio_data
from unittest.mock import patch, MagicMock

def test_transcribe_audio_data_success(mock_audio_file):
    """Test successful audio transcription"""
    with patch('utils.groq_transcribe.groq') as mock_groq:
        # Mock the Groq response
        mock_response = MagicMock()
        mock_response.text = "This is a test transcription"
        mock_groq.return_value.audio.transcriptions.create.return_value = mock_response

        # Read the mock audio file
        with open(mock_audio_file, 'rb') as f:
            audio_bytes = f.read()

        # Test transcription
        result = transcribe_audio_data(audio_bytes)
        assert result == "This is a test transcription"
        mock_groq.return_value.audio.transcriptions.create.assert_called_once()

def test_transcribe_audio_data_empty():
    """Test transcription with empty audio data"""
    result = transcribe_audio_data(b'')
    assert result is None

def test_transcribe_audio_data_error(mock_audio_file):
    """Test transcription with API error"""
    with patch('utils.groq_transcribe.groq') as mock_groq:
        # Mock API error
        mock_groq.return_value.audio.transcriptions.create.side_effect = Exception("API Error")

        # Read the mock audio file
        with open(mock_audio_file, 'rb') as f:
            audio_bytes = f.read()

        # Test transcription
        result = transcribe_audio_data(audio_bytes)
        assert result is None 