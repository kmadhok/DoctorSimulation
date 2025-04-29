import os
import sys
import json
import traceback
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def get_groq_response(input_text, model="llama3-8b-8192", history=None, system_prompt=None):
    """
    Get a response from Groq LLM with conversation history support.
    
    Args:
        input_text (str): The text to send to the LLM
        model (str): The Groq model to use
        history (list): Optional conversation history
        system_prompt (str): Optional custom system prompt
        
    Returns:
        str: The LLM response
    """
    # Get Groq API key from environment variable

    api_key=os.environ.get("GROQ_API_KEY")
    if not api_key:
        return "Error: GROQ_API_KEY environment variable not set. Please set it with your Groq API key."
    
    # Initialize history if not provided
    if history is None:
        history = []
    
    try:
        # Debug: Print incoming history
        print(f"Processing request with {len(history)} previous messages")
        
        # Initialize Groq client - explicitly use only api_key
        try:
            # Explicitly avoid proxy settings by using only the api_key parameter
            client = Groq(api_key=api_key)
            # Test the client with a simple call to ensure it works
            print("Groq client initialized successfully")
        except Exception as client_error:
            print(f"Error initializing Groq client: {client_error}")
            traceback.print_exc()  # Print full traceback for debugging
            return f"Error: Unable to initialize Groq client: {str(client_error)}"
        
        # Construct messages list with custom system prompt if provided
        default_system_prompt = "You are a helpful assistant. Respond concisely to the user's input."
        messages = [{"role": "system", "content": system_prompt or default_system_prompt}]
        messages.extend(history)
        messages.append({"role": "user", "content": input_text})
        
        # API call
        try:
            chat_completion = client.chat.completions.create(
                messages=messages,
                model=model,
            )
            
            return chat_completion.choices[0].message.content
        except Exception as api_error:
            print(f"Error during Groq API call: {api_error}")
            traceback.print_exc()  # Print full traceback for debugging
            return f"Error: Failed to get response from Groq API: {str(api_error)}"
        
    except Exception as e:
        print(f"Unexpected error in get_groq_response: {e}")
        traceback.print_exc()
        return f"Error: Failed to get response from Groq: {str(e)}"

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Get a response from Groq LLM")
    parser.add_argument("--text", type=str, help="Input text to send to LLM")
    parser.add_argument("--model", type=str, default="llama3-8b-8192", help="Groq model to use")
    parser.add_argument("--history-file", type=str, help="JSON file containing conversation history")
    parser.add_argument("--system-prompt", type=str, help="Custom system prompt")
    
    args = parser.parse_args()
    
    # Get input text from arguments, stdin, or prompt
    if args.text:
        input_text = args.text
    elif not sys.stdin.isatty():
        input_text = sys.stdin.read().strip()
    else:
        input_text = input("Enter text: ")
    
    if not input_text.strip():
        print("Error: No input text provided.")
        sys.exit(1)
    
    # Load history if provided
    history = None
    if args.history_file:
        try:
            with open(args.history_file, 'r') as f:
                history = json.load(f)
        except Exception as e:
            print(f"Error loading history file: {str(e)}")
            sys.exit(1)
    
    # Get response
    response = get_groq_response(input_text, args.model, history, args.system_prompt)
    
    # Print response
    print(response) 