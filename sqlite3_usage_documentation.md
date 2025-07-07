# SQLite3 Database Usage Documentation

This document provides a comprehensive overview of all SQLite3 database usage within the workspace.

## Overview

The application uses SQLite3 as its primary database for storing conversation data, messages, and associated metadata. The database implementation is centralized in the `utils/database.py` module with comprehensive testing and integration throughout the application.

## Database Files

### Primary Database
- **File**: `conversations.db` (located in project root)
- **Purpose**: Main application database storing all conversation and message data
- **Size**: ~380KB (as observed in workspace)

### Backup Files
- **Pattern**: `conversations_backup_YYYYMMDD_HHMMSS.db`
- **Purpose**: Automated backups created by the backup system
- **Location**: Project root directory

## Database Schema

The database consists of 4 main tables with version tracking and migration support:

### 1. conversations
```sql
CREATE TABLE IF NOT EXISTS conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    simulation_file TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```
**Purpose**: Stores conversation metadata including titles and associated simulation files.

### 2. messages
```sql
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id INTEGER NOT NULL,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
)
```
**Purpose**: Stores individual messages within conversations with role-based classification.

### 3. conversation_data
```sql
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
```
**Purpose**: Stores additional key-value data associated with conversations (patient data, voice settings, etc.).

### 4. database_version
```sql
CREATE TABLE IF NOT EXISTS database_version (
    version INTEGER PRIMARY KEY,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT
)
```
**Purpose**: Tracks database schema versions for migration management.

## Database Indexes

Performance optimization indexes:
- `idx_conversation_data_lookup` on `conversation_data(conversation_id, data_key)`
- `idx_messages_conversation` on `messages(conversation_id, timestamp)`

## Core Database Module (`utils/database.py`)

### Key Components

**Database Configuration**:
- `DB_PATH`: Database file path (`conversations.db` in project root)
- `DATABASE_VERSION`: Current schema version (v2)

**Core Functions**:

1. **Initialization**
   - `init_db()`: Creates tables and applies migrations
   - `_check_and_apply_migrations()`: Handles schema versioning
   - `_migrate_to_version_1()` / `_migrate_to_version_2()`: Version-specific migrations

2. **Conversation Management**
   - `create_conversation(title, simulation_file=None)`: Creates new conversations
   - `get_conversations()`: Retrieves all conversations ordered by update time
   - `get_conversation(conversation_id)`: Gets specific conversation with messages
   - `delete_conversation(conversation_id)`: Removes conversation and associated data
   - `update_conversation_title(conversation_id, new_title)`: Updates conversation titles

3. **Message Management**
   - `add_message(conversation_id, role, content)`: Adds messages to conversations

4. **Data Storage System**
   - `store_conversation_data(conversation_id, data_key, data_value)`: Enhanced JSON/typed storage
   - `get_conversation_data(conversation_id, data_key)`: Retrieves with type restoration
   - `get_all_conversation_data(conversation_id)`: Gets all data for a conversation

5. **Database Maintenance**
   - `backup_database(backup_path=None)`: Creates database backups
   - `restore_database(backup_path)`: Restores from backup files
   - `cleanup_old_data(days_older_than=30)`: Removes old conversation data
   - `validate_patient_data_structure()`: Validates patient data format

### SQLite3 Connection Patterns

**Standard Connection Pattern**:
```python
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
# ... database operations ...
conn.commit()
conn.close()
```

**Enhanced Row Factory Usage**:
```python
conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row  # Enables column access by name
cursor = conn.cursor()
```

**Error Handling**:
```python
try:
    # database operations
except sqlite3.Error as e:
    logger.error(f"Database error: {e}")
    return False
```

## Application Integration (`app.py`)

### Database Import and Usage
```python
from utils.database import (
    init_db, create_conversation, add_message, get_conversations, 
    get_conversation, delete_conversation, update_conversation_title, 
    store_conversation_data, get_conversation_data, validate
)
```

### Key Integration Points

1. **Application Startup**: Database initialization on app launch
2. **Conversation Management**: REST API endpoints for conversation CRUD operations
3. **Message Processing**: Audio transcription and response storage
4. **Patient Data Storage**: AI-generated and custom patient information
5. **Voice Settings**: Voice ID preferences per conversation
6. **Multi-Agent Data**: Agent state and orchestration data

### Database Usage in App Routes

**Conversation Endpoints**:
- `/api/conversations/new` - Creates new conversations
- `/api/conversations/<id>` - Retrieves specific conversations
- `/api/conversations/<id>/update-title` - Updates conversation titles
- `/api/conversations/<id>/delete` - Deletes conversations

