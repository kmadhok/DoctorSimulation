from flask import Blueprint, request, jsonify, current_app
import os
import glob
import logging
from datetime import datetime

from utils.groq_integration import get_groq_response
from utils.groq_transcribe import transcribe_audio_data
from utils.groq_tts_speech import generate_speech_audio
from utils.patient_simulation import load_patient_simulation, get_patient_system_prompt
from utils.database import (
    create_conversation, add_message, get_conversations, 
    get_conversation, delete_conversation, update_conversation_title,
    store_conversation_data, get_conversation_data
)
import base64

logger = logging.getLogger(__name__)

api_bp = Blueprint('api', __name__)

# Global state - TODO: Move to proper state management
conversation_history = []
current_patient_simulation = None
current_conversation_id = None

@api_bp.route('/debug', methods=['GET'])
def debug_routes():
    """List all available routes for debugging"""
    routes = []
    for rule in current_app.url_map.iter_rules():
        routes.append({
            'endpoint': rule.endpoint,
            'methods': list(rule.methods),
            'path': str(rule)
        })
    return jsonify({
        'status': 'success',
        'routes': routes
    })

@api_bp.route('/patient-simulations', methods=['GET'])
def list_patient_simulations():
    """List available patient simulations"""
    try:
        logger.info('Listing patient simulations')
        simulations = get_available_patient_simulations()
        logger.debug('Found simulations: %s', simulations)
        
        return jsonify({
            'status': 'success',
            'simulations': simulations,
            'current_simulation': current_patient_simulation
        })
    except Exception as e:
        logger.error(f'Error listing simulations: {str(e)}', exc_info=True)
        return jsonify({
            'status': 'error',
            'message': f'Error listing simulations: {str(e)}'
        }), 500

@api_bp.route('/conversations/new', methods=['POST'])
def create_new_conversation():
    """Create a new empty conversation without a patient simulation"""
    global current_conversation_id, conversation_history
    
    try:
        title = f"New Conversation"
        current_conversation_id = create_conversation(title, None)
        conversation_history = []
        
        return jsonify({
            'status': 'success',
            'message': 'New conversation created',
            'conversation_id': current_conversation_id
        })
        
    except Exception as e:
        logger.error(f'Error creating conversation: {str(e)}', exc_info=True)
        return jsonify({
            'status': 'error',
            'message': f'Error creating conversation: {str(e)}'
        }), 500

@api_bp.route('/select-simulation', methods=['POST'])
def select_simulation():
    """Select a patient simulation"""
    global patient_data, current_patient_simulation, current_conversation_id, conversation_history
    
    # Early validation
    data = request.get_json()
    if not data or 'simulation_file' not in data:
        return jsonify({
            'status': 'error',
            'message': 'No simulation file specified'
        }), 400
    
    simulation_file = data['simulation_file']
    logger.info(f"Selecting simulation file: {simulation_file}")
    
    try:
        # Handle empty simulation file
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
            # Load the selected simulation
            logger.info(f"Loading simulation data from: {simulation_file}")
            patient_data = initialize_patient_data(simulation_file)
            
            # Guard clause for failed loading
            if not patient_data:
                logger.warning("No patient data loaded from simulation file")
                patient_data = {}
            
            # Ensure voice_id is present
            if 'voice_id' not in patient_data:
                logger.warning(f"No voice_id found in simulation file: {simulation_file}")
                patient_data['voice_id'] = 'Fritz-PlayAI'
        
        # Clear conversation history when changing simulations
        conversation_history = []
        
        # Create a new conversation
        title = "New Conversation"
        if simulation_file:
            title = f"Conversation with {os.path.basename(simulation_file)}"
        
        current_conversation_id = create_conversation(title, simulation_file)
        
        # Store patient data if available
        if patient_data:
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

@api_bp.route('/update-voice', methods=['POST'])
def update_voice():
    """Update the voice ID for a conversation"""
    global current_conversation_id
    
    # Early validation
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
    
    try:
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

@api_bp.route('/conversations', methods=['GET'])
def list_conversations():
    """Get a list of all saved conversations"""
    try:
        conversations = get_conversations()
        return jsonify({
            'status': 'success',
            'conversations': conversations
        })
    except Exception as e:
        logger.error(f'Error getting conversations: {str(e)}', exc_info=True)
        return jsonify({
            'status': 'error',
            'message': f'Error getting conversations: {str(e)}'
        }), 500

@api_bp.route('/conversations/<int:conversation_id>', methods=['GET'])
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
        logger.error(f'Error getting conversation: {str(e)}', exc_info=True)
        return jsonify({
            'status': 'error',
            'message': f'Error getting conversation: {str(e)}'
        }), 500

@api_bp.route('/conversations/<int:conversation_id>', methods=['DELETE'])
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
        logger.error(f'Error deleting conversation: {str(e)}', exc_info=True)
        return jsonify({
            'status': 'error',
            'message': f'Error deleting conversation: {str(e)}'
        }), 500

@api_bp.route('/conversations/<int:conversation_id>/load', methods=['POST'])
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

@api_bp.route('/diagnose', methods=['GET'])
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
        test_response = get_groq_response("Hello, this is a test.", model="llama3-8b-8192")
        results["tests"]["groq_text_api"] = "SUCCESS" if test_response else "FAILED"
    except Exception as e:
        results["tests"]["groq_text_api"] = f"ERROR: {str(e)}"
    
    return jsonify(results)

@api_bp.route('/current-patient-details', methods=['GET'])
def get_current_patient_details():
    """Get details of the currently selected patient simulation"""
    # Guard clause for no patient data
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

# Helper functions (to be moved to separate service files)
def get_available_patient_simulations():
    """Get list of available patient simulation files"""
    simulation_files = glob.glob('patient_simulation_*.json')
    return [os.path.basename(f) for f in simulation_files]

def initialize_patient_data(patient_file=None):
    """Initialize patient data from file"""
    global current_patient_simulation
    patient_data = {}
    if patient_file:
        patient_data = load_patient_simulation(patient_file)
        if patient_data:
            current_patient_simulation = patient_file
        else:
            logger.warning("Failed to load patient simulation data")
    return patient_data 