import pytest
from unittest.mock import patch, MagicMock
import os
from utils.groq_tts_speech import generate_speech_audio

@pytest.fixture
def mock_audio_response():
    """Fixture for mock audio response"""
    return b"fake_audio_data"

@pytest.fixture
def mock_error_response():
    """Fixture for mock error response"""
    return {
        'error': {
            'message': 'API Error'
        }
    }

def test_speech_generation(mock_audio_response):
    """Test successful text-to-speech generation"""
    with patch('utils.groq_tts_speech.requests.post') as mock_post:
        # Configure mock
        mock_post.return_value.status_code = 200
        mock_post.return_value.content = mock_audio_response
        
        # Test speech generation
        audio_data = generate_speech_audio("Test text")
        
        # Verify response
        assert audio_data == mock_audio_response
        mock_post.assert_called_once()

def test_speech_generation_with_voice(mock_audio_response):
    """Test text-to-speech generation with specific voice"""
    voice_id = "custom-voice"
    
    with patch('utils.groq_tts_speech.requests.post') as mock_post:
        # Configure mock
        mock_post.return_value.status_code = 200
        mock_post.return_value.content = mock_audio_response
        
        # Test speech generation with voice
        audio_data = generate_speech_audio("Test text", voice_id=voice_id)
        
        # Verify response and request
        assert audio_data == mock_audio_response
        mock_post.assert_called_once()
        
        # Verify voice was used
        call_args = mock_post.call_args[1]['json']
        assert call_args['voice'] == voice_id

def test_tts_error_handling(mock_error_response):
    """Test error handling in text-to-speech generation"""
    with patch('utils.groq_tts_speech.requests.post') as mock_post:
        # Configure mock for error
        mock_post.return_value.status_code = 500
        mock_post.return_value.json.return_value = mock_error_response
        
        # Test error handling
        audio_data = generate_speech_audio("Test text")
        
        # Verify error handling
        assert audio_data is None
        mock_post.assert_called_once()

def test_tts_network_error():
    """Test network error handling"""
    with patch('utils.groq_tts_speech.requests.post') as mock_post:
        # Configure mock for network error
        mock_post.side_effect = Exception("Network error")
        
        # Test network error handling
        audio_data = generate_speech_audio("Test text")
        
        # Verify error handling
        assert audio_data is None
        mock_post.assert_called_once()

def test_tts_missing_api_key():
    """Test handling of missing API key"""
    # Save original API key
    original_key = os.environ.get('GROQ_API_KEY')
    
    try:
        # Remove API key
        if 'GROQ_API_KEY' in os.environ:
            del os.environ['GROQ_API_KEY']
        
        # Test missing API key handling
        audio_data = generate_speech_audio("Test text")
        
        # Verify error handling
        assert audio_data is None
        
    finally:
        # Restore original API key
        if original_key:
            os.environ['GROQ_API_KEY'] = original_key

def test_tts_empty_text():
    """Test handling of empty text input"""
    with patch('utils.groq_tts_speech.requests.post') as mock_post:
        # Test empty text handling
        audio_data = generate_speech_audio("")
        
        # Verify empty text handling
        assert audio_data is None
        mock_post.assert_not_called()

def test_tts_long_text(mock_audio_response):
    """Test handling of long text input"""
    long_text = "Test text " * 1000  # Create a long text
    
    with patch('utils.groq_tts_speech.requests.post') as mock_post:
        # Configure mock
        mock_post.return_value.status_code = 200
        mock_post.return_value.content = mock_audio_response
        
        # Test long text handling
        audio_data = generate_speech_audio(long_text)
        
        # Verify long text handling
        assert audio_data == mock_audio_response
        mock_post.assert_called_once()
        
        # Verify text was sent correctly
        call_args = mock_post.call_args[1]['json']
        assert call_args['input'] == long_text 