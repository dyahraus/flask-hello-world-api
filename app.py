"""
Flask Hello World API
A simple API that returns hello world messages and provides health check endpoint.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from config import get_config
from datetime import datetime, timezone
import os


def create_app(config_name=None):
    """
    Application factory pattern for creating Flask app instances.

    Args:
        config_name: Configuration environment name (development, testing, production)

    Returns:
        Flask application instance
    """
    app = Flask(__name__)

    # Load configuration using get_config helper
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app.config.from_object(get_config(config_name))

    # Configure CORS if enabled
    if app.config.get('CORS_ENABLED', True):
        cors_origins = app.config.get('CORS_ORIGINS', '*')
        # Parse comma-separated origins or use wildcard
        origins = cors_origins if cors_origins == '*' else [o.strip() for o in cors_origins.split(',')]
        CORS(app, origins=origins, supports_credentials=True)

    @app.route('/', methods=['GET'])
    def hello_world():
        """
        Main hello world endpoint.

        Returns:
            JSON response with hello world message
        """
        return jsonify({
            'message': 'Hello, World!',
            'status': 'success'
        }), 200

    @app.route('/api/hello', methods=['GET'])
    def api_hello():
        """
        API hello endpoint with optional name parameter.

        Query Parameters:
            name (optional): Name to personalize the greeting

        Returns:
            JSON response with personalized or default greeting
        """
        name = request.args.get('name')

        if name:
            message = f'Hello, {name}!'
        else:
            message = 'Hello, World!'

        return jsonify({
            'message': message,
            'status': 'success'
        }), 200

    @app.route('/health', methods=['GET'])
    def health_check():
        """
        Health check endpoint for monitoring and deployment verification.

        Returns:
            JSON response with health status and ISO8601 timestamp
        """
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now(timezone.utc).isoformat()
        }), 200

    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors with JSON response."""
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested resource was not found'
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors with JSON response."""
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred'
        }), 500

    return app


if __name__ == '__main__':
    app = create_app()
    # Get port from environment variable, default to 5001
    port = int(os.getenv('PORT', 5001))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=app.config.get('DEBUG', False)
    )
