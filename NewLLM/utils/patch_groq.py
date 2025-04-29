import os
import sys
import importlib
from unittest.mock import patch
import warnings

def patch_groq_client():
    """
    Patch proxy settings to allow Groq API calls to work properly.
    """
    try:
        # Clear proxy environment variables
        os.environ.pop('HTTP_PROXY', None)
        os.environ.pop('HTTPS_PROXY', None)
        os.environ.pop('http_proxy', None)
        os.environ.pop('https_proxy', None)
        print("Cleared proxy environment variables")
        
        # Patch the requests Session which is used by Groq client internally
        try:
            import requests
            from requests.sessions import Session
            
            # Store the original __init__ method
            original_init = Session.__init__
            
            # Define a patched __init__ method that removes proxies
            def patched_init(self, *args, **kwargs):
                # Remove proxies from kwargs if present
                if 'proxies' in kwargs:
                    del kwargs['proxies']
                
                # Call original init
                result = original_init(self, *args, **kwargs)
                
                # Ensure proxies is an empty dict
                self.proxies = {}
                return result
            
            # Apply the patch
            Session.__init__ = patched_init
            print("Successfully patched requests.Session to ignore proxies")
            return True
            
        except (ImportError, AttributeError) as e:
            print(f"Failed to patch requests.Session: {e}")
            return False
        
    except Exception as e:
        warnings.warn(f"Failed to patch request handling for Groq API: {e}")
        return False

# Try to patch immediately when this module is imported
patch_successful = patch_groq_client() 