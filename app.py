import os
import tempfile
import base64
import sys
import argparse
import json
import glob
import logging
from datetime import datetime

# Load environment variables first
from dotenv import load_dotenv
load_dotenv()

import mimetypes
mimetypes.add_type("application/javascript", ".mjs")

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger(__name__)

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
from utils.database import init_db, create_conversation, add_message, get_conversations, get_conversation, delete_conversation, update_conversation_title, store_conversation_data, get_conversation_data

# Add template folder check before app creation
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
if not os.path.exists(template_dir):
    os.makedirs(template_dir, exist_ok=True)
    # Create a simple index.html if it doesn't exist
    with open(os.path.join(template_dir, 'index.html'), 'w') as f:
        f.write('<html><body><h1>Doctor Simulation</h1><p>Welcome to the Doctor Simulation app.</p></body></html>')
    logger.info(f"Created templates directory and basic index.html at {template_dir}")

# Initialize Flask app with explicit template folder
app = Flask(__name__, template_folder=template_dir)

# Add request logging
@app.before_request
def log_request_info():
    logger.debug('Request: %s %s', request.method, request.path)
    logger.debug('Headers: %s', request.headers)
    logger.debug('Body: %s', request.get_data())

# Add error handlers
@app.errorhandler(404)
def handle_404(e):
    logger.warning('404 error: %s - Path: %s, Method: %s', 
                  e, request.path, request.method)
    return jsonify({
        'status': 'error',
        'message': f'Not Found: The requested URL {request.path} was not found on the server.'
    }), 404

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

def initialize_patient_data(patient_file=None, custom_data=None):
    global current_patient_simulation
    patient_data = {}
    
    if custom_data:
        # Handle custom patient data passed directly
        logger.info("Initializing custom patient data")
        patient_data = custom_data
        current_patient_simulation = '__custom__'
        logger.info(f"Custom patient data initialized: {patient_data}")
    elif patient_file:
        # Handle file-based patient data
        patient_data = load_patient_simulation(patient_file)
        if patient_data:
            print(f"Patient simulation data loaded successfully from {patient_file}")
            current_patient_simulation = patient_file
        else:
            print("Warning: Failed to load patient simulation data")
    
    return patient_data

# Use this global variable instead of the one dependent on args
patient_data = initialize_patient_data()

# Move this debug route outside of the if __name__ == '__main__' block
@app.route('/api/debug', methods=['GET'])
def debug_routes():
    """List all available routes for debugging"""
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            'endpoint': rule.endpoint,
            'methods': list(rule.methods),
            'path': str(rule)
        })
    return jsonify({
        'status': 'success',
        'routes': routes
    })


@app.route('/')
def index():
    """Render the main page"""
    logger.info('Serving index page')
    return render_template('index.html')

@app.route('/api/patient-simulations', methods=['GET'])
def list_patient_simulations():
    """List available patient simulations"""
    logger.info('Listing patient simulations')
    simulations = get_available_patient_simulations()
    logger.debug('Found simulations: %s', simulations)
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
        # Create a generic title that will be updated with the first message
        title = f"New Conversation"
        
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
        logger.info(f"Selecting simulation file: {simulation_file}")
        
        # Handle custom patient selection (redirect to form, don't create conversation yet)
        if simulation_file == "__custom__":
            logger.info("Custom patient selected - frontend will show form")
            # Don't create conversation yet, that happens when form is submitted
            # Just acknowledge the selection
            current_patient_simulation = None
            patient_data = {}
            return jsonify({
                'status': 'success',
                'message': 'Custom patient selection acknowledged - please fill out the form',
                'current_simulation': '__custom__',
                'conversation_id': None  # No conversation created yet
            })
        
        # Allow empty simulation file to clear the current simulation
        if simulation_file == "":
            logger.info("Clearing current simulation and voice settings")
            current_patient_simulation = None
            patient_data = {}
        elif not os.path.exists(simulation_file):
            logger.error(f"Simulation file not found: {simulation_file}")
            return jsonify({
                'status': 'error',
                'message': f'Simulation file {simulation_file} not found'
            }), 404
        else:
            # Load the selected simulation (file-based)
            logger.info(f"Loading simulation data from: {simulation_file}")
            patient_data = initialize_patient_data(simulation_file)
            
            # Explicitly log the loaded data for debugging
            logger.info(f"Loaded patient_data: {patient_data}")
            
            # Ensure voice_id is present
            if patient_data:
                current_voice = patient_data.get('voice_id')
                logger.info(f"Loaded voice_id from simulation: {current_voice}")
                if 'voice_id' not in patient_data:
                    logger.warning(f"No voice_id found in simulation file: {simulation_file}")
                    patient_data['voice_id'] = 'Fritz-PlayAI'
                    logger.info(f"Set default voice_id: {patient_data['voice_id']}")
            else:
                logger.warning("No patient data loaded from simulation file")
                patient_data = {}
        
        # Clear conversation history when changing simulations
        conversation_history = []
        
        # Create a new conversation in the database with a generic title
        # The title will be updated with actual content after the first message
        title = "New Conversation"
        if simulation_file:
            title = f"Conversation with {os.path.basename(simulation_file)}"
        
        # Store the patient_data in the database along with the conversation
        # This will require modifying your database.py file to store simulation data
        current_conversation_id = create_conversation(title, simulation_file)
        
        # Store the actual patient data in the database (add this function to database.py)
        if patient_data:
            # This should be implemented in database.py
            logger.info("Storing patient data in database for conversation")
            store_conversation_data(current_conversation_id, 'patient_data', patient_data)
        
        return jsonify({
            'status': 'success',
            'message': f'Selected simulation: {simulation_file}',
            'current_simulation': current_patient_simulation,
            'conversation_id': current_conversation_id
        })
        
    except Exception as e:
        logger.error(f"Error selecting simulation: {str(e)}", exc_info=True)
        return jsonify({
            'status': 'error',
            'message': f'Error selecting simulation: {str(e)}'
        }), 500

