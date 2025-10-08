"""
Pytest configuration and fixtures for Flask Hello World API tests.
"""

import pytest
from app import create_app


@pytest.fixture
def app():
    """
    Create and configure a Flask application instance for testing.

    Returns:
        Flask app configured for testing environment
    """
    app = create_app('testing')

    # Additional test-specific configuration can be added here
    app.config.update({
        'TESTING': True,
    })

    yield app


@pytest.fixture
def client(app):
    """
    Create a test client for the Flask application.

    Args:
        app: Flask application fixture

    Returns:
        Flask test client for making requests
    """
    return app.test_client()


@pytest.fixture
def runner(app):
    """
    Create a test CLI runner for the Flask application.

    Args:
        app: Flask application fixture

    Returns:
        Flask CLI test runner
    """
    return app.test_cli_runner()
