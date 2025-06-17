#!/usr/bin/env python3
"""
Test script for multi-agent conversation system
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_personas_endpoint():
    """Test that we can get the list of personas"""
    print("🔍 Testing personas endpoint...")
    
    response = requests.get(f"{BASE_URL}/api/personas")
    
    if response.status_code == 200:
        data = response.json()
        if data.get('status') == 'success':
            personas = data.get('personas', {})
            print(f"✅ Found {len(personas)} personas:")
            for persona_id, persona_data in personas.items():
                print(f"   - {persona_data['name']}: {persona_data['description']}")
            return list(personas.keys())
        else:
            print(f"❌ Error: {data.get('message', 'Unknown error')}")
            return None
    else:
        print(f"❌ HTTP Error: {response.status_code}")
        return None

def test_multi_agent_creation(persona_ids):
    """Test creating a multi-agent conversation"""
    print("\n🎯 Testing multi-agent conversation creation...")
    
    # Use first 2 personas for testing
    test_agents = persona_ids[:2] if len(persona_ids) >= 2 else persona_ids
    
    if len(test_agents) < 2:
        print("❌ Need at least 2 personas for multi-agent test")
        return None
    
    payload = {
        "agent_ids": test_agents
    }
    
    response = requests.post(
        f"{BASE_URL}/api/multi-agent/create",
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload)
    )
    
    if response.status_code == 200:
        data = response.json()
        if data.get('status') == 'success':
            conversation_id = data.get('conversation_id')
            active_agents = data.get('active_agents', [])
            print(f"✅ Multi-agent conversation created!")
            print(f"   Conversation ID: {conversation_id}")
            print(f"   Active agents: {[agent['name'] for agent in active_agents]}")
            return conversation_id
        else:
            print(f"❌ Error: {data.get('message', 'Unknown error')}")
            return None
    else:
        print(f"❌ HTTP Error: {response.status_code}")
        return None

def test_multi_agent_message(conversation_id):
    """Test sending a message to multi-agent conversation"""
    print("\n💬 Testing multi-agent message processing...")
    
    payload = {
        "message": "Hello everyone! How are you doing today?"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/multi-agent/process-message",
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload)
    )
    
    if response.status_code == 200:
        data = response.json()
        if data.get('status') == 'success':
            user_message = data.get('user_message')
            responses = data.get('responses', [])
            summary = data.get('conversation_summary', {})
            
            print(f"✅ Message processed successfully!")
            print(f"   User said: {user_message}")
            print(f"   Got {len(responses)} responses:")
            
            for i, response in enumerate(responses, 1):
                speaker = response.get('speaker', 'Unknown')
                content = response.get('content', '')
                print(f"   {i}. {speaker}: {content}")
            
            print(f"   Total messages in conversation: {summary.get('message_count', 0)}")
            return True
        else:
            print(f"❌ Error: {data.get('message', 'Unknown error')}")
            return False
    else:
        print(f"❌ HTTP Error: {response.status_code}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Multi-Agent Conversation System Tests\n")
    
    # Test 1: Get personas
    persona_ids = test_personas_endpoint()
    if not persona_ids:
        print("\n❌ Cannot proceed without personas")
        return
    
    # Test 2: Create multi-agent conversation
    conversation_id = test_multi_agent_creation(persona_ids)
    if not conversation_id:
        print("\n❌ Cannot proceed without conversation")
        return
    
    # Test 3: Send a message
    success = test_multi_agent_message(conversation_id)
    
    if success:
        print("\n🎉 All tests passed! Multi-agent system is working!")
        print("\n🔧 You can now test the system in the web interface:")
        print("   1. Open http://localhost:8000 in your browser")
        print("   2. Look for the '🎯 Start Conference Call' button")
        print("   3. Select 2 or more personas and start chatting!")
    else:
        print("\n❌ Some tests failed. Check the logs for more details.")

if __name__ == "__main__":
    main() 