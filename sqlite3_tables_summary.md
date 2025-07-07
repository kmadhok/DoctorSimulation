# SQLite3 Database Tables Summary

## Quick Reference: All Tables and Columns

### Database: `conversations.db`

| Table | Column | Type | Constraints | Purpose |
|-------|--------|------|-------------|---------|
| **conversations** | `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique conversation ID |
| | `title` | TEXT | NOT NULL | Conversation title |
| | `simulation_file` | TEXT | NULL allowed | Associated simulation file |
| | `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Creation time |
| | `updated_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Last update time |
| **messages** | `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique message ID |
| | `conversation_id` | INTEGER | NOT NULL, FK → conversations(id) | Parent conversation |
| | `role` | TEXT | NOT NULL | Message role (user/assistant) |
| | `content` | TEXT | NOT NULL | Message text content |
| | `timestamp` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Message time |
| **conversation_data** | `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique record ID |
| | `conversation_id` | INTEGER | NOT NULL, FK → conversations(id) | Parent conversation |
| | `data_key` | TEXT | NOT NULL | Data key name |
| | `data_value` | TEXT | NOT NULL | Serialized data value |
| | `data_type` | TEXT | DEFAULT 'string' | Type indicator |
| | `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Creation time |
| | `updated_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Last update time |
| **database_version** | `version` | INTEGER | PRIMARY KEY | Schema version number |
| | `applied_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Migration time |
| | `description` | TEXT | NULL allowed | Migration description |

## Total Counts
- **Tables**: 4
- **Columns**: 20
- **Primary Keys**: 4
- **Foreign Keys**: 2 
- **Indexes**: 2
- **Unique Constraints**: 1

## Indexes
1. `idx_conversation_data_lookup` on `conversation_data(conversation_id, data_key)`
2. `idx_messages_conversation` on `messages(conversation_id, timestamp)`

## Relationships
- `messages.conversation_id` → `conversations.id` (CASCADE DELETE)
- `conversation_data.conversation_id` → `conversations.id` (CASCADE DELETE)
- `conversation_data` has UNIQUE constraint on `(conversation_id, data_key)`