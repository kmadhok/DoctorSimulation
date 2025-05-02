import pytest
import os
import tempfile
from datetime import datetime
from utils.database import ConversationDatabase

@pytest.fixture
def temp_db():
    """Fixture for temporary database"""
    # Create a temporary database file
    fd, path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    
    # Create database instance
    db = ConversationDatabase(path)
    
    yield db
    
    # Clean up
    os.unlink(path)

def test_create_tables(temp_db):
    """Test that tables are created correctly"""
    with temp_db._create_tables() as conn:
        cursor = conn.cursor()
        
        # Check conversations table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='conversations'")
        assert cursor.fetchone() is not None
        
        # Check messages table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='messages'")
        assert cursor.fetchone() is not None

def test_start_conversation(temp_db):
    """Test starting a new conversation"""
    # Start conversation
    conv_id = temp_db.start_conversation("test_patient")
    
    # Verify conversation was created
    with temp_db._create_tables() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM conversations WHERE id = ?", (conv_id,))
        conversation = cursor.fetchone()
        
        assert conversation is not None
        assert conversation[1] == "test_patient"  # patient_simulation
        assert conversation[2] is not None  # start_time
        assert conversation[3] is None  # end_time should be None

def test_end_conversation(temp_db):
    """Test ending a conversation"""
    # Start and end conversation
    conv_id = temp_db.start_conversation()
    temp_db.end_conversation(conv_id)
    
    # Verify conversation was ended
    with temp_db._create_tables() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT end_time FROM conversations WHERE id = ?", (conv_id,))
        end_time = cursor.fetchone()[0]
        
        assert end_time is not None

def test_add_message(temp_db):
    """Test adding messages to a conversation"""
    # Start conversation
    conv_id = temp_db.start_conversation()
    
    # Add messages
    temp_db.add_message(conv_id, "user", "Hello")
    temp_db.add_message(conv_id, "assistant", "Hi there!")
    
    # Verify messages were added
    with temp_db._create_tables() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT role, content FROM messages WHERE conversation_id = ? ORDER BY timestamp", (conv_id,))
        messages = cursor.fetchall()
        
        assert len(messages) == 2
        assert messages[0] == ("user", "Hello")
        assert messages[1] == ("assistant", "Hi there!")

def test_get_conversation(temp_db):
    """Test retrieving a conversation with its messages"""
    # Start conversation and add messages
    conv_id = temp_db.start_conversation("test_patient")
    temp_db.add_message(conv_id, "user", "Hello")
    temp_db.add_message(conv_id, "assistant", "Hi there!")
    temp_db.end_conversation(conv_id)
    
    # Get conversation
    conversation = temp_db.get_conversation(conv_id)
    
    # Verify conversation data
    assert conversation is not None
    assert conversation['id'] == conv_id
    assert conversation['patient_simulation'] == "test_patient"
    assert conversation['start_time'] is not None
    assert conversation['end_time'] is not None
    assert len(conversation['messages']) == 2
    assert conversation['messages'][0]['role'] == "user"
    assert conversation['messages'][0]['content'] == "Hello"
    assert conversation['messages'][1]['role'] == "assistant"
    assert conversation['messages'][1]['content'] == "Hi there!"

def test_get_all_conversations(temp_db):
    """Test retrieving all conversations"""
    # Create multiple conversations
    conv1 = temp_db.start_conversation("patient1")
    conv2 = temp_db.start_conversation("patient2")
    
    # Get all conversations
    conversations = temp_db.get_all_conversations()
    
    # Verify conversations
    assert len(conversations) == 2
    assert conversations[0][1] == "patient2"  # Most recent first
    assert conversations[1][1] == "patient1"

def test_delete_conversation(temp_db):
    """Test deleting a conversation and its messages"""
    # Start conversation and add messages
    conv_id = temp_db.start_conversation()
    temp_db.add_message(conv_id, "user", "Hello")
    temp_db.add_message(conv_id, "assistant", "Hi there!")
    
    # Delete conversation
    temp_db.delete_conversation(conv_id)
    
    # Verify conversation and messages were deleted
    with temp_db._create_tables() as conn:
        cursor = conn.cursor()
        
        # Check conversation
        cursor.execute("SELECT * FROM conversations WHERE id = ?", (conv_id,))
        assert cursor.fetchone() is None
        
        # Check messages
        cursor.execute("SELECT * FROM messages WHERE conversation_id = ?", (conv_id,))
        assert cursor.fetchall() == []

def test_conversation_with_multiple_messages(temp_db):
    """Test handling a conversation with many messages"""
    # Start conversation
    conv_id = temp_db.start_conversation()
    
    # Add multiple messages
    messages = [
        ("user", "Hello"),
        ("assistant", "Hi there!"),
        ("user", "How are you?"),
        ("assistant", "I'm doing well, thank you!"),
        ("user", "What's the weather like?"),
        ("assistant", "I don't have access to weather information.")
    ]
    
    for role, content in messages:
        temp_db.add_message(conv_id, role, content)
    
    # Get conversation
    conversation = temp_db.get_conversation(conv_id)
    
    # Verify all messages were stored correctly
    assert len(conversation['messages']) == len(messages)
    for i, (role, content) in enumerate(messages):
        assert conversation['messages'][i]['role'] == role
        assert conversation['messages'][i]['content'] == content 