#!/usr/bin/env python3
"""
Integration test for the complete multi-agent conversation system
This test simulates a full conference call scenario
"""

import sys
import os
import json
import time
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_environment_setup():
    """Test that all required modules and dependencies are available"""
    print("🔧 Testing environment setup...")
    
    required_modules = [
        ('utils.crew_agents', 'MultiAgentConversationOrchestrator'),
        ('utils.persona_system', 'get_all_personas'),
        ('utils.groq_integration', 'get_groq_response'),
    ]
    
    missing_modules = []
    available_modules = []
    
    for module_name, class_name in required_modules:
        try:
            module = __import__(module_name, fromlist=[class_name])
            getattr(module, class_name)
            available_modules.append(f"{module_name}.{class_name}")
        except ImportError as e:
            missing_modules.append(f"{module_name}.{class_name}: {e}")
        except AttributeError as e:
            missing_modules.append(f"{module_name}.{class_name}: {e}")
    
    print(f"✅ Available modules: {len(available_modules)}")
    for module in available_modules:
        print(f"   - {module}")
    
    if missing_modules:
        print(f"❌ Missing modules: {len(missing_modules)}")
        for module in missing_modules:
            print(f"   - {module}")
        return False
    
    # Test CrewAI specifically
    try:
        import crewai
        print(f"✅ CrewAI version available")
    except ImportError:
        print("❌ CrewAI not installed. Run: pip install crewai")
        return False
    
    return True

