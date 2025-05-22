import sqlite3
import json
from datetime import datetime
import os

class ConversationDatabase:
    def __init__(self, db_path='conversations.db'):
        """Initialize the database connection"""
        self.db_path = db_path
        self._create_tables()
    
    def _create_tables(self):
        """Create necessary database tables if they don't exist"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create conversations table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_simulation TEXT,
                    start_time TIMESTAMP,
                    end_time TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create messages table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id INTEGER,
                    role TEXT,
                    content TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (conversation_id) REFERENCES conversations (id)
                )
            ''')
            
            # Create settings table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT UNIQUE,
                    value TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
    
    def start_conversation(self, patient_simulation=None):
        """Start a new conversation and return its ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO conversations (patient_simulation, start_time) VALUES (?, ?)',
                (patient_simulation, datetime.now())
            )
            conn.commit()
            return cursor.lastrowid
    
    def end_conversation(self, conversation_id):
        """Mark a conversation as ended"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE conversations SET end_time = ? WHERE id = ?',
                (datetime.now(), conversation_id)
            )
            conn.commit()
    
    def add_message(self, conversation_id, role, content):
        """Add a message to a conversation"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)',
                (conversation_id, role, content)
            )
            conn.commit()
    
    def get_conversation(self, conversation_id):
        """Get a conversation with all its messages"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Get conversation details
            cursor.execute('SELECT * FROM conversations WHERE id = ?', (conversation_id,))
            conversation = cursor.fetchone()
            
            if not conversation:
                return None
            
            # Get all messages for this conversation
            cursor.execute(
                'SELECT role, content, timestamp FROM messages WHERE conversation_id = ? ORDER BY timestamp',
                (conversation_id,)
            )
            messages = cursor.fetchall()
            
            return {
                'id': conversation[0],
                'patient_simulation': conversation[1],
                'start_time': conversation[2],
                'end_time': conversation[3],
                'created_at': conversation[4],
                'messages': [
                    {'role': msg[0], 'content': msg[1], 'timestamp': msg[2]}
                    for msg in messages
                ]
            }
    
    def get_all_conversations(self):
        """Get all conversations"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM conversations ORDER BY created_at DESC')
            return cursor.fetchall()
    
    def delete_conversation(self, conversation_id):
        """Delete a conversation and all its messages"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM messages WHERE conversation_id = ?', (conversation_id,))
            cursor.execute('DELETE FROM conversations WHERE id = ?', (conversation_id,))
            conn.commit()
            
    def get_setting(self, key, default_value=None):
        """Get a setting value by key"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
            result = cursor.fetchone()
            
            if result:
                return result[0]
            return default_value
    
    def set_setting(self, key, value):
        """Set a setting value by key"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO settings (key, value, updated_at) VALUES (?, ?, ?) '
                'ON CONFLICT(key) DO UPDATE SET value = ?, updated_at = ?',
                (key, value, datetime.now(), value, datetime.now())
            )
            conn.commit()
            return True 