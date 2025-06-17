#!/usr/bin/env python3
"""
Standalone test for the CrewAI multi-agent conversation system
"""

import sys
import os
import json
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from utils.crew_agents import MultiAgentConversationOrchestrator
    from utils.persona_system import get_all_personas, get_persona_by_id
    print("✅ Successfully imported multi-agent modules")
except ImportError as e:
    print(f"❌ Failed to import multi-agent modules: {e}")
    print("   Make sure CrewAI is installed: pip install crewai")
    sys.exit(1)

def test_orchestrator_initialization():
    """Test creating a MultiAgentConversationOrchestrator"""
    print("\n🔍 Testing MultiAgentConversationOrchestrator initialization...")
    
    try:
        orchestrator = MultiAgentConversationOrchestrator()
        assert orchestrator is not None, "Orchestrator creation failed"
        assert hasattr(orchestrator, 'agents'), "Orchestrator missing agents attribute"
        assert hasattr(orchestrator, 'crew'), "Orchestrator missing crew attribute"
        assert hasattr(orchestrator, 'conversation_history'), "Orchestrator missing conversation_history attribute"
        
        print("✅ MultiAgentConversationOrchestrator created successfully")
        print(f"   Initial agents count: {len(orchestrator.agents)}")
        print(f"   Initial conversation history: {len(orchestrator.conversation_history)} messages")
        
        return True, orchestrator
    except Exception as e:
        print(f"❌ Failed to create orchestrator: {e}")
        import traceback
        traceback.print_exc()
        return False, None

