"""
This script tests if the requests patching for Groq API works correctly.
It tries to make API calls with and without the patch.
"""

import os
import sys
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Groq API key from environment
api_key = os.environ.get('GROQ_API_KEY')
if not api_key:
    print("Error: GROQ_API_KEY not set in environment variables")
    sys.exit(1)

print("Testing Groq API with requests...")

# First, test without the patch
print("\n1. Testing WITHOUT the patch:")
try:
    # Make a simple call to the chat completions API
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say hello!"}
        ]
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        response_data = response.json()
        print("SUCCESS: Made API call to Groq without patch")
        print(f"Response: {response_data['choices'][0]['message']['content']}")
    else:
        print(f"FAILED: API call failed: Status {response.status_code}")
        print(f"Response: {response.text}")
except Exception as e:
    print(f"FAILED: Could not make API call: {str(e)}")

# Now, test with the patch
print("\n2. Testing WITH the patch:")
try:
    # Import and apply the patch
    from utils.patch_groq import patch_successful
    
    if patch_successful:
        print("Patch was applied successfully")
        
        # Make the same API call again
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            response_data = response.json()
            print("SUCCESS: Made API call to Groq with patch")
            print(f"Response: {response_data['choices'][0]['message']['content']}")
        else:
            print(f"FAILED: API call failed: Status {response.status_code}")
            print(f"Response: {response.text}")
    else:
        print("FAILED: Patch could not be applied")
        
except Exception as e:
    print(f"FAILED: Error testing with patch: {str(e)}")

# Testing text-to-speech endpoint
print("\n3. Testing TTS endpoint:")
try:
    from utils.groq_tts_speech import generate_speech_audio
    
    # Generate speech from a short text
    audio_bytes = generate_speech_audio("Hello, this is a test of the text to speech API.")
    
    if audio_bytes:
        # Save to a test file
        with open("test_tts.wav", "wb") as f:
            f.write(audio_bytes)
        print(f"SUCCESS: Generated speech audio, saved to test_tts.wav ({len(audio_bytes)} bytes)")
    else:
        print("FAILED: Could not generate speech audio")
except Exception as e:
    print(f"FAILED: Error testing TTS endpoint: {str(e)}")

print("\nTest completed.") 