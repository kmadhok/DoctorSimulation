import sqlite3
import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List

# Initialize logger
logger = logging.getLogger(__name__)

# Database file path
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'conversations.db')

# ✅ PHASE 4.1: Enhanced database schema version tracking
DATABASE_VERSION = 2  # Updated for AI-generated patient support

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
    
    # ✅ PHASE 4.1: Enhanced conversation_data table with proper constraints and indexing
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS conversation_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conversation_id INTEGER NOT NULL,
        data_key TEXT NOT NULL,
        data_value TEXT NOT NULL,
        data_type TEXT DEFAULT 'string',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE,
        UNIQUE(conversation_id, data_key)
    )
    ''')
    
    # ✅ PHASE 4.1: Create indexes for better performance
    cursor.execute('''
    CREATE INDEX IF NOT EXISTS idx_conversation_data_lookup 
    ON conversation_data(conversation_id, data_key)
    ''')
    
    cursor.execute('''
    CREATE INDEX IF NOT EXISTS idx_messages_conversation 
    ON messages(conversation_id, timestamp)
    ''')
    
    # ✅ PHASE 4.1: Database version tracking table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS database_version (
        version INTEGER PRIMARY KEY,
        applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        description TEXT
    )
    ''')
    
    # Check and apply migrations if needed
    _check_and_apply_migrations(cursor)
    
    conn.commit()
    conn.close()
    logger.info("Database initialized successfully")

def _check_and_apply_migrations(cursor):
    """Check database version and apply necessary migrations"""
    # Get current database version
    cursor.execute('SELECT MAX(version) FROM database_version')
    result = cursor.fetchone()
    current_version = result[0] if result[0] is not None else 0
    
    logger.info(f"Current database version: {current_version}, Target version: {DATABASE_VERSION}")
    
    # Apply migrations if needed
    if current_version < 1:
        _migrate_to_version_1(cursor)
    
    if current_version < 2:
        _migrate_to_version_2(cursor)

def _migrate_to_version_1(cursor):
    """Migration to version 1: Add indexes and constraints"""
    logger.info("Applying migration to database version 1...")
    
    try:
        # Add data_type column if it doesn't exist
        cursor.execute('PRAGMA table_info(conversation_data)')
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'data_type' not in columns:
            cursor.execute('ALTER TABLE conversation_data ADD COLUMN data_type TEXT DEFAULT "string"')
            logger.info("Added data_type column to conversation_data table")
        
        if 'created_at' not in columns:
            # ✅ PHASE 4.1: Fix SQLite limitation with CURRENT_TIMESTAMP in ALTER TABLE
            cursor.execute('ALTER TABLE conversation_data ADD COLUMN created_at TIMESTAMP')
            # Update existing rows with current timestamp
            cursor.execute('UPDATE conversation_data SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL')
            logger.info("Added created_at column to conversation_data table")
            
        if 'updated_at' not in columns:
            # ✅ PHASE 4.1: Fix SQLite limitation with CURRENT_TIMESTAMP in ALTER TABLE
            cursor.execute('ALTER TABLE conversation_data ADD COLUMN updated_at TIMESTAMP')
            # Update existing rows with current timestamp
            cursor.execute('UPDATE conversation_data SET updated_at = CURRENT_TIMESTAMP WHERE updated_at IS NULL')
            logger.info("Added updated_at column to conversation_data table")
        
        # Record migration
        cursor.execute(
            'INSERT INTO database_version (version, description) VALUES (?, ?)',
            (1, 'Added enhanced conversation_data schema with timestamps and data_type')
        )
        
        logger.info("Migration to version 1 completed successfully")
        
    except Exception as e:
        logger.error(f"Error during migration to version 1: {e}")
        raise

