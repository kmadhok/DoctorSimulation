import os
import tempfile
import base64
import sys
import argparse
import json
import glob
import logging
from datetime import datetime
import secrets
# NEW: Import for diagnosis evaluation
from difflib import SequenceMatcher
import re
from typing import Dict, Tuple, Any

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
from flask import Flask, request, jsonify, render_template, session
import json

# Import our refactored modules - after patching
from utils.groq_integration import get_groq_response
from utils.groq_transcribe import transcribe_audio_data
from utils.groq_tts_speech import generate_speech_audio
from utils.patient_simulation import load_patient_simulation, get_patient_system_prompt
from utils.database import init_db, create_conversation, add_message, get_conversations, get_conversation, delete_conversation, update_conversation_title, store_conversation_data, get_conversation_data, validate_patient_data_structure, get_all_conversation_data
from utils.ai_case_generator import generate_patient_case, get_all_specialties, get_available_symptoms_for_specialty, validate_symptom_specialty_combination

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
app.secret_key = secrets.token_urlsafe(24)

# Add request logging
@app.before_request
def log_request_info():
    logger.debug('Request: %s %s', request.method, request.path)
    # Only log headers and body in development, not in production
    if not os.environ.get('HEROKU'):  # or use another environment check
        logger.debug('Headers: %s', request.headers)
        if request.path != '/process_audio':
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

# NEW: Medical synonyms dictionary for diagnosis evaluation
MEDICAL_SYNONYMS = {
    'heart attack': ['myocardial infarction', 'mi', 'acute mi', 'acute myocardial infarction', 'stemi', 'nstemi'],
    'stroke': ['cva', 'cerebrovascular accident', 'brain attack', 'cerebral infarction'],
    'pneumonia': ['lung infection', 'pulmonary infection', 'chest infection'],
    'appendicitis': ['acute appendicitis', 'inflamed appendix'],
    'migraine': ['migraine headache', 'severe headache', 'vascular headache'],
    'diabetes': ['diabetes mellitus', 'dm', 'type 1 diabetes', 'type 2 diabetes'],
    'hypertension': ['high blood pressure', 'elevated blood pressure', 'htn'],
    'asthma': ['bronchial asthma', 'reactive airway disease'],
    'copd': ['chronic obstructive pulmonary disease', 'emphysema', 'chronic bronchitis'],
    'uti': ['urinary tract infection', 'bladder infection', 'cystitis'],
    'gastritis': ['stomach inflammation', 'gastric inflammation'],
    'bronchitis': ['acute bronchitis', 'chest cold'],
    'sinusitis': ['sinus infection', 'acute sinusitis'],
    'pharyngitis': ['sore throat', 'throat infection', 'strep throat'],
    'cellulitis': ['skin infection', 'soft tissue infection'],
    'gout': ['gouty arthritis', 'acute gout'],
    'kidney stones': ['renal calculi', 'nephrolithiasis', 'kidney stone'],
    'gallstones': ['cholelithiasis', 'gallbladder stones'],
    'acid reflux': ['gerd', 'gastroesophageal reflux disease', 'heartburn'],
    'panic attack': ['anxiety attack', 'panic disorder']
}

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