def test_add_agents(orchestrator):
    """Test adding agents to the orchestrator"""
    print("\n🔍 Testing adding agents to orchestrator...")
    
    try:
        # Get available personas
        personas = get_all_personas()
        persona_ids = list(personas.keys())
        
        if len(persona_ids) < 2:
            print(f"⚠️  Only {len(persona_ids)} personas available, need at least 2 for testing")
            return False
        
        # Test adding first two personas
        test_personas = persona_ids[:2]
        added_count = 0
        
        for persona_id in test_personas:
            try:
                success = orchestrator.add_agent(persona_id)
                if success:
                    persona_data = get_persona_by_id(persona_id)
                    print(f"✅ Added agent: {persona_data['name']} ({persona_id})")
                    added_count += 1
                else:
                    print(f"❌ Failed to add agent: {persona_id}")
            except Exception as e:
                print(f"❌ Error adding agent {persona_id}: {e}")
        
        print(f"📊 Successfully added {added_count}/{len(test_personas)} agents")
        print(f"   Total agents in orchestrator: {len(orchestrator.agents)}")
        
        return added_count >= 2
        
    except Exception as e:
        print(f"❌ Error in add_agents test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_agent_creation_details(orchestrator):
    """Test the details of created agents"""
    print("\n🔍 Testing agent creation details...")
    
    try:
        if not orchestrator.agents:
            print("⚠️  No agents to test")
            return False
        
        valid_agents = 0
        
        for agent_info in orchestrator.agents.values():
            try:
                agent = agent_info['agent']
                persona_data = agent_info['persona_data']
                
                # Check agent has required attributes
                assert hasattr(agent, 'role'), "Agent missing role"
                assert hasattr(agent, 'goal'), "Agent missing goal"
                assert hasattr(agent, 'backstory'), "Agent missing backstory"
                
                # Check persona data
                assert 'name' in persona_data, "Persona data missing name"
                assert 'voice_id' in persona_data, "Persona data missing voice_id"
                
                print(f"✅ Agent '{persona_data['name']}' created correctly")
                print(f"   Role: {agent.role[:60]}...")
                print(f"   Voice: {persona_data['voice_id']}")
                
                valid_agents += 1
                
            except Exception as e:
                print(f"❌ Agent validation failed: {e}")
        
        print(f"📊 Valid agents: {valid_agents}/{len(orchestrator.agents)}")
        return valid_agents == len(orchestrator.agents)
        
    except Exception as e:
        print(f"❌ Error in agent details test: {e}")
        return False

def test_conversation_processing(orchestrator):
    """Test processing a message through the multi-agent system"""
    print("\n🔍 Testing conversation processing...")
    
    try:
        if len(orchestrator.agents) < 2:
            print("⚠️  Need at least 2 agents for conversation testing")
            return False
        
        # Test message
        test_message = "Hello everyone! I'd like to introduce myself and hear about your backgrounds."
        
        print(f"📝 Processing test message: '{test_message}'")
        
        # Process the message
        responses = orchestrator.process_user_message(test_message)
        
        assert isinstance(responses, list), f"Expected list of responses, got {type(responses)}"
        assert len(responses) > 0, "No responses generated"
        
        print(f"✅ Generated {len(responses)} responses")
        
        # Validate response structure
        valid_responses = 0
        for i, response in enumerate(responses):
            try:
                assert isinstance(response, dict), f"Response {i} is not a dict"
                required_fields = ['speaker', 'content', 'agent_id', 'voice_id']
                
                for field in required_fields:
                    assert field in response, f"Response {i} missing field '{field}'"
                
                assert isinstance(response['content'], str), f"Response {i} content is not string"
                assert len(response['content']) > 0, f"Response {i} content is empty"
                
                print(f"✅ Response {i+1}: {response['speaker']} ({len(response['content'])} chars)")
                print(f"   Preview: {response['content'][:100]}...")
                
                valid_responses += 1
                
            except Exception as e:
                print(f"❌ Response {i} validation failed: {e}")
        
        print(f"📊 Valid responses: {valid_responses}/{len(responses)}")
        
        # Test conversation history
        history_length = len(orchestrator.conversation_history)
        expected_length = 1 + len(responses)  # user message + agent responses
        
        print(f"📚 Conversation history: {history_length} messages (expected ~{expected_length})")
        
        return valid_responses == len(responses) and history_length > 0
        
    except Exception as e:
        print(f"❌ Error in conversation processing test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_conversation_summary(orchestrator):
    """Test getting conversation summary"""
    print("\n🔍 Testing conversation summary...")
    
    try:
        summary = orchestrator.get_conversation_summary()
        
        assert isinstance(summary, dict), f"Expected dict summary, got {type(summary)}"
        
        expected_fields = ['total_messages', 'participants', 'recent_messages']
        for field in expected_fields:
            assert field in summary, f"Summary missing field '{field}'"
        
        print(f"✅ Conversation summary generated")
        print(f"   Total messages: {summary['total_messages']}")
        print(f"   Participants: {len(summary['participants'])}")
        print(f"   Recent messages: {len(summary['recent_messages'])}")
        
        # List participants
        for participant in summary['participants']:
            print(f"   👤 {participant}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in conversation summary test: {e}")
        return False

def test_multiple_conversations(orchestrator):
    """Test multiple conversation rounds"""
    print("\n🔍 Testing multiple conversation rounds...")
    
    try:
        test_messages = [
            "What are your areas of expertise?",
            "How do you typically approach problem-solving?",
            "What's your opinion on collaboration?"
        ]
        
        all_successful = True
        
        for i, message in enumerate(test_messages):
            try:
                print(f"\n📝 Round {i+1}: '{message}'")
                responses = orchestrator.process_user_message(message)
                
                if len(responses) > 0:
                    print(f"✅ Round {i+1}: {len(responses)} responses generated")
                else:
                    print(f"❌ Round {i+1}: No responses generated")
                    all_successful = False
                    
            except Exception as e:
                print(f"❌ Round {i+1} failed: {e}")
                all_successful = False
        
        total_messages = len(orchestrator.conversation_history)
        print(f"\n📚 Final conversation history: {total_messages} messages")
        
        return all_successful
        
    except Exception as e:
        print(f"❌ Error in multiple conversations test: {e}")
        return False

def main():
    """Run all multi-agent tests"""
    print("🧪 Starting Standalone CrewAI Multi-Agent Tests")
    print("=" * 60)
    
    # Test 1: Initialize orchestrator
    success, orchestrator = test_orchestrator_initialization()
    if not success:
        print("❌ Orchestrator initialization failed, aborting tests")
        return False
    
    # Test 2: Add agents
    success = test_add_agents(orchestrator)
    if not success:
        print("❌ Agent addition failed, aborting tests")
        return False
    
    # Test 3: Validate agent details
    success = test_agent_creation_details(orchestrator)
    if not success:
        print("⚠️  Some agent creation issues found")
    
    # Test 4: Process conversation
    success = test_conversation_processing(orchestrator)
    if not success:
        print("⚠️  Conversation processing has issues")
    
    # Test 5: Get conversation summary
    success = test_conversation_summary(orchestrator)
    if not success:
        print("⚠️  Conversation summary has issues")
    
    # Test 6: Multiple conversation rounds
    success = test_multiple_conversations(orchestrator)
    if not success:
        print("⚠️  Multiple conversations have issues")
    
    print("\n" + "=" * 60)
    print("🎉 Multi-agent tests completed!")
    
    # Final summary
    final_summary = orchestrator.get_conversation_summary()
    print(f"\n📊 Final Test Results:")
    print(f"   🤖 Active agents: {len(orchestrator.agents)}")
    print(f"   💬 Total messages: {final_summary['total_messages']}")
    print(f"   👥 Participants: {', '.join(final_summary['participants'])}")
    
    return True

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 Unexpected error during testing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1) 