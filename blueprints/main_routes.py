from flask import Blueprint, render_template, jsonify
import logging

logger = logging.getLogger(__name__)

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Render the main page"""
    try:
        logger.info('Serving index page')
        return render_template('index.html')
    except Exception as e:
        logger.error(f'Error serving index page: {str(e)}', exc_info=True)
        return jsonify({
            'status': 'error',
            'message': 'Error loading main page'
        }), 500

@main_bp.route('/test', methods=['GET'])
def test_route():
    """Simple test route to verify Flask is working"""
    logger.info('Test route accessed')
    return jsonify({
        'status': 'success',
        'message': 'Flask server is running correctly'
    }) 