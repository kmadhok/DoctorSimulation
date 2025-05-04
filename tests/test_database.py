import os
import pytest
import tempfile
import sqlite3
import sys
from pathlib import Path

# Add the parent directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import the database module with the path now resolved
from utils.database import init_db, create_conversation, add_message, get_conversations, get_conversation, delete_conversation

# Use a temporary database for testing
@pytest.fixture
def test_db():
    # Create a temporary file
    fd, temp_path = tempfile.mkstemp()
    os.close(fd)
    
    # Save original DB_PATH
    from utils.database import DB_PATH
    original_path = DB_PATH
    
    # Override DB_PATH for testing
    import utils.database
    utils.database.DB_PATH = temp_path
    
    # Initialize the database
    init_db()
    
    yield temp_path
    
    # Reset DB_PATH and remove the temporary file
    utils.database.DB_PATH = original_path
    os.unlink(temp_path)

def test_create_conversation(test_db):
    # Create a test conversation
    conversation_id = create_conversation("Test Conversation", "test_simulation.json")
    
    # Verify it was created
    assert conversation_id > 0
    
    # Connect to the database and check
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, simulation_file FROM conversations WHERE id = ?", (conversation_id,))
    result = cursor.fetchone()
    conn.close()
    
    assert result is not None
    assert result[0] == conversation_id
    assert result[1] == "Test Conversation"
    assert result[2] == "test_simulation.json"

def test_add_and_get_messages(test_db):
    # Create a test conversation
    conversation_id = create_conversation("Test Conversation")
    
    # Add messages
    add_message(conversation_id, "user", "Hello")
    add_message(conversation_id, "assistant", "Hi there!")
    
    # Get the conversation with messages
    conversation = get_conversation(conversation_id)
    
    # Verify conversation data
    assert conversation is not None
    assert conversation["id"] == conversation_id
    assert conversation["title"] == "Test Conversation"
    
    # Verify messages
    assert len(conversation["messages"]) == 2
    assert conversation["messages"][0]["role"] == "user"
    assert conversation["messages"][0]["content"] == "Hello"
    assert conversation["messages"][1]["role"] == "assistant"
    assert conversation["messages"][1]["content"] == "Hi there!"

def test_get_conversations(test_db):
    # Create multiple conversations
    conversation_id1 = create_conversation("Conversation 1")
    conversation_id2 = create_conversation("Conversation 2")
    
    # Get all conversations
    conversations = get_conversations()
    
    # Verify we have at least 2 conversations
    assert len(conversations) >= 2
    
    # Verify the conversations we created are in the list
    conversation_ids = [c["id"] for c in conversations]
    assert conversation_id1 in conversation_ids
    assert conversation_id2 in conversation_ids

def test_delete_conversation(test_db):
    # Create a conversation
    conversation_id = create_conversation("To Be Deleted")
    
    # Add a message
    add_message(conversation_id, "user", "Delete me")
    
    # Delete the conversation
    result = delete_conversation(conversation_id)
    assert result is True
    
    # Try to get the deleted conversation
    conversation = get_conversation(conversation_id)
    assert conversation is None
    
    # Try to delete a non-existent conversation
    result = delete_conversation(9999)
    assert result is False 