# SQLite3 Database Tables Specification

## Database: `conversations.db`

This document provides the exact specification of all tables and columns in the SQLite3 database.

---

## Table 1: `conversations`

**Purpose**: Stores conversation metadata including titles and associated simulation files.

### Columns:
| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| `id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | Unique conversation identifier |
| `title` | `TEXT` | `NOT NULL` | Human-readable conversation title |
| `simulation_file` | `TEXT` | `NULL` allowed | Path/name of associated simulation file |
| `created_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | Record creation timestamp |
| `updated_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | Last modification timestamp |

### SQL Definition:
```sql
CREATE TABLE IF NOT EXISTS conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    simulation_file TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

---

## Table 2: `messages`

**Purpose**: Stores individual messages within conversations with role-based classification.

### Columns:
| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| `id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | Unique message identifier |
| `conversation_id` | `INTEGER` | `NOT NULL`, `FOREIGN KEY` | References `conversations(id)` |
| `role` | `TEXT` | `NOT NULL` | Message role (e.g., 'user', 'assistant') |
| `content` | `TEXT` | `NOT NULL` | Message content/text |
| `timestamp` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | Message creation timestamp |

### Relationships:
- **Foreign Key**: `conversation_id` → `conversations(id)` `ON DELETE CASCADE`

### SQL Definition:
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

---

## Table 3: `conversation_data`

**Purpose**: Stores additional key-value data associated with conversations (patient data, voice settings, etc.).

### Columns:
| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| `id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | Unique record identifier |
| `conversation_id` | `INTEGER` | `NOT NULL`, `FOREIGN KEY` | References `conversations(id)` |
| `data_key` | `TEXT` | `NOT NULL` | Key name for the stored data |
| `data_value` | `TEXT` | `NOT NULL` | Serialized data value |
| `data_type` | `TEXT` | `DEFAULT 'string'` | Data type indicator ('string', 'json', 'number', 'boolean') |
| `created_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | Record creation timestamp |
| `updated_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | Last modification timestamp |

### Constraints:
- **Unique Constraint**: `UNIQUE(conversation_id, data_key)` - Prevents duplicate keys per conversation

### Relationships:
- **Foreign Key**: `conversation_id` → `conversations(id)` `ON DELETE CASCADE`

### SQL Definition:
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

---

## Table 4: `database_version`

**Purpose**: Tracks database schema versions for migration management.

### Columns:
| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| `version` | `INTEGER` | `PRIMARY KEY` | Database schema version number |
| `applied_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | Migration application timestamp |
| `description` | `TEXT` | `NULL` allowed | Description of migration changes |

### SQL Definition:
```sql
CREATE TABLE IF NOT EXISTS database_version (
    version INTEGER PRIMARY KEY,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT
)
```

---

## Database Indexes

### Index 1: `idx_conversation_data_lookup`
**Purpose**: Optimizes queries for conversation data retrieval
**Target**: `conversation_data(conversation_id, data_key)`
```sql
CREATE INDEX IF NOT EXISTS idx_conversation_data_lookup 
ON conversation_data(conversation_id, data_key)
```

### Index 2: `idx_messages_conversation`
**Purpose**: Optimizes message retrieval by conversation and chronological order
**Target**: `messages(conversation_id, timestamp)`
```sql
CREATE INDEX IF NOT EXISTS idx_messages_conversation 
ON messages(conversation_id, timestamp)
```

---

## Data Types Used in `conversation_data.data_type`

The `data_type` column in `conversation_data` supports the following values:

| Data Type | Description | Storage Format | Example Values |
|-----------|-------------|----------------|----------------|
| `'string'` | Text/string data | Direct text storage | "Fritz-PlayAI", "Custom prompt text" |
| `'json'` | Complex objects/arrays | JSON-serialized string | `{"type": "ai_generated", "details": {...}}` |
| `'number'` | Numeric values | String representation | "42", "3.14159" |
| `'boolean'` | Boolean values | String representation | "true", "false" |

---

## Migration History

### Version 1 Migration
**Changes Applied**:
- Added `data_type` column to `conversation_data` table
- Added `created_at` column to `conversation_data` table  
- Added `updated_at` column to `conversation_data` table
- Enhanced data type tracking and timestamps

### Version 2 Migration  
**Changes Applied**:
- AI-generated patient data support
- Migration of legacy custom patient data to new structure
- Enhanced metadata tracking for patient data

---

## Relationships Diagram

```
conversations (1) ──────┐
    │                   │
    │ (1:N)             │ (1:N)
    ▼                   ▼
messages            conversation_data
    │                   │
    └─── conversation_id ────┘
         (Foreign Key)

database_version (standalone)
```

---

## Common Data Keys in `conversation_data`

Based on the application code, common `data_key` values include:

| Key | Purpose | Data Type |
|-----|---------|-----------|
| `"patient_data"` | Patient simulation information | `json` |
| `"voice_id"` | Voice preference for TTS | `string` |
| `"active_agents"` | Multi-agent system state | `json` |
| `"custom_patient"` | Custom patient configurations | `json` |

---

## Summary

- **4 Tables Total**: conversations, messages, conversation_data, database_version
- **20 Columns Total**: Across all tables
- **2 Indexes**: For query optimization
- **3 Foreign Key Relationships**: All with CASCADE delete
- **1 Unique Constraint**: conversation_data(conversation_id, data_key)
- **Current Schema Version**: 2
- **Migration Support**: Full versioning and rollback capability