@app.route('/api/update-voice', methods=['POST'])
def update_voice():
    """Update the voice ID for a conversation"""
    global current_conversation_id
    
    try:
        data = request.get_json()
        if not data or 'voice_id' not in data:
            return jsonify({
                'status': 'error',
                'message': 'No voice ID specified'
            }), 400
        
        voice_id = data.get('voice_id')
        conversation_id = data.get('conversation_id') or current_conversation_id
        
        if not conversation_id:
            return jsonify({
                'status': 'error',
                'message': 'No active conversation'
            }), 400
        
        # Store the voice ID in the database
        store_conversation_data(conversation_id, 'voice_id', voice_id)
        
        logger.info(f"Updated voice_id to {voice_id} for conversation {conversation_id}")
        
        return jsonify({
            'status': 'success',
            'message': f'Voice updated to {voice_id}'
        })
        
    except Exception as e:
        logger.error(f"Error updating voice: {str(e)}", exc_info=True)
        return jsonify({
            'status': 'error',
            'message': f'Error updating voice: {str(e)}'
        }), 500

@app.route('/api/create-custom-patient', methods=['POST'])
def create_custom_patient():
    """Create a new conversation with custom patient data"""
    global patient_data, current_patient_simulation, current_conversation_id, conversation_history
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No data provided'
            }), 400
        
        # Validate the data structure
        if 'type' not in data or data['type'] != 'custom':
            return jsonify({
                'status': 'error',
                'message': 'Invalid data type - expected custom patient data'
            }), 400
        
        if 'patient_details' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Missing patient_details in request'
            }), 400
        
        custom_patient_details = data['patient_details']
        
        # Validate required fields
        required_fields = ['age', 'gender', 'occupation']
        missing_fields = [field for field in required_fields if not custom_patient_details.get(field)]
        
        if missing_fields:
            return jsonify({
                'status': 'error',
                'message': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        # Validate age
        try:
            age = int(custom_patient_details['age'])
            if age < 1 or age > 120:
                return jsonify({
                    'status': 'error',
                    'message': 'Age must be between 1 and 120'
                }), 400
        except (ValueError, TypeError):
            return jsonify({
                'status': 'error',
                'message': 'Age must be a valid number'
            }), 400
        
        logger.info(f"Creating custom patient with details: {custom_patient_details}")
        
        # Generate illness based on patient demographics (synchronous call)
        logger.info("Generating illness for custom patient...")
        generated_illness = generate_illness_for_patient(custom_patient_details)
        
        # Create patient data structure with generated illness
        patient_data = {
            'type': 'custom',
            'prompt_template': default_prompt_template,
            'patient_details': {
                'age': str(custom_patient_details['age']),
                'gender': custom_patient_details['gender'],
                'occupation': custom_patient_details['occupation'],
                'medical_history': custom_patient_details.get('medical_history', 'No significant medical history'),
                'illness': generated_illness['full_description'],  # Use generated illness
                'recent_exposure': custom_patient_details.get('recent_exposure', 'None reported')
            },
            'generated_condition': generated_illness,  # Store the structured illness data
            'voice_id': 'Fritz-PlayAI'
        }
        
        # Clear conversation history for new patient
        conversation_history = []
        
        # Set current patient simulation to indicate custom patient
        current_patient_simulation = '__custom__'
        
        # Create new conversation with descriptive title
        title = f"Custom Patient - {custom_patient_details['gender']}, {custom_patient_details['age']}"
        
        # Create conversation in database
        current_conversation_id = create_conversation(title, '__custom__')
        
        # Store the custom patient data in the database
        store_conversation_data(current_conversation_id, 'patient_data', patient_data)
        
        logger.info(f"Created custom patient conversation {current_conversation_id} with data: {patient_data}")
        
        return jsonify({
            'status': 'success',
            'message': 'Custom patient created successfully',
            'conversation_id': current_conversation_id,
            'patient_details': {
                'age': patient_data['patient_details']['age'],
                'gender': patient_data['patient_details']['gender'],
                'occupation': patient_data['patient_details']['occupation'],
                'medical_history': patient_data['patient_details']['medical_history'],
                'recent_exposure': patient_data['patient_details']['recent_exposure']
                # Note: illness is intentionally excluded from response
            }
        })
        
    except Exception as e:
        logger.error(f"Error creating custom patient: {str(e)}", exc_info=True)
        return jsonify({
            'status': 'error',
            'message': f'Error creating custom patient: {str(e)}'
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
        logger.info("=== Starting audio processing ===")
        
        # Log all form data keys for debugging
        logger.info(f"Form data keys: {list(request.form.keys())}")
        
        # Get voice ID from form data early in the process
        voice_id = request.form.get('voice_id')
        logger.info(f"Received voice_id from form: {voice_id}")
        
        # Check if a conversation is active
        if not current_conversation_id:
            logger.debug("No active conversation, creating new one")
            title = f"New Conversation - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            current_conversation_id = create_conversation(title, None)
            conversation_history = []
            patient_data = {}  # Default empty patient data
            logger.info(f"Created new conversation with ID: {current_conversation_id}")
        else:
            # Retrieve patient data from database
            logger.info(f"Retrieving patient data for conversation: {current_conversation_id}")
            retrieved_data = get_conversation_data(current_conversation_id, 'patient_data')
            if retrieved_data:
                patient_data = retrieved_data
                logger.info(f"Successfully retrieved patient_data: {patient_data}")
            else:
                patient_data = {}
                logger.warning(f"No patient data found for conversation {current_conversation_id}")
            
        logger.info(f"Using patient_data: {patient_data}")

        # If voice_id was received from form data, store it in the database right away
        if voice_id and current_conversation_id:
            logger.info(f"Storing voice_id from form data: {voice_id}")
            store_conversation_data(current_conversation_id, 'voice_id', voice_id)
        
        # Check if audio file was sent
        if 'audio' not in request.files:
            logger.error("No audio file provided in the request")
            return jsonify({
                'status': 'error',
                'message': 'No audio file provided'
            }), 400
        
        # Get audio file
        audio_file = request.files['audio']
        logger.debug(f"Received audio file: {audio_file.filename}, size: {audio_file.content_length}")
        
        # Transcribe audio
        audio_bytes = audio_file.read()
        logger.debug(f"Read {len(audio_bytes)} bytes from audio file")
        logger.debug("Attempting to transcribe audio...")
        transcription = transcribe_audio_data(audio_bytes)
        
        # If transcription failed, return error
        if not transcription:
            logger.error("Transcription failed - no text returned from transcribe_audio_data")
            return jsonify({
                'status': 'error',
                'message': 'Failed to transcribe audio. Please try again.'
            }), 500
        
        logger.debug(f"Transcription successful: '{transcription}'")
        
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
            
            # Update conversation title if this is the first user message
            conversation = get_conversation(current_conversation_id)
            if conversation and len(conversation['messages']) == 2:  # First user-assistant exchange (2 messages)
                # Create title from first 30 characters of user's message
                title_text = transcription[:30] + "..." if len(transcription) > 30 else transcription
                update_conversation_title(current_conversation_id, title_text)
        
        # Get voice ID from form data or database
        logger.info("=== Voice selection process ===")
        # We already retrieved voice_id at the beginning
        if voice_id:
            logger.info(f"Using voice_id from form data: {voice_id}")
            # Already stored above
        else:
            # Try to get voice_id from the database
            if current_conversation_id:
                voice_id = get_conversation_data(current_conversation_id, 'voice_id')
                if voice_id:
                    logger.info(f"Retrieved voice_id from database: {voice_id}")
                else:
                    voice_id = 'Fritz-PlayAI'  # Default voice
                    logger.warning(f"No voice_id found in database, using default: {voice_id}")
                    # Store the default voice_id
                    store_conversation_data(current_conversation_id, 'voice_id', voice_id)
            else:
                voice_id = 'Fritz-PlayAI'  # Default voice
                logger.warning(f"No active conversation, using default voice_id: {voice_id}")
        
        logger.info(f"Final voice_id selected for TTS: {voice_id}")
        speech_audio_bytes = generate_speech_audio(response_text, voice_id)
        
        # Log speech generation result
        if speech_audio_bytes:
            logger.debug(f"Speech audio generated successfully: {len(speech_audio_bytes)} bytes")
            base64_audio = base64.b64encode(speech_audio_bytes).decode('utf-8')
            logger.debug(f"Base64 audio size: {len(base64_audio)}")
        else:
            base64_audio = ""
            logger.error("Speech audio generation failed, returning empty audio")
        
        return jsonify({
            'status': 'success',
            'user_transcription': transcription,
            'assistant_response_text': response_text,
            'assistant_response_audio': base64_audio
        })
        
    except Exception as e:
        logger.error(f"Error processing audio: {str(e)}", exc_info=True)
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
        
        # Get the voice ID if available
        voice_id = get_conversation_data(conversation_id, 'voice_id')
        
        # Convert database messages to conversation history format
        conversation_history = [
            {"role": msg["role"], "content": msg["content"]}
            for msg in conversation["messages"]
        ]
            
        return jsonify({
            'status': 'success',
            'message': f'Conversation {conversation_id} loaded successfully',
            'conversation': conversation,
            'voice_id': voice_id
        })
    except Exception as e:
        logger.error(f"Error loading conversation: {str(e)}", exc_info=True)
        return jsonify({
            'status': 'error',
            'message': f'Error loading conversation: {str(e)}'
        }), 500

@app.route('/test', methods=['GET'])
def test_route():
    """Simple test route to verify Flask is working"""
    logger.info('Test route accessed')
    return jsonify({
        'status': 'success',
        'message': 'Flask server is running correctly'
    }) 

@app.route('/api/diagnose', methods=['GET'])
def diagnose_api():
    """Test API connections and functionality"""
    results = {
        "environment": {},
        "tests": {}
    }
    
    # Check environment
    for key in ['GROQ_API_KEY', 'PORT']:
        results["environment"][key] = "SET" if os.environ.get(key) else "NOT SET"
    
    # Test Groq API connection
    try:
        # Simple test that doesn't require audio
        test_response = get_groq_response("Hello, this is a test.", model="llama3-8b-8192")
        results["tests"]["groq_text_api"] = "SUCCESS" if test_response else "FAILED"
    except Exception as e:
        results["tests"]["groq_text_api"] = f"ERROR: {str(e)}"
    
    # Add more component tests as needed
    
    return jsonify(results)

@app.route('/api/current-patient-details', methods=['GET'])
def get_current_patient_details():
    """Get details of the currently selected patient simulation"""
    if not patient_data or not patient_data.get('patient_details'):
        return jsonify({
            'status': 'error',
            'message': 'No patient simulation selected or invalid simulation data'
        }), 404
        
    # Get patient details, excluding the 'illness' field
    details = patient_data.get('patient_details', {}).copy()
    if 'illness' in details:
        del details['illness']  # Remove illness field
        
    return jsonify({
        'status': 'success',
        'patient_details': details,
        'simulation_file': current_patient_simulation
    })

@app.route('/api/generate-illness', methods=['POST'])
def generate_illness():
    """Generate a realistic illness based on patient demographics"""
    
    try:
        data = request.get_json()
        if not data or 'patient_details' not in data:
            return jsonify({
                'status': 'error',
                'message': 'No patient details provided'
            }), 400
        
        patient_details = data['patient_details']
        
        # Generate illness based on patient demographics
        logger.info("Generating illness for custom patient...")
        generated_illness = generate_illness_for_patient(patient_details)
        
        return jsonify({
            'status': 'success',
            'generated_illness': generated_illness
        })
        
    except Exception as e:
        logger.error(f"Error generating illness: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

def generate_illness_for_patient(patient_details):
    """Generate a realistic illness based on patient demographics (synchronous)"""
    
    prompt = f"""Based on the following patient profile, generate a realistic medical condition or illness that this patient could plausibly have. Consider their demographics and risk factors.

Patient Profile:
- Age: {patient_details['age']}
- Gender: {patient_details['gender']}
- Occupation: {patient_details['occupation']}
- Medical History: {patient_details.get('medical_history', 'No significant history')}
- Recent Exposures: {patient_details.get('recent_exposure', 'None reported')}

Generate a single, specific medical condition with realistic symptoms that would be appropriate for this patient profile. Consider:
- Age-related conditions
- Occupational hazards
- Gender-specific conditions
- Medical history implications

Respond with just the condition name and 2-3 key symptoms they would experience, formatted as:
CONDITION: [condition name]
SYMPTOMS: [symptom 1], [symptom 2], [symptom 3]

Example:
CONDITION: Tension headaches
SYMPTOMS: Throbbing headache, neck stiffness, light sensitivity"""

    try:
        # Use your existing Groq client (synchronous call)
        response = groq_client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=200
        )
        
        generated_text = response.choices[0].message.content.strip()
        
        # Parse the response
        lines = generated_text.split('\n')
        condition = ""
        symptoms = ""
        
        for line in lines:
            if line.startswith('CONDITION:'):
                condition = line.replace('CONDITION:', '').strip()
            elif line.startswith('SYMPTOMS:'):
                symptoms = line.replace('SYMPTOMS:', '').strip()
        
        return {
            'condition': condition,
            'symptoms': symptoms,
            'full_description': f"{condition} - {symptoms}"
        }
        
    except Exception as e:
        logger.error(f"Error generating illness: {e}")
        # Fallback to a generic condition
        return {
            'condition': 'General fatigue and discomfort',
            'symptoms': 'Tiredness, mild aches, general malaise',
            'full_description': 'General fatigue and discomfort - Tiredness, mild aches, general malaise'
        }

@app.route('/api/submit-diagnosis', methods=['POST'])
def submit_diagnosis():
    """Allow the doctor to submit their diagnosis for evaluation"""
    global current_conversation_id
    
    try:
        data = request.get_json()
        submitted_diagnosis = data.get('diagnosis', '').strip()
        
        if not current_conversation_id:
            return jsonify({'status': 'error', 'message': 'No active conversation'}), 400
        
        # Get the actual condition from the database
        patient_data = get_conversation_data(current_conversation_id, 'patient_data')
        if not patient_data or 'generated_condition' not in patient_data:
            return jsonify({'status': 'error', 'message': 'No patient data found'}), 400
        
        actual_condition = patient_data['generated_condition']['condition']
        
        # Use LLM to evaluate the diagnosis
        evaluation = evaluate_diagnosis(submitted_diagnosis, actual_condition)
        
        return jsonify({
            'status': 'success',
            'actual_condition': actual_condition,
            'evaluation': evaluation,
            'submitted_diagnosis': submitted_diagnosis
        })
        
    except Exception as e:
        logger.error(f"Error submitting diagnosis: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

def evaluate_diagnosis(submitted_diagnosis, actual_condition):
    """Use LLM to evaluate how close the diagnosis is"""
    prompt = f"""Evaluate how accurate this medical diagnosis is:

Submitted Diagnosis: {submitted_diagnosis}
Actual Condition: {actual_condition}

Rate the accuracy on a scale of 1-10 and provide brief feedback on:
1. How close the diagnosis is
2. What was missed or incorrect
3. What was correctly identified

Format your response as:
SCORE: [1-10]
FEEDBACK: [your evaluation]"""

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except:
        return "Unable to evaluate diagnosis at this time."

# Keep the if __name__ == '__main__' block for running the app
if __name__ == '__main__':
    # Parse command line arguments only when running directly with Python
    parser = argparse.ArgumentParser(description='Run the voice conversation app')
    parser.add_argument('--port', type=int, default=5000, help='Port to run the app on')
    parser.add_argument('--patient-file', type=str, help='Path to patient simulation JSON file')
    args = parser.parse_args()
    
    # Load patient simulation data if provided
    if args.patient_file:
        patient_data = initialize_patient_data(args.patient_file)
        logger.info('Loaded patient data from %s', args.patient_file)
    
    # Create utils directory if it doesn't exist
    os.makedirs('utils', exist_ok=True)
    
    # Print API key status (without revealing the key)
    api_key = os.environ.get('GROQ_API_KEY')
    if api_key:
        logger.info('GROQ_API_KEY found - length: %d', len(api_key))
    else:
        logger.warning('GROQ_API_KEY not found in environment!')
    
    # Get port from environment variable (Heroku sets this) or use default
    port = int(os.environ.get('PORT', args.port))
    #host = '127.0.0.1'
    host = '0.0.0.0'
    logger.info('Starting Flask app on %s:%d', host, port)
    app.run(host=host, port=port, debug=True)

    # Add this before app.run()
    logger.info("Registered URL Rules:")
    for rule in app.url_map.iter_rules():
        logger.info(f"Route: {rule}, Endpoint: {rule.endpoint}")
