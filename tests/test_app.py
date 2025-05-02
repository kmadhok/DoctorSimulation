import pytest
import json
import tempfile
import os
from app import app, db
from unittest.mock import patch

@pytest.fixture
def client():
    """Create a test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def temp_db():
    """Create a temporary database for testing"""
    fd, path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    
    # Create a new database instance with the temporary path
    test_db = db.__class__(path)
    
    yield test_db
    
    # Clean up
    os.unlink(path)

def test_list_conversations_empty(client, temp_db):
    """Test listing conversations when none exist"""
    # Replace the app's database with our test database
    app.db = temp_db
    
    response = client.get('/api/conversations')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['status'] == 'success'
    assert len(data['conversations']) == 0

def test_list_conversations_with_data(client, temp_db):
    """Test listing conversations with existing data"""
    # Replace the app's database with our test database
    app.db = temp_db
    
    # Create some test conversations
    conv1 = temp_db.start_conversation("patient1")
    conv2 = temp_db.start_conversation("patient2")
    
    response = client.get('/api/conversations')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['status'] == 'success'
    assert len(data['conversations']) == 2
    assert data['conversations'][0][1] == "patient2"  # Most recent first
    assert data['conversations'][1][1] == "patient1"

def test_get_conversation(client, temp_db):
    """Test getting a specific conversation"""
    # Replace the app's database with our test database
    app.db = temp_db
    
    # Create a test conversation with messages
    conv_id = temp_db.start_conversation("test_patient")
    temp_db.add_message(conv_id, "user", "Hello")
    temp_db.add_message(conv_id, "assistant", "Hi there!")
    temp_db.end_conversation(conv_id)
    
    response = client.get(f'/api/conversations/{conv_id}')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['status'] == 'success'
    assert data['conversation']['id'] == conv_id
    assert data['conversation']['patient_simulation'] == "test_patient"
    assert len(data['conversation']['messages']) == 2
    assert data['conversation']['messages'][0]['role'] == "user"
    assert data['conversation']['messages'][0]['content'] == "Hello"
    assert data['conversation']['messages'][1]['role'] == "assistant"
    assert data['conversation']['messages'][1]['content'] == "Hi there!"

def test_get_nonexistent_conversation(client, temp_db):
    """Test getting a conversation that doesn't exist"""
    # Replace the app's database with our test database
    app.db = temp_db
    
    response = client.get('/api/conversations/999')
    data = json.loads(response.data)
    
    assert response.status_code == 404
    assert data['status'] == 'error'
    assert data['message'] == 'Conversation not found'

def test_conversation_storage_during_chat(client, temp_db):
    """Test that conversations are stored during chat"""
    # Replace the app's database with our test database
    app.db = temp_db
    
    # Select a simulation
    response = client.post('/api/select-simulation',
                          json={'simulation_file': 'test_patient.json'})
    assert response.status_code == 200
    
    # Process some audio (simulate a conversation)
    with tempfile.NamedTemporaryFile(suffix='.wav') as audio_file:
        audio_file.write(b"fake_audio_data")
        audio_file.seek(0)
        
        response = client.post('/process_audio',
                             data={'audio': (audio_file, 'test.wav')},
                             content_type='multipart/form-data')
    
    # Get all conversations
    response = client.get('/api/conversations')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert len(data['conversations']) > 0
    
    # Get the conversation details
    conv_id = data['conversations'][0][0]  # Get the ID of the most recent conversation
    response = client.get(f'/api/conversations/{conv_id}')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['conversation']['patient_simulation'] == 'test_patient.json'
    assert len(data['conversation']['messages']) > 0

def test_conversation_end_on_exit(client, temp_db):
    """Test that conversation is properly ended when user says 'exit'"""
    # Replace the app's database with our test database
    app.db = temp_db
    
    # Select a simulation
    response = client.post('/api/select-simulation',
                          json={'simulation_file': 'test_patient.json'})
    assert response.status_code == 200
    
    # Process audio with exit command
    with tempfile.NamedTemporaryFile(suffix='.wav') as audio_file:
        audio_file.write(b"fake_audio_data")
        audio_file.seek(0)
        
        # Mock the transcription to return "exit"
        with patch('app.transcribe_audio_data', return_value="exit"):
            response = client.post('/process_audio',
                                 data={'audio': (audio_file, 'test.wav')},
                                 content_type='multipart/form-data')
    
    # Get all conversations
    response = client.get('/api/conversations')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert len(data['conversations']) > 0
    
    # Get the conversation details
    conv_id = data['conversations'][0][0]
    response = client.get(f'/api/conversations/{conv_id}')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['conversation']['end_time'] is not None  # Conversation should be ended 