import os
import tempfile
import base64
import sys
import argparse
import json
import glob
from datetime import datetime

# Load environment variables first
from dotenv import load_dotenv
load_dotenv()

# Apply patch to Groq client before importing any Groq modules
print("Applying Groq client patch...")
from utils.patch_groq import patch_successful
if not patch_successful:
    print("WARNING: Failed to patch Groq client, proxy issues may occur")
else:
    print("Groq client patch applied successfully")

# Initialize Flask only after patching
from flask import Flask, request, jsonify, render_template
import json

# Import our refactored modules - after patching
from utils.groq_integration import get_groq_response
from utils.groq_transcribe import transcribe_audio_data
from utils.groq_tts_speech import generate_speech_audio
from utils.patient_simulation import load_patient_simulation, get_patient_system_prompt
from utils.database import init_db, create_conversation, add_message, get_conversations, get_conversation, delete_conversation

# Initialize Flask app
app = Flask(__name__)

# Initialize database
init_db()

# Initialize conversation history
conversation_history = []

# Global variable to store the current patient simulation
current_patient_simulation = None

# Global variable for current conversation ID
current_conversation_id = None

def get_available_patient_simulations():
    """Get list of available patient simulation files"""
    simulation_files = glob.glob('patient_simulation_*.json')
    return [os.path.basename(f) for f in simulation_files]

def initialize_patient_data(patient_file=None):
    global current_patient_simulation
    patient_data = {}
    if patient_file:
        patient_data = load_patient_simulation(patient_file)
        if patient_data:
            print(f"Patient simulation data loaded successfully from {patient_file}")
            current_patient_simulation = patient_file
        else:
            print("Warning: Failed to load patient simulation data")
    return patient_data

# Use this global variable instead of the one dependent on args
patient_data = initialize_patient_data()

# Move the argument parsing inside the if __name__ == '__main__' block
if __name__ == '__main__':
    # Parse command line arguments only when running directly with Python
    parser = argparse.ArgumentParser(description='Run the voice conversation app')
    parser.add_argument('--port', type=int, default=5000, help='Port to run the app on')
    parser.add_argument('--patient-file', type=str, help='Path to patient simulation JSON file')
    args = parser.parse_args()
    
    # Load patient simulation data if provided
    if args.patient_file:
        patient_data = initialize_patient_data(args.patient_file)
    
    # Create utils directory if it doesn't exist
    os.makedirs('utils', exist_ok=True)
    
    # Print API key status (without revealing the key)
    api_key = os.environ.get('GROQ_API_KEY')
    if api_key:
        print(f"GROQ_API_KEY found - length: {len(api_key)}")
    else:
        print("WARNING: GROQ_API_KEY not found in environment!")
    
    # Get port from environment variable (Heroku sets this) or use default
    port = int(os.environ.get('PORT', args.port))
    host = '0.0.0.0'
    
    print(f"Starting Flask app on {host}:{port}")
    app.run(host=host, port=port, debug=False)

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/api/patient-simulations', methods=['GET'])
def list_patient_simulations():
    """List available patient simulations"""
    simulations = get_available_patient_simulations()
    return jsonify({
        'status': 'success',
        'simulations': simulations,
        'current_simulation': current_patient_simulation
    })

@app.route('/api/conversations/new', methods=['POST'])
def create_new_conversation():
    """Create a new empty conversation without a patient simulation"""
    global current_conversation_id, conversation_history
    
    try:
        # Create a title based on the current timestamp
        title = f"New Conversation - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        # Create a new conversation in the database
        current_conversation_id = create_conversation(title, None)
        
        # Clear conversation history for the new conversation
        conversation_history = []
        
        return jsonify({
            'status': 'success',
            'message': 'New conversation created',
            'conversation_id': current_conversation_id
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error creating conversation: {str(e)}'
        }), 500

@app.route('/api/select-simulation', methods=['POST'])
def select_simulation():
    """Select a patient simulation"""
    global patient_data, current_patient_simulation, current_conversation_id, conversation_history
    
    try:
        data = request.get_json()
        if not data or 'simulation_file' not in data:
            return jsonify({
                'status': 'error',
                'message': 'No simulation file specified'
            }), 400
            
        simulation_file = data['simulation_file']
        
        # Allow empty simulation file to clear the current simulation
        if simulation_file == "":
            current_patient_simulation = None
            patient_data = {}
        elif not os.path.exists(simulation_file):
            return jsonify({
                'status': 'error',
                'message': f'Simulation file {simulation_file} not found'
            }), 404
        else:
            # Load the selected simulation
            patient_data = initialize_patient_data(simulation_file)
        
        # Clear conversation history when changing simulations
        conversation_history = []
        
        # Create a new conversation in the database
        title = simulation_file if simulation_file else "Default Conversation"
        title = f"Conversation with {title} - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        current_conversation_id = create_conversation(title, simulation_file)
        
        return jsonify({
            'status': 'success',
            'message': f'Selected simulation: {simulation_file}',
            'current_simulation': current_patient_simulation,
            'conversation_id': current_conversation_id
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error selecting simulation: {str(e)}'
        }), 500

