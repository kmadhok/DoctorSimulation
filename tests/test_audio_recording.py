import os
import pytest
from flask import Flask
import json
import base64
from unittest.mock import patch, MagicMock
import tempfile

# Import the app
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app

@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_audio_recording_endpoint_exists(client):
    """Test that the audio recording endpoint exists and accepts POST requests"""
    response = client.post('/process_audio')
    assert response.status_code != 404  # Endpoint should exist
    assert response.status_code == 400  # Should return 400 without audio file

def test_audio_recording_without_file(client):
    """Test that the endpoint properly handles requests without audio files"""
    response = client.post('/process_audio')
    data = json.loads(response.data)
    assert response.status_code == 400
    assert data['status'] == 'error'
    assert 'No audio file provided' in data['message']

@patch('app.transcribe_audio_data')
@patch('app.get_groq_response')
@patch('app.generate_speech_audio')
def test_audio_recording_successful_flow(mock_generate_speech, mock_groq_response, mock_transcribe, client):
    """Test the complete successful flow of audio recording, transcription, and response"""
    # Mock the transcription response
    mock_transcribe.return_value = "Hello, this is a test"
    
    # Mock the Groq response
    mock_groq_response.return_value = "This is a test response"
    
    # Mock the speech generation
    mock_generate_speech.return_value = b"fake_audio_data"
    
    # Create a temporary audio file
    with tempfile.NamedTemporaryFile(suffix='.wav') as audio_file:
        audio_file.write(b"fake_audio_data")
        audio_file.seek(0)
        
        # Send the request
        response = client.post('/process_audio', 
                             data={'audio': (audio_file, 'test.wav')},
                             content_type='multipart/form-data')
    
    # Parse the response
    data = json.loads(response.data)
    
    # Verify the response
    assert response.status_code == 200
    assert data['status'] == 'success'
    assert data['user_transcription'] == "Hello, this is a test"
    assert data['assistant_response_text'] == "This is a test response"
    assert data['assistant_response_audio'] == base64.b64encode(b"fake_audio_data").decode('utf-8')

@patch('app.transcribe_audio_data')
def test_audio_recording_transcription_failure(mock_transcribe, client):
    """Test handling of transcription failure"""
    # Mock transcription failure
    mock_transcribe.return_value = None
    
    # Create a temporary audio file
    with tempfile.NamedTemporaryFile(suffix='.wav') as audio_file:
        audio_file.write(b"fake_audio_data")
        audio_file.seek(0)
        
        # Send the request
        response = client.post('/process_audio', 
                             data={'audio': (audio_file, 'test.wav')},
                             content_type='multipart/form-data')
    
    # Parse the response
    data = json.loads(response.data)
    
    # Verify the response
    assert response.status_code == 500
    assert data['status'] == 'error'
    assert 'Failed to transcribe audio' in data['message']

@patch('app.transcribe_audio_data')
def test_audio_recording_exit_command(mock_transcribe, client):
    """Test handling of exit command in transcription"""
    # Mock transcription with exit command
    mock_transcribe.return_value = "exit"
    
    # Create a temporary audio file
    with tempfile.NamedTemporaryFile(suffix='.wav') as audio_file:
        audio_file.write(b"fake_audio_data")
        audio_file.seek(0)
        
        # Send the request
        response = client.post('/process_audio', 
                             data={'audio': (audio_file, 'test.wav')},
                             content_type='multipart/form-data')
    
    # Parse the response
    data = json.loads(response.data)
    
    # Verify the response
    assert response.status_code == 200
    assert data['status'] == 'exit'
    assert data['assistant_response_text'] == 'Ending conversation. Goodbye!'
    assert data['assistant_response_audio'] == ''

def test_audio_recording_invalid_file_type(client):
    """Test handling of invalid file types"""
    # Create a temporary text file
    with tempfile.NamedTemporaryFile(suffix='.txt') as text_file:
        text_file.write(b"not audio data")
        text_file.seek(0)
        
        # Send the request
        response = client.post('/process_audio', 
                             data={'audio': (text_file, 'test.txt')},
                             content_type='multipart/form-data')
    
    # Parse the response
    data = json.loads(response.data)
    
    # Verify the response
    assert response.status_code == 500
    assert data['status'] == 'error' 