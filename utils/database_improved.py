import sqlite3
import os
import json
import logging
from contextlib import contextmanager
from datetime import datetime
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)

# Database file path
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'conversations.db')

@contextmanager
def get_db_connection():
    """
    Context manager for database connections
    Ensures proper connection handling and cleanup
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        yield conn
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        logger.error(f"Database error: {e}")
        raise
    finally:
        if conn:
            conn.close()

def init_db() -> bool:
    """
    Initialize the database by creating necessary tables if they don't exist
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with get_db_connection() as conn:
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
            
            # Create conversation_data table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversation_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id INTEGER NOT NULL,
                    data_key TEXT NOT NULL,
                    data_value TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE,
                    UNIQUE(conversation_id, data_key)
                )
            ''')
            
            conn.commit()
            logger.info("Database initialized successfully")
            return True
            
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        return False

def create_conversation(title: str, simulation_file: Optional[str] = None) -> Optional[int]:
    """
    Create a new conversation and return its ID
    
    Args:
        title: Conversation title
        simulation_file: Optional simulation file path
        
    Returns:
        Optional[int]: Conversation ID if successful, None otherwise
    """
    if not title:
        logger.error("Conversation title cannot be empty")
        return None
        
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO conversations (title, simulation_file) VALUES (?, ?)',
                (title, simulation_file)
            )
            conversation_id = cursor.lastrowid
            conn.commit()
            logger.info(f"Created conversation with ID: {conversation_id}")
            return conversation_id
            
    except Exception as e:
        logger.error(f"Failed to create conversation: {e}")
        return None

def add_message(conversation_id: int, role: str, content: str) -> bool:
    """
    Add a message to a conversation
    
    Args:
        conversation_id: ID of the conversation
        role: Message role (user/assistant)
        content: Message content
        
    Returns:
        bool: True if successful, False otherwise
    """
    # Guard clauses for validation
    if not conversation_id:
        logger.error("Conversation ID is required")
        return False
        
    if not role or role not in ['user', 'assistant']:
        logger.error(f"Invalid role: {role}")
        return False
        
    if not content:
        logger.error("Message content cannot be empty")
        return False
    
    try:
        with get_db_connection() as conn:
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
            logger.debug(f"Added {role} message to conversation {conversation_id}")
            return True
            
    except Exception as e:
        logger.error(f"Failed to add message: {e}")
        return False

def get_conversations() -> List[Dict[str, Any]]:
    """
    Get all conversations ordered by updated_at timestamp
    
    Returns:
        List[Dict]: List of conversation dictionaries
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT id, title, simulation_file, created_at, updated_at '
                'FROM conversations ORDER BY updated_at DESC'
            )
            conversations = [dict(row) for row in cursor.fetchall()]
            logger.debug(f"Retrieved {len(conversations)} conversations")
            return conversations
            
    except Exception as e:
        logger.error(f"Failed to get conversations: {e}")
        return []

def get_conversation(conversation_id: int) -> Optional[Dict[str, Any]]:
    """
    Get a conversation by ID including all its messages
    
    Args:
        conversation_id: ID of the conversation
        
    Returns:
        Optional[Dict]: Conversation dictionary with messages, None if not found
    """
    if not conversation_id:
        logger.error("Conversation ID is required")
        return None
        
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Get conversation details
            cursor.execute(
                'SELECT id, title, simulation_file, created_at, updated_at '
                'FROM conversations WHERE id = ?',
                (conversation_id,)
            )
            conversation = cursor.fetchone()
            
            if not conversation:
                logger.warning(f"Conversation {conversation_id} not found")
                return None
            
            # Get conversation messages
            cursor.execute(
                'SELECT id, role, content, timestamp FROM messages '
                'WHERE conversation_id = ? ORDER BY timestamp',
                (conversation_id,)
            )
            messages = [dict(row) for row in cursor.fetchall()]
            
            # Convert to dict and add messages
            result = dict(conversation)
            result['messages'] = messages
            
            logger.debug(f"Retrieved conversation {conversation_id} with {len(messages)} messages")
            return result
            
    except Exception as e:
        logger.error(f"Failed to get conversation {conversation_id}: {e}")
        return None

def delete_conversation(conversation_id: int) -> bool:
    """
    Delete a conversation and all its messages
    
    Args:
        conversation_id: ID of the conversation to delete
        
    Returns:
        bool: True if deleted, False otherwise
    """
    if not conversation_id:
        logger.error("Conversation ID is required")
        return False
        
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM conversations WHERE id = ?', (conversation_id,))
            conn.commit()
            
            is_deleted = cursor.rowcount > 0
            if is_deleted:
                logger.info(f"Deleted conversation {conversation_id}")
            else:
                logger.warning(f"Conversation {conversation_id} not found for deletion")
                
            return is_deleted
            
    except Exception as e:
        logger.error(f"Failed to delete conversation {conversation_id}: {e}")
        return False

def update_conversation_title(conversation_id: int, new_title: str) -> bool:
    """
    Update the title of a conversation
    
    Args:
        conversation_id: ID of the conversation
        new_title: New title for the conversation
        
    Returns:
        bool: True if updated, False otherwise
    """
    # Guard clauses
    if not conversation_id:
        logger.error("Conversation ID is required")
        return False
        
    if not new_title:
        logger.error("New title cannot be empty")
        return False
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE conversations SET title = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
                (new_title, conversation_id)
            )
            conn.commit()
            
            is_updated = cursor.rowcount > 0
            if is_updated:
                logger.info(f"Updated title for conversation {conversation_id}")
            else:
                logger.warning(f"Conversation {conversation_id} not found for title update")
                
            return is_updated
            
    except Exception as e:
        logger.error(f"Failed to update conversation title: {e}")
        return False

def store_conversation_data(conversation_id: int, data_key: str, data_value: Any) -> bool:
    """
    Store additional data for a conversation
    
    Args:
        conversation_id: ID of the conversation
        data_key: Key for the data
        data_value: Value to store (will be JSON-encoded if complex)
        
    Returns:
        bool: True if successful, False otherwise
    """
    # Guard clauses
    if not conversation_id:
        logger.error("Conversation ID is required")
        return False
        
    if not data_key:
        logger.error("Data key is required")
        return False
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Convert complex data types to JSON
            if isinstance(data_value, (dict, list)):
                data_value = json.dumps(data_value)
            
            # Use INSERT OR REPLACE for simplicity
            cursor.execute('''
                INSERT OR REPLACE INTO conversation_data 
                (conversation_id, data_key, data_value, updated_at) 
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ''', (conversation_id, data_key, data_value))
            
            conn.commit()
            logger.debug(f"Stored data key '{data_key}' for conversation {conversation_id}")
            return True
            
    except Exception as e:
        logger.error(f"Failed to store conversation data: {e}")
        return False

def get_conversation_data(conversation_id: int, data_key: str) -> Any:
    """
    Retrieve additional data for a conversation
    
    Args:
        conversation_id: ID of the conversation
        data_key: Key for the data to retrieve
        
    Returns:
        Any: Retrieved data value, None if not found
    """
    # Guard clauses
    if not conversation_id:
        logger.error("Conversation ID is required")
        return None
        
    if not data_key:
        logger.error("Data key is required")
        return None
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT data_value FROM conversation_data WHERE conversation_id = ? AND data_key = ?',
                (conversation_id, data_key)
            )
            row = cursor.fetchone()
            
            if not row:
                logger.debug(f"No data found for key '{data_key}' in conversation {conversation_id}")
                return None
            
            data_value = row[0]
            
            # Try to parse as JSON, return as-is if not valid JSON
            try:
                return json.loads(data_value)
            except (json.JSONDecodeError, TypeError):
                return data_value
                
    except Exception as e:
        logger.error(f"Failed to get conversation data: {e}")
        return None 