def _migrate_to_version_2(cursor):
    """Migration to version 2: Support for AI-generated patient data"""
    logger.info("Applying migration to database version 2...")
    
    try:
        # ✅ PHASE 4.1: Migrate existing custom patient data to new structure
        cursor.execute('SELECT conversation_id, data_value FROM conversation_data WHERE data_key = "patient_data"')
        existing_patient_data = cursor.fetchall()
        
        migrated_count = 0
        for conversation_id, data_value in existing_patient_data:
            try:
                # Parse existing patient data
                if isinstance(data_value, str):
                    patient_data = json.loads(data_value)
                else:
                    patient_data = data_value
                
                # Check if this is already in the new format
                if patient_data.get('type') in ['ai_generated', 'file_based', 'custom']:
                    continue  # Already migrated
                
                # Migrate to new structure
                migrated_data = {
                    'type': 'custom',  # Mark legacy data as custom
                    'prompt_template': patient_data.get('prompt_template', ''),
                    'patient_details': patient_data.get('patient_details', {}),
                    'voice_id': patient_data.get('voice_id', 'Fritz-PlayAI'),
                    'migration_metadata': {
                        'migrated_from': 'legacy_format',
                        'migration_date': datetime.now().isoformat(),
                        'original_structure': 'custom_patient'
                    }
                }
                
                # Update the record
                cursor.execute(
                    'UPDATE conversation_data SET data_value = ?, data_type = ?, updated_at = CURRENT_TIMESTAMP WHERE conversation_id = ? AND data_key = ?',
                    (json.dumps(migrated_data), 'json', conversation_id, 'patient_data')
                )
                
                migrated_count += 1
                logger.debug(f"Migrated patient data for conversation {conversation_id}")
                
            except Exception as e:
                logger.error(f"Error migrating patient data for conversation {conversation_id}: {e}")
                continue
        
        # Record migration
        cursor.execute(
            'INSERT INTO database_version (version, description) VALUES (?, ?)',
            (2, f'AI-generated patient data support - migrated {migrated_count} existing records')
        )
        
        logger.info(f"Migration to version 2 completed successfully - migrated {migrated_count} patient records")
        
    except Exception as e:
        logger.error(f"Error during migration to version 2: {e}")
        raise

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
    
    logger.debug(f"Created conversation {conversation_id}: {title}")
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

def store_conversation_data(conversation_id: int, data_key: str, data_value: Any) -> bool:
    """
    Store additional data for a conversation with enhanced validation and error handling.
    ✅ PHASE 4.1: Enhanced JSON storage with validation and type tracking.
    
    Args:
        conversation_id (int): The conversation ID
        data_key (str): The key for the data
        data_value (Any): The value to store
        
    Returns:
        bool: True if successful, False otherwise
    """
    conn = sqlite3.connect(DB_PATH)
    try:
        # ✅ PHASE 4.1: Enhanced data type detection and validation
        data_type = 'string'
        if isinstance(data_value, (dict, list)):
            try:
                json_value = json.dumps(data_value, ensure_ascii=False)
                # ✅ Validate that the JSON can be parsed back
                json.loads(json_value)
                data_value = json_value
                data_type = 'json'
                logger.debug(f"Storing JSON data for conversation {conversation_id}, key: {data_key}")
            except (TypeError, ValueError) as e:
                logger.error(f"Failed to serialize data for conversation {conversation_id}, key {data_key}: {e}")
                return False
        elif isinstance(data_value, (int, float)):
            data_type = 'number'
        elif isinstance(data_value, bool):
            data_type = 'boolean'
            data_value = str(data_value)
        else:
            data_value = str(data_value)
            data_type = 'string'
        
        # ✅ PHASE 4.1: Check if enhanced columns exist before using them
        cursor = conn.cursor()
        cursor.execute('PRAGMA table_info(conversation_data)')
        columns = [col[1] for col in cursor.fetchall()]
        
        has_data_type = 'data_type' in columns
        has_updated_at = 'updated_at' in columns
        
        # Build appropriate INSERT OR REPLACE query based on available columns
        if has_data_type and has_updated_at:
            # Full enhanced version
            conn.execute(
                '''INSERT OR REPLACE INTO conversation_data 
                   (conversation_id, data_key, data_value, data_type, updated_at) 
                   VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)''',
                (conversation_id, data_key, data_value, data_type)
            )
        elif has_data_type:
            # Has data_type but not updated_at
            conn.execute(
                '''INSERT OR REPLACE INTO conversation_data 
                   (conversation_id, data_key, data_value, data_type) 
                   VALUES (?, ?, ?, ?)''',
                (conversation_id, data_key, data_value, data_type)
            )
        else:
            # Legacy version - basic columns only
            conn.execute(
                '''INSERT OR REPLACE INTO conversation_data 
                   (conversation_id, data_key, data_value) 
                   VALUES (?, ?, ?)''',
                (conversation_id, data_key, data_value)
            )
        
        conn.commit()
        logger.debug(f"Successfully stored {data_type} data for conversation {conversation_id}, key: {data_key}")
        return True
        
    except sqlite3.Error as e:
        logger.error(f"Database error storing conversation data: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error storing conversation data: {e}")
        return False
    finally:
        conn.close()

