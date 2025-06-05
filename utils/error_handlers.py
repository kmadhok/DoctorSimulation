from flask import jsonify, request
import logging

logger = logging.getLogger(__name__)

def register_error_handlers(app):
    """Register error handlers for the Flask application"""
    
    @app.errorhandler(400)
    def handle_bad_request(e):
        logger.warning('400 error: %s - Path: %s, Method: %s', 
                      e, request.path, request.method)
        return jsonify({
            'status': 'error',
            'message': 'Bad request. Please check your input.'
        }), 400
    
    @app.errorhandler(404)
    def handle_404(e):
        logger.warning('404 error: %s - Path: %s, Method: %s', 
                      e, request.path, request.method)
        return jsonify({
            'status': 'error',
            'message': f'Not Found: The requested URL {request.path} was not found on the server.'
        }), 404
    
    @app.errorhandler(500)
    def handle_internal_error(e):
        logger.error('500 error: %s - Path: %s, Method: %s', 
                    e, request.path, request.method, exc_info=True)
        return jsonify({
            'status': 'error',
            'message': 'Internal server error. Please try again later.'
        }), 500
    
    @app.errorhandler(Exception)
    def handle_unexpected_error(e):
        logger.error('Unexpected error: %s - Path: %s, Method: %s', 
                    e, request.path, request.method, exc_info=True)
        return jsonify({
            'status': 'error',
            'message': 'An unexpected error occurred. Please try again later.'
        }), 500 