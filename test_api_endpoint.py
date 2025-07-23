#!/usr/bin/env python3
"""
Test script for the new user profile summary API endpoint
"""
import sys
import os
import json

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the Flask app
from app import app

def test_user_profile_summary_endpoint():
    """Test the /api/user-profile-summary endpoint"""
    print("Testing /api/user-profile-summary endpoint...")
    
    try:
        # Test the API endpoint within the app context
        with app.test_client() as client:
            response = client.get('/api/user-profile-summary')
            
            print(f"Response Status: {response.status_code}")
            print(f"Response Headers: {dict(response.headers)}")
            
            response_data = response.get_json()
            print(f"Response Data: {json.dumps(response_data, indent=2)}")
            
            # Test different scenarios
            if response.status_code == 200:
                print("✅ Endpoint is working correctly!")
                
                # Check response structure
                if 'status' in response_data:
                    print(f"✅ Status: {response_data['status']}")
                    
                if 'analysis_type' in response_data:
                    print(f"✅ Analysis Type: {response_data['analysis_type']}")
                    
                if 'data' in response_data:
                    print(f"✅ Data keys: {list(response_data['data'].keys())}")
                    
            else:
                print(f"⚠️  Endpoint returned error status: {response.status_code}")
                if response_data:
                    print(f"Error message: {response_data.get('message', 'No error message')}")
                    
    except Exception as e:
        print(f"❌ Error testing endpoint: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_user_profile_summary_endpoint()