def get_conversation_data(conversation_id: int, data_key: str) -> Optional[Any]:
    """
    Retrieve additional data for a conversation with enhanced parsing and error handling.
    ✅ PHASE 4.1: Enhanced retrieval with proper type restoration.
    
    Args:
        conversation_id (int): The conversation ID
        data_key (str): The key for the data
        
    Returns:
        Optional[Any]: The retrieved data or None if not found
    """
    conn = sqlite3.connect(DB_PATH)
    try:
        # ✅ PHASE 4.1: Check if enhanced columns exist
        cursor = conn.cursor()
        cursor.execute('PRAGMA table_info(conversation_data)')
        columns = [col[1] for col in cursor.fetchall()]
        has_data_type = 'data_type' in columns
        
        # Query with appropriate columns
        if has_data_type:
            cursor.execute(
                'SELECT data_value, data_type FROM conversation_data WHERE conversation_id = ? AND data_key = ?',
                (conversation_id, data_key)
            )
            row = cursor.fetchone()
            
            if not row:
                logger.debug(f"No data found for conversation {conversation_id}, key: {data_key}")
                return None
            
            data_value, data_type = row
            
            # ✅ PHASE 4.1: Enhanced type restoration based on stored data_type
            try:
                if data_type == 'json':
                    parsed_data = json.loads(data_value)
                    logger.debug(f"Retrieved JSON data for conversation {conversation_id}, key: {data_key}")
                    return parsed_data
                elif data_type == 'number':
                    # Try to determine if it's int or float
                    if '.' in str(data_value):
                        return float(data_value)
                    else:
                        return int(data_value)
                elif data_type == 'boolean':
                    return data_value.lower() == 'true'
                else:
                    return data_value
                    
            except (json.JSONDecodeError, ValueError) as e:
                logger.error(f"Error parsing stored data for conversation {conversation_id}, key {data_key}: {e}")
                # ✅ Fallback to string if parsing fails
                return data_value
        else:
            # Legacy version - no data_type column
            cursor.execute(
                'SELECT data_value FROM conversation_data WHERE conversation_id = ? AND data_key = ?',
                (conversation_id, data_key)
            )
            row = cursor.fetchone()
            
            if not row:
                logger.debug(f"No data found for conversation {conversation_id}, key: {data_key}")
                return None
            
            data_value = row[0]
            
            # Legacy parsing - try to detect JSON
            if isinstance(data_value, str) and (data_value.startswith('{') or data_value.startswith('[')):
                try:
                    return json.loads(data_value)
                except json.JSONDecodeError:
                    return data_value
            return data_value
        
    except sqlite3.Error as e:
        logger.error(f"Database error retrieving conversation data: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error retrieving conversation data: {e}")
        return None
    finally:
        conn.close()

def get_all_conversation_data(conversation_id: int) -> Dict[str, Any]:
    """
    Retrieve all data for a conversation.
    ✅ PHASE 4.1: New function for comprehensive data retrieval.
    
    Args:
        conversation_id (int): The conversation ID
        
    Returns:
        Dict[str, Any]: Dictionary of all data keys and values
    """
    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.execute(
            'SELECT data_key, data_value, data_type FROM conversation_data WHERE conversation_id = ?',
            (conversation_id,)
        )
        rows = cursor.fetchall()
        
        result = {}
        for data_key, data_value, data_type in rows:
            try:
                if data_type == 'json':
                    result[data_key] = json.loads(data_value)
                elif data_type == 'number':
                    result[data_key] = float(data_value) if '.' in str(data_value) else int(data_value)
                elif data_type == 'boolean':
                    result[data_key] = data_value.lower() == 'true'
                else:
                    result[data_key] = data_value
            except (json.JSONDecodeError, ValueError) as e:
                logger.error(f"Error parsing data for conversation {conversation_id}, key {data_key}: {e}")
                result[data_key] = data_value  # Fallback to string
        
        logger.debug(f"Retrieved {len(result)} data items for conversation {conversation_id}")
        return result
        
    except sqlite3.Error as e:
        logger.error(f"Database error retrieving all conversation data: {e}")
        return {}
    except Exception as e:
        logger.error(f"Unexpected error retrieving all conversation data: {e}")
        return {}
    finally:
        conn.close()

def backup_database(backup_path: str = None) -> bool:
    """
    ✅ PHASE 4.1: Create a backup of the database.
    
    Args:
        backup_path (str, optional): Path for the backup file
        
    Returns:
        bool: True if successful, False otherwise
    """
    if backup_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"conversations_backup_{timestamp}.db"
    
    try:
        source = sqlite3.connect(DB_PATH)
        backup = sqlite3.connect(backup_path)
        source.backup(backup)
        backup.close()
        source.close()
        
        logger.info(f"Database backup created successfully: {backup_path}")
        return True
        
    except Exception as e:
        logger.error(f"Error creating database backup: {e}")
        return False