@app.route('/api/generate-patient-case', methods=['POST'])
def generate_patient_case_route():
    """Generate a new AI patient case based on provided parameters"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No data provided'
            }), 400

        # Extract case parameters
        case_params = data.get('case_parameters', {})
        specialty = case_params.get('specialty')
        symptoms = case_params.get('symptoms', [])
        severity = case_params.get('severity', 'moderate')
        
        # Debug logging
        logger.info(f"Generating AI case with specialty: {specialty}, symptoms: {symptoms}, severity: {severity}")
        
        # Validate inputs before processing
        if not specialty:
            return jsonify({
                'status': 'error',
                'message': 'Specialty is required'
            }), 400
            
        if not symptoms:
            return jsonify({
                'status': 'error',
                'message': 'At least one symptom is required'
            }), 400

        # Extract demographics
        demographics = {
            'age': case_params.get('age', 45),
            'gender': case_params.get('gender', 'Male'),
            'occupation': case_params.get('occupation', 'Office worker'),
            'medical_history': case_params.get('medical_history', 'No significant medical history')
        }
        
        logger.info(f"Demographics: {demographics}")

        # Add type checking before calling generate_patient_case
        try:
            # Test the medical validation functions first
            logger.info("Testing get_all_specialties()...")
            test_specialties = get_all_specialties()
            logger.info(f"get_all_specialties() returned type: {type(test_specialties)}")
            
            if not isinstance(test_specialties, dict):
                return jsonify({
                    'status': 'error',
                    'message': f'Medical system error: expected dict, got {type(test_specialties)}'
                }), 500
                
            logger.info("Testing get_available_symptoms_for_specialty()...")
            test_symptoms = get_available_symptoms_for_specialty(specialty)
            logger.info(f"get_available_symptoms_for_specialty() returned type: {type(test_symptoms)}")
            
            if not isinstance(test_symptoms, list):
                return jsonify({
                    'status': 'error', 
                    'message': f'Medical system error: expected list, got {type(test_symptoms)}'
                }), 500
                
        except Exception as e:
            logger.error(f"Error testing medical functions: {e}", exc_info=True)
            return jsonify({
                'status': 'error',
                'message': f'Medical system validation error: {str(e)}'
            }), 500

        # Generate the patient case
        logger.info("Calling generate_patient_case()...")
        result = generate_patient_case(specialty, symptoms, demographics, severity)
        logger.info(f"generate_patient_case() returned: {result.get('status', 'unknown')}")

        if result.get('status') == 'success':
            patient_data = result['patient_data']
            
            # ===== CONVERSATION ATTACHMENT LOGGING =====
            logger.info("🔗 ATTACHING AI CASE TO CONVERSATION")
            logger.info(f"   Patient Data Type: {patient_data.get('type', 'unknown')}")
            logger.info(f"   Generation Metadata Available: {bool(patient_data.get('generation_metadata'))}")
            
            # Initialize with the generated patient data
            global current_patient_simulation, current_conversation_id, conversation_history
            
            # Store the patient data globally
            initialize_patient_data(custom_data=patient_data)
            logger.info("✅ Patient data stored globally")
            
            # Create a new conversation for this case
            case_title = f"AI Case: {result['case_summary'].get('diagnosis', 'Unknown')}"
            current_conversation_id = create_conversation(case_title, current_patient_simulation)
            conversation_history = []
            
            # ✅ FIX: Store the patient data in the database
            store_conversation_data(current_conversation_id, 'patient_data', patient_data)
            logger.info("💾 Patient data stored in database")
            
            logger.info("💾 CONVERSATION CREATED & ATTACHED")
            logger.info(f"   Conversation ID: {current_conversation_id}")
            logger.info(f"   Conversation Title: {case_title}")
            logger.info(f"   Conversation History Reset: True")
            
            # Log what will be included in the actual patient prompt
            logger.info("🎭 PATIENT SIMULATION READY")
            logger.info("   The following prompt will be sent to AI when doctor asks questions:")
            
            # Build the actual prompt that will be used (simulate the formatting)
            if 'prompt_template' in patient_data and 'patient_details' in patient_data:
                try:
                    formatted_prompt = patient_data['prompt_template'].format(**patient_data['patient_details'])
                    # Log first 300 characters of the formatted prompt
                    logger.info(f"   Formatted Prompt Preview: {formatted_prompt[:300]}...")
                    logger.info(f"   Full Prompt Length: {len(formatted_prompt)} characters")
                except Exception as prompt_error:
                    logger.warning(f"   Could not format prompt preview: {prompt_error}")
            
            # Log voice settings
            voice_id = patient_data.get('voice_id', 'Unknown')
            logger.info(f"🔊 Voice ID for TTS: {voice_id}")
            
            # Log for Heroku monitoring (structured format)
            case_summary = result.get('case_summary', {})
            generation_metadata = patient_data.get('generation_metadata', {})
            
            logger.info("📊 HEROKU_MONITORING_DATA: " + json.dumps({
                'event': 'ai_case_generated',
                'conversation_id': current_conversation_id,
                'case_diagnosis': case_summary.get('diagnosis', 'Unknown'),
                'specialty': generation_metadata.get('specialty', 'Unknown'),
                'input_symptoms': generation_metadata.get('input_symptoms', []),
                'severity': generation_metadata.get('severity', 'Unknown'),
                'difficulty': case_summary.get('difficulty', 'Unknown'),
                'patient_age': patient_data.get('patient_details', {}).get('age', 'Unknown'),
                'patient_gender': patient_data.get('patient_details', {}).get('gender', 'Unknown'),
                'patient_occupation': patient_data.get('patient_details', {}).get('occupation', 'Unknown'),
                'warnings_count': len(result.get('warnings', [])),
                'learning_objectives_count': len(case_summary.get('learning_objectives', [])),
                'timestamp': datetime.now().isoformat()
            }))
            
            # Log successful generation with final summary
            logger.info(f"🎉 AI PATIENT CASE FULLY DEPLOYED: {case_title}")
            logger.info("   Case is now active and ready for doctor-patient simulation")
            
            return jsonify({
                'status': 'success',
                'message': 'AI patient case generated successfully',
                'patient_data': patient_data,
                'case_summary': result.get('case_summary', {}),
                'warnings': result.get('warnings', []),
                'conversation_id': current_conversation_id
            })
        else:
            logger.error(f"AI case generation failed: {result.get('message', 'Unknown error')}")
            return jsonify({
                'status': 'error',
                'message': f"Error generating AI patient case: {result.get('message', 'Unknown error')}"
            }), 500
            
    except Exception as e:
        logger.error(f"Error in generate_patient_case_route: {str(e)}", exc_info=True)
        return jsonify({
            'status': 'error',
            'message': f'Error generating AI patient case: {str(e)}'
        }), 500

@app.route('/api/create-custom-patient', methods=['POST'])
def create_custom_patient():
    """Create a new conversation with custom patient data (DEPRECATED - maintained for backward compatibility)"""
    global patient_data, current_patient_simulation, current_conversation_id, conversation_history
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No data provided'
            }), 400
        
        # Check if this is a new-style AI generation request
        if data.get('type') == 'ai_generated':
            logger.info("Redirecting AI generation request to new endpoint")
            # Redirect to new endpoint internally
            return generate_patient_case_route()
        
        # Handle legacy custom patient creation
        logger.info("Processing legacy custom patient creation request")
        
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
        required_fields = ['age', 'gender', 'occupation', 'illness']
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
        
        logger.info(f"Creating legacy custom patient with details: {custom_patient_details}")
        
        # Create patient data structure compatible with existing system
        # Use the default prompt template from existing patient simulations
        default_prompt_template = """You are a virtual patient in a clinical simulation. You have been assigned the following profile (for your reference only – you must never reveal the diagnosis itself, only describe symptoms):

  • Age: {age}  
  • Gender: {gender}  
  • Occupation: {occupation}  
  • Relevant medical history: {medical_history}  
  • Underlying illness (secret – do not mention this word or any synonyms): {illness}  
  • Any recent events or exposures: {recent_exposure}  

