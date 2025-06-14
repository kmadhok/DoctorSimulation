# DoctorSimulation/explore_conversations.py

import sqlite3
import json
import os
from pprint import pprint

DB_PATH = os.path.join(os.path.dirname(__file__), 'conversations.db')

def get_conversations(conn):
    cursor = conn.execute(
        'SELECT id, title, simulation_file, created_at, updated_at FROM conversations ORDER BY updated_at DESC'
    )
    return cursor.fetchall()

def get_messages(conn, conversation_id):
    cursor = conn.execute(
        'SELECT role, content, timestamp FROM messages WHERE conversation_id = ? ORDER BY timestamp',
        (conversation_id,)
    )
    return cursor.fetchall()

def get_patient_data(conn, conversation_id):
    cursor = conn.execute(
        'SELECT data_value, data_type FROM conversation_data WHERE conversation_id = ? AND data_key = "patient_data"',
        (conversation_id,)
    )
    row = cursor.fetchone()
    if not row:
        return None
    data_value, data_type = row
    if data_type == 'json':
        return json.loads(data_value)
    return data_value

def get_highest_conversation_id(conn):
    """Get the highest conversation ID from the database."""
    cursor = conn.execute('SELECT MAX(id) FROM conversations')
    result = cursor.fetchone()
    return result[0] if result[0] is not None else 0

def main():
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    
    # Get and display the highest conversation ID
    highest_id = get_highest_conversation_id(conn)
    print(f"Highest conversation ID: {highest_id}")
    
    print("\n=== All Conversations ===")
    conversations = get_conversations(conn)
    for conv in conversations:
        print(f"\n--- Conversation ID: {conv[0]} ---")
        print(f"Title: {conv[1]}")
        print(f"Simulation: {conv[2]}")
        print(f"Created: {conv[3]}, Updated: {conv[4]}")
        
        # Print transcript
        print("Transcript:")
        messages = get_messages(conn, conv[0])
        for msg in messages:
            print(f"  [{msg[2]}] {msg[0].capitalize()}: {msg[1]}")
        
        # Print patient data
        patient_data = get_patient_data(conn, conv[0])
        if patient_data:
            print("Patient Data:")
            pprint(patient_data)
        else:
            print("No patient data found.")
    conn.close()

def specific_conversation():
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}")
        return

    conversation_id = 35  # <-- Only show this conversation

    conn = sqlite3.connect(DB_PATH)
    
    # Get and display the highest conversation ID
    highest_id = get_highest_conversation_id(conn)
    print(f"Highest conversation ID: {highest_id}")
    
    cursor = conn.execute(
        'SELECT id, title, simulation_file, created_at, updated_at FROM conversations WHERE id = ?',
        (conversation_id,)
    )
    conv = cursor.fetchone()
    if not conv:
        print(f"No conversation found with ID {conversation_id}")
        return

    print(f"\n--- Conversation ID: {conv[0]} ---")
    print(f"Title: {conv[1]}")
    print(f"Simulation: {conv[2]}")
    print(f"Created: {conv[3]}, Updated: {conv[4]}")

    # Print transcript
    print("Transcript:")
    messages = get_messages(conn, conv[0])
    for msg in messages:
        print(f"  [{msg[2]}] {msg[0].capitalize()}: {msg[1]}")

    # Print patient data
    patient_data = get_patient_data(conn, conv[0])
    if patient_data:
        print("Patient Data:")
        pprint(patient_data)
    else:
        print("No patient data found.")
    conn.close()

    return patient_data, messages

if __name__ == "__main__":
    # You can choose which function to run
    # main()  # To see all conversations
    patient_data, messages = specific_conversation()  # To see a specific conversation
    print("patient_data: ", patient_data)
    print("messages: ", messages)