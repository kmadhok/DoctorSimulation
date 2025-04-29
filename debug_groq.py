"""
Debug script to test the Groq client initialization and patching.
"""
import os
import sys
import traceback
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("Step 1: Clearing proxy environment variables...")
# Clear proxy environment variables
for var in ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy']:
    if var in os.environ:
        print(f"Removing {var} from environment")
        os.environ.pop(var)

print("\nStep 2: Patching Groq client...")
# Try to import and patch the Groq client
try:
    from groq.client import Client
    
    # Store original __init__ method
    original_groq_init = Client.__init__
    
    # Define patched init method that filters out proxies
    def patched_groq_init(self, *args, **kwargs):
        print(f"Groq Client.__init__ called with args: {args}, kwargs: {kwargs}")
        # Remove proxies if present
        if 'proxies' in kwargs:
            print(f"Removing 'proxies' from kwargs: {kwargs['proxies']}")
            del kwargs['proxies']
        result = original_groq_init(self, *args, **kwargs)
        print("Groq Client.__init__ completed successfully")
        return result
    
    # Apply the patch
    Client.__init__ = patched_groq_init
    print("Successfully patched Groq Client.__init__")
except Exception as e:
    print(f"Failed to patch Groq Client: {e}")
    traceback.print_exc()

print("\nStep 3: Patching requests.Session...")
# Patch requests.Session
try:
    import requests
    from requests.sessions import Session
    
    # Store the original __init__ method
    original_init = Session.__init__
    
    # Define a patched __init__ method
    def patched_init(self, *args, **kwargs):
        print(f"Session.__init__ called with args: {args}, kwargs: {kwargs}")
        # Remove proxies from kwargs if present
        if 'proxies' in kwargs:
            print(f"Removing 'proxies' from kwargs: {kwargs['proxies']}")
            del kwargs['proxies']
        
        # Call original init
        result = original_init(self, *args, **kwargs)
        
        # Force empty proxies
        if hasattr(self, 'proxies') and self.proxies:
            print(f"Overriding existing proxies: {self.proxies}")
        self.proxies = {}
        return result
    
    # Apply the patch
    Session.__init__ = patched_init
    print("Successfully patched requests.Session.__init__")
except Exception as e:
    print(f"Failed to patch requests.Session: {e}")
    traceback.print_exc()

print("\nStep 4: Testing Groq client initialization...")
# Test Groq client initialization
try:
    from groq import Groq
    
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("ERROR: GROQ_API_KEY environment variable not set.")
        sys.exit(1)
    
    print("Initializing Groq client with api_key only...")
    client = Groq(api_key=api_key)
    print("Groq client initialized successfully!")
    
    print("\nTesting a simple chat completion...")
    completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, how are you?"}
        ],
        model="llama3-8b-8192",
        max_tokens=10
    )
    
    print(f"Response received: {completion.choices[0].message.content}")
    print("Test completed successfully!")
    
except Exception as e:
    print(f"ERROR testing Groq client: {e}")
    traceback.print_exc()

print("\nDebug script completed.") 