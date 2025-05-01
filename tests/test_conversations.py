import pytest
import os
from app import app, db
from models import Conversation, Message
from datetime import datetime

@pytest.fixture(scope='function')
def client():
    """Test client fixture that properly handles Flask contexts"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    # Push an application context
    ctx = app.app_context()
    ctx.push()
    
    # Create tables
    db.create_all()
    
    # Create test client
    with app.test_client() as client:
        yield client
    
    # Clean up
    db.session.remove()
    db.drop_all()
    ctx.pop()

@pytest.fixture
def test_simulation_file():
    """Create a temporary test simulation file"""
    filename = 'test_simulation.json'
    with open(filename, 'w') as f:
        f.write('{"test": "data"}')
    yield filename
    if os.path.exists(filename):
        os.remove(filename)

def test_create_conversation(client):
    """Test creating a new conversation"""
    # Create a conversation
    conversation = Conversation(patient_simulation='test_simulation.json')
    db.session.add(conversation)
    db.session.commit()
    
    # Verify conversation was created
    assert conversation.id is not None
    assert conversation.patient_simulation == 'test_simulation.json'
    assert isinstance(conversation.created_at, datetime)

def test_add_messages_to_conversation(client):
    """Test adding messages to a conversation"""
    # Create a conversation
    conversation = Conversation(patient_simulation='test_simulation.json')
    db.session.add(conversation)
    db.session.commit()
    
    # Add messages
    user_message = Message(
        conversation_id=conversation.id,
        role='user',
        content='Hello'
    )
    assistant_message = Message(
        conversation_id=conversation.id,
        role='assistant',
        content='Hi there!'
    )
    
    db.session.add(user_message)
    db.session.add(assistant_message)
    db.session.commit()
    
    # Verify messages were added
    assert len(conversation.messages) == 2
    assert conversation.messages[0].role == 'user'
    assert conversation.messages[0].content == 'Hello'
    assert conversation.messages[1].role == 'assistant'
    assert conversation.messages[1].content == 'Hi there!'

def test_get_conversations_endpoint(client):
    """Test the GET /api/conversations endpoint"""
    # Create a conversation with messages
    conversation = Conversation(patient_simulation='test_simulation.json')
    db.session.add(conversation)
    db.session.commit()
    
    user_message = Message(
        conversation_id=conversation.id,
        role='user',
        content='Hello'
    )
    assistant_message = Message(
        conversation_id=conversation.id,
        role='assistant',
        content='Hi there!'
    )
    
    db.session.add(user_message)
    db.session.add(assistant_message)
    db.session.commit()
    
    # Test the endpoint
    response = client.get('/api/conversations')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['status'] == 'success'
    assert len(data['conversations']) == 1
    assert data['conversations'][0]['patient_simulation'] == 'test_simulation.json'
    assert len(data['conversations'][0]['messages']) == 2

def test_select_simulation_endpoint(client, test_simulation_file):
    """Test the POST /api/select-simulation endpoint"""
    response = client.post('/api/select-simulation', json={
        'simulation_file': test_simulation_file
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert data['current_simulation'] == test_simulation_file 