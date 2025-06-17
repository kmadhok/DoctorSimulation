#!/usr/bin/env python3
"""
Test runner for all standalone multi-agent tests
"""

import sys
import os
import subprocess
import time
from datetime import datetime

def run_test_script(script_name, description):
    """Run a test script and return success status"""
    print(f"\n{'='*60}")
    print(f"🚀 Running: {description}")
    print(f"📄 Script: {script_name}")
    print(f"⏰ Started: {datetime.now().strftime('%H:%M:%S')}")
    print('='*60)
    
    try:
        start_time = time.time()
        
        # Run the test script
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=False,  # Show output in real-time
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        duration = time.time() - start_time
        
        print(f"\n{'='*60}")
        if result.returncode == 0:
            print(f"✅ {description} PASSED")
        else:
            print(f"❌ {description} FAILED (exit code: {result.returncode})")
        
        print(f"⏱️  Duration: {duration:.2f} seconds")
        print(f"🏁 Finished: {datetime.now().strftime('%H:%M:%S')}")
        print('='*60)
        
        return result.returncode == 0
        
    except FileNotFoundError:
        print(f"❌ Script not found: {script_name}")
        return False
    except Exception as e:
        print(f"❌ Error running {script_name}: {e}")
        return False

def main():
    """Run all test scripts"""
    print("🧪 Multi-Agent System Test Suite")
    print("=" * 70)
    print(f"🕐 Test suite started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # Define test scripts in order of execution
    test_scripts = [
        {
            "script": "test_standalone_persona_system.py",
            "description": "Persona System Tests",
            "critical": True  # If this fails, others likely will too
        },
        {
            "script": "test_standalone_crew_agents.py", 
            "description": "CrewAI Multi-Agent Tests",
            "critical": True
        },
        {
            "script": "test_integration_multi_agent.py",
            "description": "Complete Integration Tests",
            "critical": False  # Integration test, might have minor issues
        }
    ]
    
    results = {}
    critical_failure = False
    
    for test_config in test_scripts:
        script_name = test_config["script"]
        description = test_config["description"]
        is_critical = test_config["critical"]
        
        # Check if script exists
        if not os.path.exists(script_name):
            print(f"\n⚠️  Skipping {script_name} - file not found")
            results[script_name] = False
            continue
        
        # Run the test
        success = run_test_script(script_name, description)
        results[script_name] = success
        
        # Check for critical failures
        if not success and is_critical:
            critical_failure = True
            print(f"\n💥 CRITICAL TEST FAILED: {description}")
            print("   This indicates a fundamental issue with the system.")
            print("   Continuing with remaining tests for diagnosis...")
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST SUITE SUMMARY")
    print("=" * 70)
    
    passed_tests = sum(1 for success in results.values() if success)
    total_tests = len(results)
    
    for script_name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        description = next(
            (test["description"] for test in test_scripts if test["script"] == script_name),
            script_name
        )
        print(f"   {status} {description}")
    
    print(f"\n📈 Results: {passed_tests}/{total_tests} tests passed")
    
    # Overall assessment
    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED!")
        print("   Your multi-agent system is ready for production use.")
        print("   You can confidently deploy the Flask application.")
        
    elif passed_tests >= total_tests * 0.75 and not critical_failure:
        print("✅ MOST TESTS PASSED!")
        print("   Your system is functional with minor issues.")
        print("   Safe to proceed with Flask integration.")
        
    elif critical_failure:
        print("💥 CRITICAL FAILURES DETECTED!")
        print("   Core components have issues that need resolution.")
        print("   Review the failed tests before deploying.")
        
    else:
        print("⚠️  SIGNIFICANT ISSUES FOUND!")
        print("   Multiple components have problems.")
        print("   System needs debugging before deployment.")
    
    # Recommendations
    print(f"\n💡 NEXT STEPS:")
    
    if passed_tests == total_tests:
        print("   1. Start your Flask application: python app.py --port 8000")
        print("   2. Test the multi-agent features in the web interface")
        print("   3. Create some test conversations with multiple personas")
    
    elif passed_tests >= total_tests * 0.75:
        print("   1. Review any failed tests and fix minor issues")
        print("   2. Start Flask app for manual testing: python app.py --port 8000")
        print("   3. Test multi-agent features carefully")
    
    else:
        failed_tests = [name for name, success in results.items() if not success]
        print("   1. Focus on fixing these failed tests:")
        for failed_test in failed_tests:
            print(f"      - {failed_test}")
        print("   2. Check dependencies: pip install crewai")
        print("   3. Verify environment variables are set")
        print("   4. Re-run tests after fixes")
    
    print(f"\n🕐 Test suite completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Return appropriate exit code
    if critical_failure:
        return 2  # Critical failure
    elif passed_tests >= total_tests * 0.75:
        return 0  # Success or acceptable
    else:
        return 1  # General failure

if __name__ == '__main__':
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⏹️  Test suite interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 Unexpected error in test runner: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1) 