Your task:
When the "Doctor" (the next speaker) asks you questions, respond as a real patient would – describe what hurts, how you feel, when symptoms started, how they've changed, etc. Under no circumstances mention or hint at the diagnosis name.  
Keep answers concise, natural, and include details like pain quality, timing, triggers, and any self-care you've tried."""
        
        # Structure the custom patient data to match file-based patient format
        patient_data = {
            'type': 'custom',
            'prompt_template': default_prompt_template,
            'patient_details': {
                'age': str(custom_patient_details['age']),
                'gender': custom_patient_details['gender'],
                'occupation': custom_patient_details['occupation'],
                'medical_history': custom_patient_details.get('medical_history', 'No significant medical history'),
                'illness': custom_patient_details['illness'],
                'recent_exposure': custom_patient_details.get('recent_exposure', 'None reported')
            },
            'voice_id': 'Fritz-PlayAI'  # Default voice, can be changed later
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
        
        logger.info(f"Created legacy custom patient conversation {current_conversation_id} with data: {patient_data}")
        
        return jsonify({
            'status': 'success',
            'message': 'Custom patient created successfully (legacy mode)',
            'conversation_id': current_conversation_id,
            'patient_details': {
                'age': patient_data['patient_details']['age'],
                'gender': patient_data['patient_details']['gender'],
                'occupation': patient_data['patient_details']['occupation'],
                'medical_history': patient_data['patient_details']['medical_history'],
                'recent_exposure': patient_data['patient_details']['recent_exposure']
                # Note: illness is intentionally excluded from response for UI display
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
        
        # ✅ FIX: Initialize conversation_id properly to avoid UnboundLocalError
        target_conversation_id = current_conversation_id  # Start with global value
        
        # Get conversation ID from form data if provided
        form_conversation_id = request.form.get('conversation_id')
        if form_conversation_id:
            try:
                target_conversation_id = int(form_conversation_id)
                logger.info(f"Using conversation_id from form: {target_conversation_id}")
            except (ValueError, TypeError):
                logger.warning(f"Invalid conversation_id in form: {form_conversation_id}")
        
        # Update the global variable
        current_conversation_id = target_conversation_id
        
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
            # ===== ENHANCED CONVERSATION DATA RETRIEVAL LOGGING =====
            logger.info("🔄 RETRIEVING CONVERSATION DATA FROM DATABASE")
            logger.info(f"   Conversation ID: {current_conversation_id}")
            
            # Get all conversation data for comprehensive logging
            all_conversation_data = get_all_conversation_data(current_conversation_id)
            logger.info(f"   Available Data Keys: {list(all_conversation_data.keys()) if all_conversation_data else 'None'}")
            
            # Retrieve patient data specifically
            retrieved_data = get_conversation_data(current_conversation_id, 'patient_data')
            if retrieved_data:
                patient_data = retrieved_data
                
                # Log detailed patient data information
                logger.info("✅ PATIENT DATA RETRIEVED SUCCESSFULLY")
                logger.info(f"   Patient Type: {patient_data.get('type', 'unknown')}")
                
                if patient_data.get('type') == 'ai_generated':
                    generation_metadata = patient_data.get('generation_metadata', {})
                    logger.info("   🏥 AI-Generated Case Details:")
                    logger.info(f"      Specialty: {generation_metadata.get('specialty', 'Unknown')}")
                    logger.info(f"      Input Symptoms: {generation_metadata.get('input_symptoms', [])}")
                    logger.info(f"      Severity: {generation_metadata.get('severity', 'Unknown')}")
                    logger.info(f"      Difficulty: {generation_metadata.get('difficulty_level', 'Unknown')}")
                    
                    patient_details = patient_data.get('patient_details', {})
                    logger.info("   👤 Patient Demographics:")
                    logger.info(f"      Age: {patient_details.get('age', 'Unknown')}")
                    logger.info(f"      Gender: {patient_details.get('gender', 'Unknown')}")
                    logger.info(f"      Occupation: {patient_details.get('occupation', 'Unknown')}")
                    logger.info(f"      Medical History: {patient_details.get('medical_history', 'None')}")
                    logger.info(f"      Hidden Diagnosis: {patient_details.get('illness', 'Unknown')}")
                    
                elif patient_data.get('type') == 'custom':
                    patient_details = patient_data.get('patient_details', {})
                    logger.info("   👤 Custom Patient Details:")
                    logger.info(f"      Age: {patient_details.get('age', 'Unknown')}")
                    logger.info(f"      Gender: {patient_details.get('gender', 'Unknown')}")
                    logger.info(f"      Occupation: {patient_details.get('occupation', 'Unknown')}")
                    logger.info(f"      Illness: {patient_details.get('illness', 'Unknown')}")
                    
                # Log prompt template information
                if 'prompt_template' in patient_data:
                    template_length = len(patient_data['prompt_template'])
                    logger.info(f"   💬 Prompt Template: {template_length} characters")
                    
                # Log voice settings
                voice_id = patient_data.get('voice_id', 'Unknown')
                logger.info(f"   🔊 Voice ID: {voice_id}")
                
                # Log for Heroku monitoring 
                logger.info("📊 HEROKU_CONVERSATION_DATA: " + json.dumps({
                    'event': 'conversation_data_retrieved',
                    'conversation_id': current_conversation_id,
                    'patient_type': patient_data.get('type', 'unknown'),
                    'has_patient_data': True,
                    'data_keys_available': list(all_conversation_data.keys()) if all_conversation_data else [],
                    'patient_age': patient_details.get('age', 'Unknown') if 'patient_details' in patient_data else 'N/A',
                    'patient_gender': patient_details.get('gender', 'Unknown') if 'patient_details' in patient_data else 'N/A',
                    'timestamp': datetime.now().isoformat()
                }))
                
            else:
                patient_data = {}
                logger.warning("❌ NO PATIENT DATA FOUND")
                logger.info(f"   Conversation {current_conversation_id} has no associated patient simulation")
                
                # Check if there are any other data keys
                if all_conversation_data:
                    logger.info(f"   Other data available: {list(all_conversation_data.keys())}")
                    for key, value in all_conversation_data.items():
                        if key != 'patient_data':
                            value_preview = str(value)[:100] + "..." if len(str(value)) > 100 else str(value)
                            logger.info(f"      {key}: {value_preview}")
                else:
                    logger.info("   No data stored for this conversation")
                
                # Log for Heroku monitoring 
                logger.info("📊 HEROKU_CONVERSATION_DATA: " + json.dumps({
                    'event': 'conversation_data_retrieved',
                    'conversation_id': current_conversation_id,
                    'patient_type': 'none',
                    'has_patient_data': False,
                    'data_keys_available': list(all_conversation_data.keys()) if all_conversation_data else [],
                    'timestamp': datetime.now().isoformat()
                }))
        
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
    """
    Load a conversation into the active session.
    ✅ PHASE 4.1: Enhanced loading for AI-generated patient conversations.
    """
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
        logger.info(f"Loading conversation {conversation_id}: {conversation.get('title', 'Untitled')}")
        
        # ✅ PHASE 4.1: Enhanced patient data loading with type detection
        simulation_file = conversation.get('simulation_file')
        
        # ===== ENHANCED CONVERSATION LOADING LOGGING =====
        logger.info("📁 LOADING CONVERSATION DATA")
        logger.info(f"   Conversation ID: {conversation_id}")
        logger.info(f"   Title: {conversation.get('title', 'Untitled')}")
        logger.info(f"   Simulation File: {simulation_file or 'None'}")
        logger.info(f"   Created: {conversation.get('created_at', 'Unknown')}")
        logger.info(f"   Message Count: {len(conversation.get('messages', []))}")
        
        # Get all conversation data for comprehensive logging
        all_conversation_data = get_all_conversation_data(conversation_id)
        logger.info(f"   Stored Data Keys: {list(all_conversation_data.keys()) if all_conversation_data else 'None'}")
        
        # Log conversation history overview
        messages = conversation.get('messages', [])
        if messages:
            logger.info("📜 CONVERSATION HISTORY OVERVIEW:")
            logger.info(f"   Total Messages: {len(messages)}")
            
            # Log first few messages for context
            for i, msg in enumerate(messages[:3]):  # First 3 messages
                role = msg.get('role', 'unknown')
                content = msg.get('content', '')
                preview = content[:50] + "..." if len(content) > 50 else content
                logger.info(f"   {i+1}. {role.upper()}: {preview}")
            
            if len(messages) > 6:
                logger.info(f"   ... [{len(messages)-6} messages omitted] ...")
                
                # Show last few messages if we have many
                for i, msg in enumerate(messages[-3:], len(messages)-2):
                    role = msg.get('role', 'unknown')
                    content = msg.get('content', '')
                    preview = content[:50] + "..." if len(content) > 50 else content
                    logger.info(f"   {i}. {role.upper()}: {preview}")
        
        retrieved_patient_data = get_conversation_data(conversation_id, 'patient_data')
        
        if retrieved_patient_data:
            # Use stored patient data (AI-generated or custom)
            patient_data = retrieved_patient_data
            
            logger.info(f"✅ PATIENT SIMULATION DATA LOADED")
            patient_type = retrieved_patient_data.get('type', 'unknown')
            logger.info(f"   Patient Type: {patient_type}")
            
            if patient_type == 'ai_generated':
                generation_metadata = retrieved_patient_data.get('generation_metadata', {})
                patient_details = retrieved_patient_data.get('patient_details', {})
                
                logger.info(f"   🏥 AI Case Information:")
                logger.info(f"      Specialty: {generation_metadata.get('specialty', 'Unknown')}")
                logger.info(f"      Diagnosis: {patient_details.get('illness', 'Unknown')}")
                logger.info(f"      Patient: {patient_details.get('gender', 'Unknown')}, Age {patient_details.get('age', 'Unknown')}")
                logger.info(f"      Occupation: {patient_details.get('occupation', 'Unknown')}")
                logger.info(f"      Symptoms: {generation_metadata.get('input_symptoms', [])}")
                logger.info(f"      Severity: {generation_metadata.get('severity', 'Unknown')}")
                logger.info(f"      Difficulty: {generation_metadata.get('difficulty_level', 'Unknown')}")
                
                learning_objectives = generation_metadata.get('learning_objectives', [])
                if learning_objectives:
                    logger.info(f"      Learning Objectives: {len(learning_objectives)} defined")
                    for i, obj in enumerate(learning_objectives[:3], 1):
                        logger.info(f"         {i}. {obj}")
                
                current_patient_simulation = 'AI Generated Case'
                
            elif patient_type == 'custom':
                patient_details = retrieved_patient_data.get('patient_details', {})
                logger.info(f"   👤 Custom Patient Information:")
                logger.info(f"      Age: {patient_details.get('age', 'Unknown')}")
                logger.info(f"      Gender: {patient_details.get('gender', 'Unknown')}")
                logger.info(f"      Occupation: {patient_details.get('occupation', 'Unknown')}")
                logger.info(f"      Medical History: {patient_details.get('medical_history', 'None')}")
                logger.info(f"      Condition: {patient_details.get('illness', 'Unknown')}")
                current_patient_simulation = 'Custom Patient'
                
            else:
                logger.info(f"   📄 File-based or Other Patient Type")
                current_patient_simulation = simulation_file or 'Unknown'
            
            # ✅ PHASE 4.1: Validate retrieved data structure
            is_valid, validation_errors = validate_patient_data_structure(retrieved_patient_data)
            if not is_valid:
                logger.warning(f"⚠️ PATIENT DATA VALIDATION ISSUES:")
                for error in validation_errors:
                    logger.warning(f"      - {error}")
            else:
                logger.info(f"✅ Patient data structure validation passed")
                
        elif simulation_file and os.path.exists(simulation_file):
            # Load from file-based simulation
            logger.info(f"📂 LOADING FILE-BASED SIMULATION")
            logger.info(f"   File Path: {simulation_file}")
            patient_data = initialize_patient_data(simulation_file)
            current_patient_simulation = simulation_file
            
            if patient_data:
                logger.info(f"✅ File-based patient data loaded successfully")
                patient_details = patient_data.get('patient_details', {})
                logger.info(f"   Patient Age: {patient_details.get('age', 'Unknown')}")
                logger.info(f"   Patient Gender: {patient_details.get('gender', 'Unknown')}")
                logger.info(f"   Patient Condition: {patient_details.get('illness', 'Unknown')}")
            else:
                logger.warning(f"❌ Failed to load file-based patient data")
            
        else:
            # No patient data available
            logger.warning(f"❌ NO PATIENT DATA AVAILABLE")
            logger.info(f"   No stored patient data found")
            logger.info(f"   No valid simulation file: {simulation_file}")
            patient_data = None
            current_patient_simulation = None
        
        # ✅ PHASE 4.1: Get additional conversation metadata
        voice_id = get_conversation_data(conversation_id, 'voice_id')
        
        # Convert database messages to conversation history format
        conversation_history = [
            {"role": msg["role"], "content": msg["content"]}
            for msg in conversation.get("messages", [])
        ]
        
        # ✅ PHASE 4.1: Build enhanced response with detailed metadata
        response_data = {
            'status': 'success',
            'message': f'Conversation {conversation_id} loaded successfully',
            'conversation': conversation,
            'voice_id': voice_id,
            'message_count': len(conversation_history),
            'has_patient_data': patient_data is not None
        }
        
        # Add patient type information if available
        if patient_data:
            response_data['patient_type'] = patient_data.get('type', 'unknown')
            
            # Add AI-generated case info for display
            if patient_data.get('type') == 'ai_generated':
                generation_metadata = patient_data.get('generation_metadata', {})
                response_data['ai_case_summary'] = {
                    'specialty': generation_metadata.get('specialty', 'Unknown'),
                    'symptoms': generation_metadata.get('input_symptoms', []),
                    'severity': generation_metadata.get('severity', 'Unknown'),
                    'difficulty': generation_metadata.get('difficulty_level', 'intermediate')
                }
            
            # Add migration info if available
            if 'migration_metadata' in patient_data:
                response_data['migration_info'] = patient_data['migration_metadata']
        
        # Add any additional stored data keys (for debugging/admin purposes)
        if all_conversation_data:
            response_data['stored_data_keys'] = list(all_conversation_data.keys())
            
        logger.info(f"Successfully loaded conversation {conversation_id} with {len(conversation_history)} messages")
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Error loading conversation {conversation_id}: {str(e)}", exc_info=True)
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
    """
    Get details of the currently selected patient simulation.
    ✅ PHASE 4.1: Enhanced retrieval logic for AI-generated cases.
    """
    try:
        # Check if we have an active conversation with patient data
        if current_conversation_id:
            # Try to get patient data from database
            retrieved_patient_data = get_conversation_data(current_conversation_id, 'patient_data')
            if retrieved_patient_data:
                patient_data_to_use = retrieved_patient_data
                logger.debug(f"Retrieved patient data from database for conversation {current_conversation_id}")
            else:
                patient_data_to_use = patient_data
                logger.debug("Using in-memory patient data")
        else:
            patient_data_to_use = patient_data
            logger.debug("Using global patient data")
        
        if not patient_data_to_use or not patient_data_to_use.get('patient_details'):
            return jsonify({
                'status': 'error',
                'message': 'No patient simulation selected or invalid simulation data'
            }), 404
        
        # ✅ PHASE 4.1: Validate patient data structure before processing
        is_valid, validation_errors = validate_patient_data_structure(patient_data_to_use)
        if not is_valid:
            logger.warning(f"Invalid patient data structure: {validation_errors}")
            # Continue with fallback handling rather than failing
        
        # Get patient details, excluding the 'illness' field (hidden diagnosis)
        details = patient_data_to_use.get('patient_details', {}).copy()
        if 'illness' in details:
            del details['illness']  # Remove illness field (hidden diagnosis)
        
        response_data = {
            'status': 'success',
            'patient_details': details,
            'simulation_file': current_patient_simulation,
            'patient_type': patient_data_to_use.get('type', 'unknown')
        }
        
        # ✅ PHASE 4.1: Enhanced handling for AI-generated cases
        if patient_data_to_use.get('type') == 'ai_generated':
            generation_metadata = patient_data_to_use.get('generation_metadata', {})
            response_data['ai_case_info'] = {
                'specialty': generation_metadata.get('specialty', 'Unknown'),
                'input_symptoms': generation_metadata.get('input_symptoms', []),
                'severity': generation_metadata.get('severity', 'Unknown'),
                'difficulty_level': generation_metadata.get('difficulty_level', 'intermediate'),
                'learning_objectives': generation_metadata.get('learning_objectives', []),
                'differential_diagnoses': generation_metadata.get('differential_diagnoses', []),
                'clinical_notes': generation_metadata.get('clinical_notes', ''),
                'generation_warnings': generation_metadata.get('generation_warnings', [])
            }
            
            # ✅ PHASE 4.1: Enhanced symptom mapping with validation
            symptom_mapping = {
                'chest_pain': 'Chest pain',
                'shortness_breath': 'Shortness of breath',
                'palpitations': 'Palpitations',
                'dizziness': 'Dizziness',
                'fatigue': 'Fatigue',
                'swelling_legs': 'Leg swelling',
                'irregular_heartbeat': 'Irregular heartbeat',
                'headache': 'Headache',
                'seizure': 'Seizure',
                'memory_loss': 'Memory loss',
                'confusion': 'Confusion',
                'weakness': 'Weakness',
                'numbness': 'Numbness',
                'speech_difficulty': 'Speech difficulty',
                'vision_changes': 'Vision changes',
                'joint_pain': 'Joint pain',
                'back_pain': 'Back pain',
                'limited_mobility': 'Limited mobility',
                'muscle_pain': 'Muscle pain',
                'bone_pain': 'Bone pain',
                'stiffness': 'Stiffness',
                'abdominal_pain': 'Abdominal pain',
                'nausea': 'Nausea',
                'vomiting': 'Vomiting',
                'diarrhea': 'Diarrhea',
                'constipation': 'Constipation',
                'bloating': 'Bloating',
                'loss_appetite': 'Loss of appetite',
                'cough': 'Cough',
                'wheezing': 'Wheezing',
                'chest_tightness': 'Chest tightness',
                'sputum_production': 'Sputum production',
                'difficulty_breathing': 'Difficulty breathing',
                'rash': 'Rash',
                'itching': 'Itching',
                'skin_lesion': 'Skin lesion',
                'dry_skin': 'Dry skin',
                'skin_discoloration': 'Skin discoloration',
                'fever': 'Fever',
                'severe_pain': 'Severe pain',
                'rapid_heart_rate': 'Rapid heart rate',
                'low_blood_pressure': 'Low blood pressure',
                'high_blood_pressure': 'High blood pressure'
            }
            
            # Map symptoms to display names with fallback
            input_symptoms = generation_metadata.get('input_symptoms', [])
            response_data['ai_case_info']['symptom_display_names'] = [
                symptom_mapping.get(symptom, symptom.replace('_', ' ').title()) 
                for symptom in input_symptoms
            ]
        
        # ✅ PHASE 4.1: Add migration info if available
        if 'migration_metadata' in patient_data_to_use:
            response_data['migration_info'] = patient_data_to_use['migration_metadata']
        
        logger.debug(f"Successfully retrieved patient details for type: {patient_data_to_use.get('type', 'unknown')}")
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Error getting current patient details: {str(e)}", exc_info=True)
        return jsonify({
            'status': 'error',
            'message': f'Error getting patient details: {str(e)}'
        }), 500

@app.route('/api/medical-knowledge', methods=['GET'])
def get_medical_knowledge():
    """Get medical specialties and symptoms for the frontend form"""
    try:
        # Debug: Check what we're getting from the chain
        logger.info("Calling get_all_specialties()...")
        specialties = get_all_specialties()
        logger.info(f"get_all_specialties() returned type: {type(specialties)}")
        
        # Validate data type before processing
        if not isinstance(specialties, dict):
            logger.error(f"Expected dict but got {type(specialties)}: {specialties}")
            return jsonify({
                'status': 'error',
                'message': f'Invalid data type from medical system: expected dict, got {type(specialties)}'
            }), 500
        
        # Build response with specialties and their associated symptoms
        response_data = {
            'status': 'success',
            'specialties': {},
            'all_symptoms': {}
        }
        
        # Add specialty information with error handling for each specialty
        for specialty_key, specialty_name in specialties.items():
            try:
                logger.debug(f"Processing specialty: {specialty_key}")
                response_data['specialties'][specialty_key] = {
                    'name': specialty_name,
                    'description': specialty_name,  # Fallback if description lookup fails
                    'symptoms': get_available_symptoms_for_specialty(specialty_key)
                }
            except Exception as e:
                logger.error(f"Error processing specialty {specialty_key}: {e}")
                # Continue with other specialties instead of failing completely
                continue
        
        # Add all symptoms with human-readable names
        symptom_mapping = {
            'chest_pain': 'Chest pain',
            'shortness_breath': 'Shortness of breath',
            'palpitations': 'Palpitations',
            'dizziness': 'Dizziness',
            'fatigue': 'Fatigue',
            'swelling_legs': 'Leg swelling',
            'irregular_heartbeat': 'Irregular heartbeat',
            'headache': 'Headache',
            'seizure': 'Seizure',
            'memory_loss': 'Memory loss',
            'confusion': 'Confusion',
            'weakness': 'Weakness',
            'numbness': 'Numbness',
            'speech_difficulty': 'Speech difficulty',
            'vision_changes': 'Vision changes',
            'joint_pain': 'Joint pain',
            'back_pain': 'Back pain',
            'limited_mobility': 'Limited mobility',
            'muscle_pain': 'Muscle pain',
            'bone_pain': 'Bone pain',
            'stiffness': 'Stiffness',
            'abdominal_pain': 'Abdominal pain',
            'nausea': 'Nausea',
            'vomiting': 'Vomiting',
            'diarrhea': 'Diarrhea',
            'constipation': 'Constipation',
            'bloating': 'Bloating',
            'loss_appetite': 'Loss of appetite',
            'cough': 'Cough',
            'wheezing': 'Wheezing',
            'chest_tightness': 'Chest tightness',
            'sputum_production': 'Sputum production',
            'difficulty_breathing': 'Difficulty breathing',
            'rash': 'Rash',
            'itching': 'Itching',
            'skin_lesion': 'Skin lesion',
            'dry_skin': 'Dry skin',
            'skin_discoloration': 'Skin discoloration',
            'fever': 'Fever',
            'severe_pain': 'Severe pain',
            'rapid_heart_rate': 'Rapid heart rate',
            'low_blood_pressure': 'Low blood pressure',
            'high_blood_pressure': 'High blood pressure'
        }
        
        response_data['all_symptoms'] = symptom_mapping
        
        logger.info(f"Successfully built medical knowledge response with {len(response_data['specialties'])} specialties")
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Error getting medical knowledge: {str(e)}", exc_info=True)
        return jsonify({
            'status': 'error',
            'message': f'Error getting medical knowledge: {str(e)}'
        }), 500

# NEW: Diagnosis submission endpoint
@app.route('/api/submit-diagnosis', methods=['POST'])
def submit_diagnosis():
    """Submit a diagnosis for evaluation against the correct answer"""
    try:
        data = request.get_json()
        conversation_id = data.get('conversation_id')
        user_diagnosis = data.get('user_diagnosis', '').strip()
        
        logger.info(f"Diagnosis submission received for conversation {conversation_id}")
        logger.info(f"User diagnosis: '{user_diagnosis}'")
        
        # Validation
        if not conversation_id:
            logger.warning("No conversation ID provided in diagnosis submission")
            return jsonify({
                'status': 'error',
                'message': 'No conversation ID provided'
            }), 400
            
        if not user_diagnosis:
            logger.warning("Empty diagnosis submitted")
            return jsonify({
                'status': 'error',
                'message': 'No diagnosis provided'
            }), 400
        
        # Get the correct diagnosis from patient data
        patient_data = get_conversation_data(conversation_id, 'patient_data')
        if not patient_data:
            logger.error(f"No patient data found for conversation {conversation_id}")
            return jsonify({
                'status': 'error',
                'message': 'No patient data found for this conversation'
            }), 404
            
        correct_diagnosis = patient_data.get('patient_details', {}).get('illness')
        if not correct_diagnosis:
            logger.error(f"No diagnosis available for conversation {conversation_id}")
            return jsonify({
                'status': 'error',
                'message': 'No diagnosis available for this patient'
            }), 404
        
        logger.info(f"Correct diagnosis: '{correct_diagnosis}'")
        
        # Evaluate the diagnosis
        evaluation_result = evaluate_diagnosis(user_diagnosis, correct_diagnosis)
        
        logger.info(f"Evaluation result: {evaluation_result}")
        
        # Store the diagnosis attempt in the database
        attempt_data = {
            'user_diagnosis': user_diagnosis,
            'correct_diagnosis': correct_diagnosis,
            'timestamp': datetime.now().isoformat(),
            'similarity_score': evaluation_result['similarity_score'],
            'is_correct': evaluation_result['is_correct'],
            'is_close': evaluation_result['is_close']
        }
        
        # Get existing attempts or create new list
        existing_attempts = get_conversation_data(conversation_id, 'diagnosis_attempts') or []
        existing_attempts.append(attempt_data)
        store_conversation_data(conversation_id, 'diagnosis_attempts', existing_attempts)
        
        logger.info(f"Diagnosis attempt stored for conversation {conversation_id}")
        
        # Prepare response
        response_data = {
            'status': 'success',
            'is_correct': evaluation_result['is_correct'],
            'is_close': evaluation_result['is_close'],
            'similarity_score': evaluation_result['similarity_score'],
            'feedback': evaluation_result['feedback']
        }
        
        # Only include correct diagnosis in response if user was correct
        if evaluation_result['is_correct']:
            response_data['correct_diagnosis'] = correct_diagnosis
        
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Error in submit_diagnosis: {str(e)}", exc_info=True)
        return jsonify({
            'status': 'error',
            'message': f'Error processing diagnosis: {str(e)}'
        }), 500

def evaluate_diagnosis(user_diagnosis: str, correct_diagnosis: str) -> Dict[str, Any]:
    """
    Evaluate user diagnosis against correct diagnosis using fuzzy matching
    
    Returns:
        Dict with evaluation results including similarity score and feedback
    """
    try:
        logger.info(f"Evaluating diagnosis: '{user_diagnosis}' vs '{correct_diagnosis}'")
        
        # Normalize both diagnoses for comparison
        user_clean = normalize_diagnosis(user_diagnosis)
        correct_clean = normalize_diagnosis(correct_diagnosis)
        
        logger.debug(f"Normalized user: '{user_clean}' | Normalized correct: '{correct_clean}'")
        
        # Calculate similarity scores using multiple methods
        sequence_similarity = SequenceMatcher(None, user_clean, correct_clean).ratio()
        
        # Check for keyword matches and synonyms
        keyword_similarity = calculate_keyword_similarity(user_clean, correct_clean)
        synonym_similarity = calculate_synonym_similarity(user_diagnosis, correct_diagnosis)
        
        # Combined score (weighted)
        combined_score = max(
            (sequence_similarity * 0.4) + (keyword_similarity * 0.3) + (synonym_similarity * 0.3),
            sequence_similarity,  # Don't let combined score be lower than direct match
            synonym_similarity    # Or synonym match
        )
        
        logger.debug(f"Similarity scores - Sequence: {sequence_similarity:.3f}, Keyword: {keyword_similarity:.3f}, Synonym: {synonym_similarity:.3f}, Combined: {combined_score:.3f}")
        
        # Determine result thresholds
        is_correct = combined_score >= 0.85
        is_close = 0.60 <= combined_score < 0.85
        
        # Generate feedback
        feedback = generate_diagnosis_feedback(
            user_diagnosis, 
            correct_diagnosis, 
            combined_score, 
            is_correct, 
            is_close
        )
        
        result = {
            'is_correct': is_correct,
            'is_close': is_close,
            'similarity_score': combined_score,
            'feedback': feedback,
            'sequence_similarity': sequence_similarity,
            'keyword_similarity': keyword_similarity,
            'synonym_similarity': synonym_similarity
        }
        
        logger.info(f"Evaluation complete - Correct: {is_correct}, Close: {is_close}, Score: {combined_score:.3f}")
        return result
        
    except Exception as e:
        logger.error(f"Error in evaluate_diagnosis: {str(e)}", exc_info=True)
        return {
            'is_correct': False,
            'is_close': False,
            'similarity_score': 0.0,
            'feedback': 'Error evaluating diagnosis. Please try again.',
            'sequence_similarity': 0.0,
            'keyword_similarity': 0.0,
            'synonym_similarity': 0.0
        }

def normalize_diagnosis(diagnosis: str) -> str:
    """Normalize diagnosis text for comparison"""
    try:
        # Convert to lowercase
        normalized = diagnosis.lower().strip()
        
        # Remove common medical prefixes/suffixes that don't affect core meaning
        common_removals = [
            'acute', 'chronic', 'mild', 'moderate', 'severe',
            'primary', 'secondary', 'syndrome', 'disease',
            'disorder', 'condition', 'episode', 'attack'
        ]
        
        # Split into words and filter
        words = normalized.split()
        filtered_words = []
        
        for word in words:
            # Remove punctuation from word
            clean_word = re.sub(r'[^\w]', '', word)
            # Keep word if it's not in removal list and not empty
            if clean_word and clean_word not in common_removals:
                filtered_words.append(clean_word)
        
        # Rejoin words
        normalized = ' '.join(filtered_words)
        
        logger.debug(f"Normalized '{diagnosis}' to '{normalized}'")
        return normalized
        
    except Exception as e:
        logger.error(f"Error normalizing diagnosis '{diagnosis}': {str(e)}")
        return diagnosis.lower().strip()

def calculate_keyword_similarity(user_diagnosis: str, correct_diagnosis: str) -> float:
    """Calculate similarity based on key medical terms"""
    try:
        user_words = set(user_diagnosis.split())
        correct_words = set(correct_diagnosis.split())
        
        if not correct_words:
            return 0.0
        
        intersection = user_words.intersection(correct_words)
        union = user_words.union(correct_words)
        
        # Jaccard similarity
        jaccard = len(intersection) / len(union) if union else 0.0
        
        # Also check overlap ratio (how much of correct diagnosis is covered)
        overlap = len(intersection) / len(correct_words) if correct_words else 0.0
        
        # Return the better of the two scores
        return max(jaccard, overlap)
        
    except Exception as e:
        logger.error(f"Error calculating keyword similarity: {str(e)}")
        return 0.0

def calculate_synonym_similarity(user_diagnosis: str, correct_diagnosis: str) -> float:
    """Calculate similarity based on medical synonyms"""
    try:
        user_clean = user_diagnosis.lower().strip()
        correct_clean = correct_diagnosis.lower().strip()
        
        # Check if they're already similar enough
        if user_clean == correct_clean:
            return 1.0
        
        # Check synonyms
        max_similarity = 0.0
        
        for condition, synonyms in MEDICAL_SYNONYMS.items():
            all_terms = [condition] + synonyms
            
            user_match = any(term in user_clean for term in all_terms)
            correct_match = any(term in correct_clean for term in all_terms)
            
            if user_match and correct_match:
                # Both diagnoses match this condition group
                max_similarity = max(max_similarity, 0.9)
            elif user_match or correct_match:
                # Check if one is a broader/narrower term of the other
                if condition in user_clean or condition in correct_clean:
                    max_similarity = max(max_similarity, 0.7)
        
        return max_similarity
        
    except Exception as e:
        logger.error(f"Error calculating synonym similarity: {str(e)}")
        return 0.0

def generate_diagnosis_feedback(
    user_diagnosis: str, 
    correct_diagnosis: str, 
    similarity_score: float,
    is_correct: bool,
    is_close: bool
) -> str:
    """Generate helpful feedback for the diagnosis attempt"""
    
    try:
        if is_correct:
            return "Excellent! You correctly identified the condition."
        
        elif is_close:
            if similarity_score > 0.75:
                return "Very close! You're on the right track. Consider being more specific or check your spelling."
            else:
                return "You're thinking in the right direction. The condition is related to what you've identified."
        
        else:
            if similarity_score > 0.4:
                return "Some elements of your diagnosis are relevant, but the overall condition is different. Review the primary symptoms and their pattern."
            elif similarity_score > 0.2:
                return "Your diagnosis touches on relevant medical areas, but doesn't match the patient's condition. Consider other possibilities."
            else:
                return "This diagnosis doesn't match the patient's condition. Review the symptoms, patient history, and examination findings more carefully."
                
    except Exception as e:
        logger.error(f"Error generating feedback: {str(e)}")
        return "Unable to generate feedback. Please try again."

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