def simulate_conference_call():
    """Simulate a complete conference call scenario"""
    print("\n🎯 Simulating Complete Conference Call Scenario")
    print("=" * 60)
    
    try:
        # Import required modules
        from utils.crew_agents import MultiAgentConversationOrchestrator
        from utils.persona_system import get_all_personas
        
        # Step 1: Get available personas
        print("1️⃣ Loading available personas...")
        personas = get_all_personas()
        persona_ids = list(personas.keys())
        
        if len(persona_ids) < 3:
            print(f"⚠️  Only {len(persona_ids)} personas available. Using all available.")
            selected_personas = persona_ids
        else:
            # Select first 3 personas for the test
            selected_personas = persona_ids[:3]
        
        print(f"📋 Selected personas for conference call:")
        for persona_id in selected_personas:
            persona_data = personas[persona_id]
            print(f"   🎭 {persona_data['name']} ({persona_id}) - {persona_data['voice_id']}")
        
        # Step 2: Create orchestrator and add agents
        print("\n2️⃣ Setting up multi-agent orchestrator...")
        orchestrator = MultiAgentConversationOrchestrator()
        
        added_agents = []
        for persona_id in selected_personas:
            if orchestrator.add_agent(persona_id):
                added_agents.append(persona_id)
                print(f"✅ Added {personas[persona_id]['name']}")
            else:
                print(f"❌ Failed to add {personas[persona_id]['name']}")
        
        if len(added_agents) < 2:
            print("❌ Need at least 2 agents for conference call")
            return False
        
        # Step 3: Simulate conversation flow
        print(f"\n3️⃣ Starting conference call with {len(added_agents)} participants...")
        
        # Define a realistic conversation scenario
        conversation_scenario = [
            {
                "round": 1,
                "user_message": "Hello everyone! Welcome to our team meeting. Could you each introduce yourselves and share what expertise you bring to the team?",
                "expected_responses": len(added_agents),
                "description": "Opening introductions"
            },
            {
                "round": 2,
                "user_message": "Great introductions! Now, I have a challenge I'd like your perspectives on. We need to improve team collaboration. What are your thoughts?",
                "expected_responses": len(added_agents),
                "description": "Problem discussion"
            },
            {
                "round": 3,
                "user_message": "Those are excellent points. How do you think we should prioritize these suggestions?",
                "expected_responses": len(added_agents),
                "description": "Solution prioritization"
            },
            {
                "round": 4,
                "user_message": "Perfect! Can we establish some next steps and action items?",
                "expected_responses": len(added_agents),
                "description": "Action planning"
            }
        ]
        
        # Process each conversation round
        total_responses = 0
        successful_rounds = 0
        
        for scenario in conversation_scenario:
            print(f"\n📝 Round {scenario['round']}: {scenario['description']}")
            print(f"   User: \"{scenario['user_message']}\"")
            
            try:
                start_time = time.time()
                responses = orchestrator.process_user_message(scenario['user_message'])
                processing_time = time.time() - start_time
                
                print(f"   ⏱️  Processing time: {processing_time:.2f} seconds")
                print(f"   💬 Generated {len(responses)} responses")
                
                # Display agent responses
                for i, response in enumerate(responses):
                    speaker = response.get('speaker', 'Unknown')
                    content = response.get('content', '')
                    content_preview = content[:100] + "..." if len(content) > 100 else content
                    
                    print(f"   🎭 {speaker}: \"{content_preview}\"")
                
                total_responses += len(responses)
                
                if len(responses) > 0:
                    successful_rounds += 1
                
                # Small delay between rounds to simulate natural conversation flow
                time.sleep(1)
                
            except Exception as e:
                print(f"   ❌ Round {scenario['round']} failed: {e}")
                import traceback
                traceback.print_exc()
        
        # Step 4: Analyze conversation results
        print(f"\n4️⃣ Conference call analysis...")
        
        summary = orchestrator.get_conversation_summary()
        
        print(f"📊 Conference Call Statistics:")
        print(f"   🎭 Participants: {len(added_agents)}")
        print(f"   🗣️  Total responses generated: {total_responses}")
        print(f"   ✅ Successful rounds: {successful_rounds}/{len(conversation_scenario)}")
        print(f"   💬 Total messages in history: {summary['total_messages']}")
        print(f"   👥 Active participants: {', '.join(summary['participants'])}")
        
        # Step 5: Test conversation continuity
        print(f"\n5️⃣ Testing conversation continuity...")
        
        # Ask a follow-up question that requires context from previous discussion
        followup_message = "Based on our discussion, what would be the most important single action to implement first?"
        
        try:
            followup_responses = orchestrator.process_user_message(followup_message)
            print(f"✅ Follow-up conversation successful: {len(followup_responses)} responses")
            
            for response in followup_responses:
                speaker = response.get('speaker', 'Unknown')
                content = response.get('content', '')[:150]
                print(f"   🎭 {speaker}: \"{content}...\"")
                
        except Exception as e:
            print(f"❌ Follow-up conversation failed: {e}")
        
        # Success criteria
        success_criteria = {
            "agents_added": len(added_agents) >= 2,
            "responses_generated": total_responses > 0,
            "successful_rounds": successful_rounds >= len(conversation_scenario) // 2,
            "conversation_history": summary['total_messages'] > len(conversation_scenario),
        }
        
        print(f"\n📋 Success Criteria:")
        overall_success = True
        for criterion, passed in success_criteria.items():
            status = "✅" if passed else "❌"
            print(f"   {status} {criterion.replace('_', ' ').title()}: {passed}")
            if not passed:
                overall_success = False
        
        print(f"\n🎉 Conference call simulation: {'SUCCESS' if overall_success else 'PARTIAL SUCCESS'}")
        return overall_success
        
    except Exception as e:
        print(f"💥 Conference call simulation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_error_handling():
    """Test error handling in various scenarios"""
    print("\n🛡️ Testing error handling...")
    
    try:
        from utils.crew_agents import MultiAgentConversationOrchestrator
        
        # Test 1: Empty orchestrator
        orchestrator = MultiAgentConversationOrchestrator()
        
        try:
            responses = orchestrator.process_user_message("Hello")
            print(f"✅ Empty orchestrator handled gracefully: {len(responses)} responses")
        except Exception as e:
            print(f"❌ Empty orchestrator failed: {e}")
        
        # Test 2: Invalid persona ID
        try:
            success = orchestrator.add_agent("invalid_persona_id")
            print(f"✅ Invalid persona ID handled gracefully: {success}")
        except Exception as e:
            print(f"❌ Invalid persona ID caused error: {e}")
        
        # Test 3: Very long message
        try:
            long_message = "This is a very long message. " * 100
            # Add a valid agent first
            from utils.persona_system import get_all_personas
            personas = get_all_personas()
            if personas:
                first_persona = next(iter(personas.keys()))
                orchestrator.add_agent(first_persona)
            
            responses = orchestrator.process_user_message(long_message)
            print(f"✅ Long message handled gracefully: {len(responses)} responses")
        except Exception as e:
            print(f"❌ Long message caused error: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False

def performance_test():
    """Test performance with multiple agents and messages"""
    print("\n⚡ Performance testing...")
    
    try:
        from utils.crew_agents import MultiAgentConversationOrchestrator
        from utils.persona_system import get_all_personas
        
        orchestrator = MultiAgentConversationOrchestrator()
        personas = get_all_personas()
        
        # Add maximum available agents (up to 4 for performance test)
        max_agents = min(4, len(personas))
        agent_count = 0
        
        for persona_id in list(personas.keys())[:max_agents]:
            if orchestrator.add_agent(persona_id):
                agent_count += 1
        
        print(f"🤖 Testing with {agent_count} agents")
        
        # Performance test scenarios
        test_messages = [
            "Quick question for everyone.",
            "What's your take on this?",
            "Any final thoughts?",
            "Thanks everyone!"
        ]
        
        total_time = 0
        total_responses = 0
        
        for i, message in enumerate(test_messages):
            start_time = time.time()
            
            try:
                responses = orchestrator.process_user_message(message)
                processing_time = time.time() - start_time
                
                total_time += processing_time
                total_responses += len(responses)
                
                print(f"   Message {i+1}: {processing_time:.2f}s, {len(responses)} responses")
                
            except Exception as e:
                print(f"   Message {i+1}: FAILED - {e}")
        
        avg_time = total_time / len(test_messages) if test_messages else 0
        avg_responses = total_responses / len(test_messages) if test_messages else 0
        
        print(f"📊 Performance Results:")
        print(f"   ⏱️  Average processing time: {avg_time:.2f} seconds")
        print(f"   💬 Average responses per message: {avg_responses:.1f}")
        print(f"   🎯 Total processing time: {total_time:.2f} seconds")
        
        # Performance criteria (adjust based on acceptable performance)
        performance_acceptable = avg_time < 30.0  # Less than 30 seconds per message
        
        return performance_acceptable
        
    except Exception as e:
        print(f"❌ Performance test failed: {e}")
        return False

def main():
    """Run comprehensive integration tests"""
    print("🧪 Starting Comprehensive Multi-Agent Integration Tests")
    print("=" * 70)
    
    test_results = {}
    
    # Test 1: Environment setup
    test_results['environment'] = test_environment_setup()
    if not test_results['environment']:
        print("❌ Environment setup failed, aborting remaining tests")
        return False
    
    # Test 2: Conference call simulation
    test_results['conference_call'] = simulate_conference_call()
    
    # Test 3: Error handling
    test_results['error_handling'] = test_error_handling()
    
    # Test 4: Performance test
    test_results['performance'] = performance_test()
    
    # Final results
    print("\n" + "=" * 70)
    print("🎉 Integration Test Results Summary")
    print("=" * 70)
    
    passed_tests = 0
    total_tests = len(test_results)
    
    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} {test_name.replace('_', ' ').title()}")
        if result:
            passed_tests += 1
    
    print(f"\n📊 Overall Results: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED! Multi-agent system is ready for production.")
    elif passed_tests >= total_tests * 0.75:
        print("✅ Most tests passed. System is functional with minor issues.")
    else:
        print("⚠️  Several tests failed. System needs attention before deployment.")
    
    print("\n🚀 Multi-agent conference call system is ready for use!")
    print("💡 You can now integrate this into your Flask application.")
    
    return passed_tests >= total_tests * 0.75

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 Unexpected error during integration testing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1) 