def restore_database(backup_path: str) -> bool:
    """
    ✅ PHASE 4.1: Restore database from backup.
    
    Args:
        backup_path (str): Path to the backup file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if not os.path.exists(backup_path):
            logger.error(f"Backup file not found: {backup_path}")
            return False
        
        # Create a backup of current database before restoring
        current_backup = f"conversations_pre_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        backup_database(current_backup)
        
        # Restore from backup
        backup = sqlite3.connect(backup_path)
        target = sqlite3.connect(DB_PATH)
        backup.backup(target)
        target.close()
        backup.close()
        
        logger.info(f"Database restored successfully from: {backup_path}")
        return True
        
    except Exception as e:
        logger.error(f"Error restoring database: {e}")
        return False

def validate_patient_data_structure(patient_data: Dict[str, Any]) -> tuple[bool, List[str]]:
    """
    ✅ PHASE 4.1: Validate patient data structure for storage.
    
    Args:
        patient_data (Dict): Patient data to validate
        
    Returns:
        tuple[bool, List[str]]: (is_valid, list_of_errors)
    """
    errors = []
    
    # Check required top-level fields
    required_fields = ['type', 'patient_details']
    for field in required_fields:
        if field not in patient_data:
            errors.append(f"Missing required field: {field}")
    
    # Validate type field
    valid_types = ['ai_generated', 'file_based', 'custom']
    if 'type' in patient_data and patient_data['type'] not in valid_types:
        errors.append(f"Invalid patient type: {patient_data['type']}. Must be one of: {valid_types}")
    
    # Validate patient_details structure
    if 'patient_details' in patient_data:
        if not isinstance(patient_data['patient_details'], dict):
            errors.append("patient_details must be a dictionary")
    
    # Type-specific validation
    if patient_data.get('type') == 'ai_generated':
        if 'generation_metadata' not in patient_data:
            errors.append("AI-generated patients must have generation_metadata")
        else:
            metadata = patient_data['generation_metadata']
            required_metadata = ['specialty', 'input_symptoms', 'severity']
            for field in required_metadata:
                if field not in metadata:
                    errors.append(f"Missing generation_metadata field: {field}")
    
    return len(errors) == 0, errors

def cleanup_old_data(days_older_than: int = 30) -> int:
    """
    ✅ PHASE 4.1: Clean up old conversation data.
    
    Args:
        days_older_than (int): Delete conversations older than this many days
        
    Returns:
        int: Number of conversations deleted
    """
    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.cursor()
        
        # Delete old conversations and their associated data
        cursor.execute(
            '''DELETE FROM conversations 
               WHERE created_at < datetime('now', '-{} days')'''.format(days_older_than)
        )
        
        deleted_count = cursor.rowcount
        conn.commit()
        
        logger.info(f"Cleaned up {deleted_count} conversations older than {days_older_than} days")
        return deleted_count
        
    except sqlite3.Error as e:
        logger.error(f"Error during database cleanup: {e}")
        return 0
    finally:
        conn.close()

# ✅ PHASE 4.1: Initialize database on import
if __name__ != "__main__":
    try:
        init_db()
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")

# ✅ PHASE 4.1: Testing functions for validation
def test_database_functionality():
    """Test database functionality with AI-generated patient data"""
    logger.info("Testing database functionality...")
    
    try:
        # Test conversation creation
        conv_id = create_conversation("Test AI Patient Case")
        logger.info(f"Created test conversation: {conv_id}")
        
        # Test AI patient data storage
        test_patient_data = {
            'type': 'ai_generated',
            'patient_details': {
                'age': '45',
                'gender': 'Female',
                'occupation': 'Teacher',
                'medical_history': 'Hypertension',
                'illness': 'Acute myocardial infarction'
            },
            'generation_metadata': {
                'specialty': 'cardiology',
                'input_symptoms': ['chest_pain', 'shortness_breath'],
                'severity': 'moderate',
                'difficulty_level': 'intermediate'
            }
        }
        
        # Test storage
        success = store_conversation_data(conv_id, 'patient_data', test_patient_data)
        logger.info(f"Patient data storage: {'SUCCESS' if success else 'FAILED'}")
        
        # Test retrieval
        retrieved_data = get_conversation_data(conv_id, 'patient_data')
        logger.info(f"Patient data retrieval: {'SUCCESS' if retrieved_data else 'FAILED'}")
        
        # Test validation
        is_valid, errors = validate_patient_data_structure(test_patient_data)
        logger.info(f"Patient data validation: {'SUCCESS' if is_valid else 'FAILED'} - {errors}")
        
        # Cleanup
        delete_conversation(conv_id)
        logger.info("Test completed successfully")
        
        return True
        
    except Exception as e:
        logger.error(f"Database test failed: {e}")
        return False

if __name__ == "__main__":
    # Run tests if script is executed directly
    test_database_functionality() 