**Audio Processing**:
- `/process_audio` - Stores transcriptions and responses
- Message history integration for context

## Testing Infrastructure

### Test Files Using SQLite3

#### 1. `tests/test_database.py`
**Purpose**: Unit tests for database functions
**SQLite3 Usage**:
- Temporary database creation for isolated testing
- Direct SQLite3 connections for verification
- Tests all CRUD operations

**Key Test Patterns**:
```python
@pytest.fixture
def test_db():
    fd, temp_path = tempfile.mkstemp()
    os.close(fd)
    utils.database.DB_PATH = temp_path  # Override for testing
    init_db()
    yield temp_path
    utils.database.DB_PATH = original_path  # Reset
    os.unlink(temp_path)  # Cleanup
```

#### 2. `tests/test_conversations.py`
**Purpose**: Integration tests for conversation API endpoints
**SQLite3 Usage**:
- Flask test client with temporary database
- Database state verification
- API endpoint testing with database integration

### Testing Patterns

**Temporary Database Setup**:
- Uses `tempfile.mkstemp()` for isolated test databases
- Overrides `DB_PATH` during tests
- Automatic cleanup after test completion

**Direct SQLite3 Verification**:
```python
conn = sqlite3.connect(test_db)
cursor = conn.cursor()
cursor.execute("SELECT id, title FROM conversations WHERE id = ?", (conversation_id,))
result = cursor.fetchone()
conn.close()
```

## Database Versioning and Migrations

### Current Version: 2

**Version 1 Migration**:
- Added `data_type`, `created_at`, `updated_at` columns to `conversation_data`
- Enhanced data type tracking and timestamps

**Version 2 Migration**:
- AI-generated patient data support
- Migration of legacy custom patient data to new structure
- Enhanced metadata tracking

### Migration Safety Features
- Pre-migration validation
- Rollback capability through backup system
- Comprehensive logging of migration process
- Graceful handling of missing columns

## Error Handling and Logging

### Error Patterns
- `sqlite3.Error` catching for database-specific errors
- Graceful degradation when database operations fail
- Comprehensive logging of all database operations

### Logging Integration
```python
logger.error(f"Database error storing conversation data: {e}")
logger.info(f"Database backup created successfully: {backup_path}")
logger.debug(f"Retrieved patient data from database for conversation {current_conversation_id}")
```

## Data Types and JSON Handling

### Enhanced Type System
- **String**: Default text storage
- **JSON**: Complex objects (dicts, lists) with validation
- **Number**: Integer and float values
- **Boolean**: True/false values with proper conversion

### JSON Storage Pattern
```python
# Storage with type detection
if isinstance(data_value, (dict, list)):
    json_value = json.dumps(data_value, ensure_ascii=False)
    data_type = 'json'

# Retrieval with type restoration
if data_type == 'json':
    return json.loads(data_value)
```

## Performance Considerations

### Optimization Features
- **Connection Management**: Proper connection opening/closing
- **Indexes**: Strategic indexing for common query patterns
- **Row Factory**: Efficient column access by name
- **Batch Operations**: Efficient bulk data operations

### Connection Patterns
- Short-lived connections for individual operations
- Immediate commit and close for data consistency
- Row factory usage for structured data access

## Security Considerations

### SQL Injection Prevention
- **Parameterized Queries**: All user input uses parameter binding
- **No String Concatenation**: Avoiding dynamic SQL construction
- **Input Validation**: Data validation before database operations

**Example Safe Query Pattern**:
```python
cursor.execute(
    'INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)',
    (conversation_id, role, content)
)
```

## File Dependencies

### Direct SQLite3 Usage Files
1. **`utils/database.py`** - Core database module (22 sqlite3 references)
2. **`tests/test_database.py`** - Database unit tests (2 sqlite3 imports)
3. **`tests/test_conversations.py`** - Integration tests (1 sqlite3 import)

### Indirect Usage Files
1. **`app.py`** - Main application with database integration (30+ database references)
2. **`PHASE_4_1_IMPLEMENTATION.md`** - Documentation referencing database features

## Summary Statistics

- **Total SQLite3 Direct References**: 25+ across 3 Python files
- **Database Functions**: 15+ core database functions
- **Tables**: 4 main tables with relationships
- **Indexes**: 2 performance optimization indexes
- **Migration Versions**: 2 schema versions with upgrade path
- **Test Coverage**: Comprehensive unit and integration tests
- **Error Handling**: Robust error handling throughout
- **Data Types**: 4 supported data types (string, json, number, boolean)

The SQLite3 implementation provides a robust, tested, and scalable foundation for the application's data persistence needs with proper versioning, migration support, and comprehensive error handling.