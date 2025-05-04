import pytest
from utils.groq_tts_speech import generate_speech_audio
from unittest.mock import patch, MagicMock

def test_generate_speech_audio_success():
    """Test successful speech audio generation"""
    with patch('utils.groq_tts_speech.groq') as mock_groq:
        # Mock the Groq response
        mock_response = MagicMock()
        mock_response.audio = b'test audio data'
        mock_groq.return_value.audio.speech.create.return_value = mock_response

        # Test speech generation
        result = generate_speech_audio("Hello, this is a test.")
        assert result == b'test audio data'
        mock_groq.return_value.audio.speech.create.assert_called_once()

def test_generate_speech_audio_empty():
    """Test speech generation with empty text"""
    result = generate_speech_audio("")
    assert result is None

def test_generate_speech_audio_error():
    """Test speech generation with API error"""
    with patch('utils.groq_tts_speech.groq') as mock_groq:
        # Mock API error
        mock_groq.return_value.audio.speech.create.side_effect = Exception("API Error")

        # Test speech generation
        result = generate_speech_audio("Hello, this is a test.")
        assert result is None

def test_generate_speech_audio_long_text():
    """Test speech generation with long text"""
    with patch('utils.groq_tts_speech.groq') as mock_groq:
        # Mock the Groq response
        mock_response = MagicMock()
        mock_response.audio = b'test audio data'
        mock_groq.return_value.audio.speech.create.return_value = mock_response

        # Test with long text
        long_text = "This is a very long text that should be split into multiple chunks for processing. " * 10
        result = generate_speech_audio(long_text)
        assert result == b'test audio data'
        assert mock_groq.return_value.audio.speech.create.call_count > 1 