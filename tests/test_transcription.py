import pytest
from unittest.mock import patch, MagicMock
import os
import tempfile
from utils.groq_transcribe import transcribe_audio_data, save_audio_bytes_to_temp_file

@pytest.fixture
def mock_audio_data():
    """Fixture for mock audio data"""
    return b"fake_audio_data"

@pytest.fixture
def mock_transcription_response():
    """Fixture for mock transcription response"""
    return {
        'text': 'Test transcription'
    }

def test_audio_transcription(mock_audio_data, mock_transcription_response):
    """Test successful audio transcription"""
    with patch('utils.groq_transcribe.requests.post') as mock_post:
        # Configure mock
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = mock_transcription_response
        
        # Test transcription
        transcription = transcribe_audio_data(mock_audio_data)
        
        # Verify transcription
        assert transcription == "Test transcription"
        mock_post.assert_called_once()

def test_transcription_error_handling(mock_audio_data):
    """Test transcription error handling"""
    with patch('utils.groq_transcribe.requests.post') as mock_post:
        # Configure mock for error
        mock_post.return_value.status_code = 500
        mock_post.return_value.text = "API Error"
        
        # Test error handling
        transcription = transcribe_audio_data(mock_audio_data)
        
        # Verify error handling
        assert transcription == ""
        mock_post.assert_called_once()

def test_transcription_network_error(mock_audio_data):
    """Test network error handling"""
    with patch('utils.groq_transcribe.requests.post') as mock_post:
        # Configure mock for network error
        mock_post.side_effect = Exception("Network error")
        
        # Test network error handling
        transcription = transcribe_audio_data(mock_audio_data)
        
        # Verify error handling
        assert transcription == ""
        mock_post.assert_called_once()

def test_transcription_missing_api_key(mock_audio_data):
    """Test handling of missing API key"""
    # Save original API key
    original_key = os.environ.get('GROQ_API_KEY')
    
    try:
        # Remove API key
        if 'GROQ_API_KEY' in os.environ:
            del os.environ['GROQ_API_KEY']
        
        # Test missing API key handling
        transcription = transcribe_audio_data(mock_audio_data)
        
        # Verify error handling
        assert transcription == ""
        
    finally:
        # Restore original API key
        if original_key:
            os.environ['GROQ_API_KEY'] = original_key

def test_save_audio_bytes_to_temp_file(mock_audio_data):
    """Test saving audio bytes to temporary file"""
    # Test file saving
    temp_file_path = save_audio_bytes_to_temp_file(mock_audio_data)
    
    try:
        # Verify file exists
        assert os.path.exists(temp_file_path)
        
        # Verify file contents
        with open(temp_file_path, 'rb') as f:
            saved_data = f.read()
        assert saved_data == mock_audio_data
        
    finally:
        # Clean up
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

def test_transcription_with_different_models(mock_audio_data, mock_transcription_response):
    """Test transcription with different model options"""
    models = [
        "whisper-large-v3-turbo",
        "distil-whisper-large-v3-en",
        "whisper-large-v3"
    ]
    
    for model in models:
        with patch('utils.groq_transcribe.requests.post') as mock_post:
            # Configure mock
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = mock_transcription_response
            
            # Test transcription with model
            transcription = transcribe_audio_data(mock_audio_data, model=model)
            
            # Verify transcription
            assert transcription == "Test transcription"
            
            # Verify model was used
            call_args = mock_post.call_args[1]['files']
            assert call_args['model'] == (None, model) 