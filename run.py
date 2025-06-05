#!/usr/bin/env python3
"""
Doctor Simulation Application Entry Point
Uses application factory pattern for better modularity and testing
"""

import os
import sys
import argparse
import logging
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import application factory
from app_factory import create_app
from utils.patient_simulation import load_patient_simulation

logger = logging.getLogger(__name__)

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Run the Doctor Simulation voice conversation app'
    )
    parser.add_argument(
        '--port', 
        type=int, 
        default=5000, 
        help='Port to run the app on (default: 5000)'
    )
    parser.add_argument(
        '--patient-file', 
        type=str, 
        help='Path to patient simulation JSON file'
    )
    parser.add_argument(
        '--host',
        type=str,
        default='0.0.0.0',
        help='Host to bind to (default: 0.0.0.0)'
    )
    parser.add_argument(
        '--config',
        type=str,
        default='default',
        choices=['default', 'production', 'development'],
        help='Configuration environment (default: default)'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug mode'
    )
    
    return parser.parse_args()

def validate_environment():
    """Validate required environment variables and setup"""
    required_env_vars = ['GROQ_API_KEY']
    missing_vars = []
    
    for var in required_env_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        logger.error("Please check your .env file or environment setup")
        return False
    
    # Log API key status (without revealing the key)
    api_key = os.environ.get('GROQ_API_KEY')
    if api_key:
        logger.info(f'GROQ_API_KEY found - length: {len(api_key)}')
    
    return True

def setup_directories():
    """Create necessary directories if they don't exist"""
    directories = ['utils', 'blueprints', 'static/js/modules', 'templates']
    
    for directory in directories:
        dir_path = project_root / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Ensured directory exists: {dir_path}")

def load_patient_data_if_provided(patient_file):
    """Load patient simulation data if file is provided"""
    if not patient_file:
        return None
        
    if not os.path.exists(patient_file):
        logger.error(f"Patient simulation file not found: {patient_file}")
        return None
    
    try:
        patient_data = load_patient_simulation(patient_file)
        if patient_data:
            logger.info(f'Loaded patient data from {patient_file}')
            return patient_data
        else:
            logger.error(f'Failed to load patient data from {patient_file}')
            return None
    except Exception as e:
        logger.error(f'Error loading patient file {patient_file}: {e}')
        return None

def main():
    """Main application entry point"""
    try:
        # Parse command line arguments
        args = parse_arguments()
        
        # Validate environment
        if not validate_environment():
            sys.exit(1)
        
        # Setup necessary directories
        setup_directories()
        
        # Load patient data if provided
        patient_data = load_patient_data_if_provided(args.patient_file)
        
        # Create Flask application using factory
        config_name = 'production' if not args.debug else 'development'
        app = create_app(config_name)
        
        # Override debug setting if specified
        if args.debug:
            app.config['DEBUG'] = True
        
        # Get port from environment variable (for Heroku) or use argument
        port = int(os.environ.get('PORT', args.port))
        
        # Log startup information
        logger.info(f'Starting Doctor Simulation app on {args.host}:{port}')
        logger.info(f'Configuration: {config_name}')
        logger.info(f'Debug mode: {app.config.get("DEBUG", False)}')
        
        if patient_data:
            logger.info(f'Patient simulation loaded: {args.patient_file}')
        
        # Log registered routes for debugging
        logger.debug("Registered URL Rules:")
        for rule in app.url_map.iter_rules():
            logger.debug(f"Route: {rule}, Endpoint: {rule.endpoint}")
        
        # Run the application
        app.run(
            host=args.host,
            port=port,
            debug=app.config.get('DEBUG', False),
            threaded=True
        )
        
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
    except Exception as e:
        logger.error(f"Failed to start application: {e}", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    main() 