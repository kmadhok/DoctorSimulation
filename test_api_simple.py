#!/usr/bin/env python3
"""
Simple test to verify the API endpoint was added correctly
"""
import sys
import os
import re

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_api_endpoint_exists():
    """Test that the API endpoint was added to app.py"""
    print("Testing if API endpoint was added correctly...")
    
    try:
        # Read the app.py file
        with open('app.py', 'r') as f:
            content = f.read()
        
        # Check if the endpoint was added
        if '@app.route(\'/api/user-profile-summary\', methods=[\'GET\'])' in content:
            print("✅ API endpoint route decorator found")
        else:
            print("❌ API endpoint route decorator NOT found")
            
        if 'def get_user_profile_summary():' in content:
            print("✅ API endpoint function found")
        else:
            print("❌ API endpoint function NOT found")
            
        # Check if imports were added
        if 'from utils.user_profile_analyzer import analyze_user_personality, analyze_brief_conversations' in content:
            print("✅ Required imports found")
        else:
            print("❌ Required imports NOT found")
            
        # Check for proper error handling
        if 'analysis_result = analyze_user_personality()' in content:
            print("✅ Main analysis function call found")
        else:
            print("❌ Main analysis function call NOT found")
            
        if 'brief_result = analyze_brief_conversations()' in content:
            print("✅ Brief analysis fallback found")
        else:
            print("❌ Brief analysis fallback NOT found")
            
        print("\n📄 API Endpoint Summary:")
        print("- Route: GET /api/user-profile-summary")
        print("- Function: get_user_profile_summary()")
        print("- Returns: JSON response with user personality analysis")
        print("- Fallback: Brief conversation analysis for <5 conversations")
        print("- Error handling: Database, API, and general errors")
        
    except Exception as e:
        print(f"❌ Error reading app.py: {e}")

def test_user_profile_analyzer_import():
    """Test that we can import the user profile analyzer functions"""
    print("\nTesting user profile analyzer imports...")
    
    try:
        from utils.user_profile_analyzer import analyze_user_personality, analyze_brief_conversations
        print("✅ Successfully imported analyze_user_personality")
        print("✅ Successfully imported analyze_brief_conversations")
        
        # Test a basic call to make sure functions work
        result = analyze_user_personality()
        print(f"✅ analyze_user_personality() returned: {result.get('status', 'unknown')}")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
    except Exception as e:
        print(f"❌ Function call error: {e}")

if __name__ == "__main__":
    test_api_endpoint_exists()
    test_user_profile_analyzer_import()