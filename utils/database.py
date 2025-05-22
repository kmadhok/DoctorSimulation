import sqlite3
import os
import json
import logging
from datetime import datetime

# Initialize logger
logger = logging.getLogger(__name__)

# Database file path
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'conversations.db')

def init_db():
    """Initialize the database by creating necessary tables if they don't exist"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create conversations table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        simulation_file TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create messages table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conversation_id INTEGER NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
    )
    ''')
    
    conn.commit()
    conn.close()

def create_conversation(title, simulation_file=None):
    """Create a new conversation and return its ID"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        'INSERT INTO conversations (title, simulation_file) VALUES (?, ?)',
        (title, simulation_file)
    )
    
    conversation_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return conversation_id

def add_message(conversation_id, role, content):
    """Add a message to a conversation"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        'INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)',
        (conversation_id, role, content)
    )
    
    # Update the conversation's updated_at timestamp
    cursor.execute(
        'UPDATE conversations SET updated_at = CURRENT_TIMESTAMP WHERE id = ?',
        (conversation_id,)
    )
    
    conn.commit()
    conn.close()

def get_conversations():
    """Get all conversations ordered by updated_at timestamp"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute(
        'SELECT id, title, simulation_file, created_at, updated_at FROM conversations ORDER BY updated_at DESC'
    )
    
    conversations = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return conversations

def get_conversation(conversation_id):
    """Get a conversation by ID including all its messages"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get conversation details
    cursor.execute(
        'SELECT id, title, simulation_file, created_at, updated_at FROM conversations WHERE id = ?',
        (conversation_id,)
    )
    conversation = cursor.fetchone()
    
    if not conversation:
        conn.close()
        return None
    
    # Get conversation messages
    cursor.execute(
        'SELECT id, role, content, timestamp FROM messages WHERE conversation_id = ? ORDER BY timestamp',
        (conversation_id,)
    )
    messages = [dict(row) for row in cursor.fetchall()]
    
    # Convert to dict and add messages
    result = dict(conversation)
    result['messages'] = messages
    
    conn.close()
    return result

def delete_conversation(conversation_id):
    """Delete a conversation and all its messages"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM conversations WHERE id = ?', (conversation_id,))
    
    conn.commit()
    conn.close()
    
    return cursor.rowcount > 0  # Return True if a row was deleted

def update_conversation_title(conversation_id, new_title):
    """Update the title of a conversation"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        'UPDATE conversations SET title = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
        (new_title, conversation_id)
    )
    
    conn.commit()
    conn.close()
    
    return cursor.rowcount > 0  # Return True if a row was updated 

def store_conversation_data(conversation_id, data_key, data_value):
    """Store additional data for a conversation"""
    conn = sqlite3.connect(DB_PATH)
    try:
        # Convert complex data types to JSON
        if isinstance(data_value, (dict, list)):
            data_value = json.dumps(data_value)
            
        # Check if the conversation_data table exists
        conn.execute('''
            CREATE TABLE IF NOT EXISTS conversation_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER,
                data_key TEXT,
                data_value TEXT,
                FOREIGN KEY (conversation_id) REFERENCES conversations (id)
            )
        ''')
        
        # Check if data already exists
        cursor = conn.execute(
            'SELECT id FROM conversation_data WHERE conversation_id = ? AND data_key = ?',
            (conversation_id, data_key)
        )
        row = cursor.fetchone()
        
        if row:
            # Update existing data
            conn.execute(
                'UPDATE conversation_data SET data_value = ? WHERE id = ?',
                (data_value, row[0])
            )
        else:
            # Insert new data
            conn.execute(
                'INSERT INTO conversation_data (conversation_id, data_key, data_value) VALUES (?, ?, ?)',
                (conversation_id, data_key, data_value)
            )
            
        conn.commit()
        return True
    except Exception as e:
        logger.error(f"Error storing conversation data: {e}")
        return False
    finally:
        conn.close()

def get_conversation_data(conversation_id, data_key):
    """Retrieve additional data for a conversation"""
    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.execute(
            'SELECT data_value FROM conversation_data WHERE conversation_id = ? AND data_key = ?',
            (conversation_id, data_key)
        )
        row = cursor.fetchone()
        
        if row:
            data_value = row[0]
            # Try to parse as JSON if it looks like JSON
            try:
                if data_value.startswith('{') or data_value.startswith('['):
                    return json.loads(data_value)
                return data_value
            except (json.JSONDecodeError, AttributeError):
                return data_value
        return None
    except Exception as e:
        logger.error(f"Error retrieving conversation data: {e}")
        return None
    finally:
        conn.close() 