@app.route('/process_audio', methods=['POST'])
def process_audio():
    """
    Process audio from the client:
    1. Receive audio file
    2. Transcribe audio using Groq API
    3. Get LLM response using Groq API
    4. Generate speech audio from response
    5. Return all results to client
    """
    global conversation_history, current_conversation_id
    
    try:
        # Check if a conversation is active
        if not current_conversation_id:
            # Create a new conversation if none exists
            title = f"New Conversation - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            current_conversation_id = create_conversation(title, None)
            conversation_history = []
        
        # Check if audio file was sent
        if 'audio' not in request.files:
            return jsonify({
                'status': 'error',
                'message': 'No audio file provided'
            }), 400
        
        # Get audio file
        audio_file = request.files['audio']
        
        # Transcribe audio
        audio_bytes = audio_file.read()
        transcription = transcribe_audio_data(audio_bytes)
        
        # If transcription failed, return error
        if not transcription:
            return jsonify({
                'status': 'error',
                'message': 'Failed to transcribe audio. Please try again.'
            }), 500
        
        # Check for termination commands
        if "exit" in transcription.lower() or "quit" in transcription.lower():
            return jsonify({
                'status': 'exit',
                'user_transcription': transcription,
                'assistant_response_text': 'Ending conversation. Goodbye!',
                'assistant_response_audio': ''  # Empty as we don't need audio for exit
            })
        
        # Get system prompt from patient simulation if available
        system_prompt = get_patient_system_prompt(patient_data) if patient_data else None
        
        # Check for repetition of last assistant message
        if conversation_history and len(conversation_history) >= 2:
            last_assistant_message = next((msg for msg in reversed(conversation_history) 
                                        if msg.get('role') == 'assistant'), None)
            if last_assistant_message and transcription.lower() == last_assistant_message.get('content', '').lower():
                response_text = "It seems you're repeating what I just said. Do you have a question about that?"
            else:
                # Get LLM response with patient simulation context (or default if none)
                response_text = get_groq_response(
                    input_text=transcription,
                    model="llama3-8b-8192",
                    history=conversation_history,
                    system_prompt=system_prompt
                )
        else:
            # First interaction or empty history
            response_text = get_groq_response(
                input_text=transcription,
                model="llama3-8b-8192",
                system_prompt=system_prompt
            )
        
        # Update conversation history
        conversation_history.append({"role": "user", "content": transcription})
        conversation_history.append({"role": "assistant", "content": response_text})
        
        # Save messages to database if a conversation is active
        if current_conversation_id:
            add_message(current_conversation_id, "user", transcription)
            add_message(current_conversation_id, "assistant", response_text)
        
        # Generate speech audio from response
        speech_audio_bytes = generate_speech_audio(response_text)
        
        # Convert audio bytes to base64 for transmission
        if speech_audio_bytes:
            base64_audio = base64.b64encode(speech_audio_bytes).decode('utf-8')
        else:
            base64_audio = ""  # Empty string if audio generation failed
            print("Warning: Speech audio generation failed, returning empty audio")
        
        return jsonify({
            'status': 'success',
            'user_transcription': transcription,
            'assistant_response_text': response_text,
            'assistant_response_audio': base64_audio
        })
        
    except Exception as e:
        print(f"Error processing audio: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f"Error processing request: {str(e)}"
        }), 500

# Add new routes for conversation management
@app.route('/api/conversations', methods=['GET'])
def list_conversations():
    """Get a list of all saved conversations"""
    try:
        conversations = get_conversations()
        return jsonify({
            'status': 'success',
            'conversations': conversations
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error getting conversations: {str(e)}'
        }), 500

@app.route('/api/conversations/<int:conversation_id>', methods=['GET'])
def get_conversation_by_id(conversation_id):
    """Get a specific conversation by ID"""
    try:
        conversation = get_conversation(conversation_id)
        if not conversation:
            return jsonify({
                'status': 'error',
                'message': f'Conversation with ID {conversation_id} not found'
            }), 404
            
        return jsonify({
            'status': 'success',
            'conversation': conversation
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error getting conversation: {str(e)}'
        }), 500

@app.route('/api/conversations/<int:conversation_id>', methods=['DELETE'])
def delete_conversation_by_id(conversation_id):
    """Delete a specific conversation by ID"""
    try:
        success = delete_conversation(conversation_id)
        if not success:
            return jsonify({
                'status': 'error',
                'message': f'Conversation with ID {conversation_id} not found'
            }), 404
            
        return jsonify({
            'status': 'success',
            'message': f'Conversation {conversation_id} deleted successfully'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error deleting conversation: {str(e)}'
        }), 500

@app.route('/api/conversations/<int:conversation_id>/load', methods=['POST'])
def load_conversation_by_id(conversation_id):
    """Load a conversation into the active session"""
    global conversation_history, current_conversation_id, current_patient_simulation, patient_data
    
    try:
        conversation = get_conversation(conversation_id)
        if not conversation:
            return jsonify({
                'status': 'error',
                'message': f'Conversation with ID {conversation_id} not found'
            }), 404
            
        # Update current conversation ID
        current_conversation_id = conversation_id
        
        # Load the simulation file if available
        simulation_file = conversation.get('simulation_file')
        if simulation_file and os.path.exists(simulation_file):
            patient_data = initialize_patient_data(simulation_file)
        
        # Convert database messages to conversation history format
        conversation_history = [
            {"role": msg["role"], "content": msg["content"]}
            for msg in conversation["messages"]
        ]
            
        return jsonify({
            'status': 'success',
            'message': f'Conversation {conversation_id} loaded successfully',
            'conversation': conversation
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error loading conversation: {str(e)}'
        }), 500 