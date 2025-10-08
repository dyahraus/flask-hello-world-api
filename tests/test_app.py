"""
Unit tests for Flask Hello World API endpoints.
"""

import pytest
from datetime import datetime, timezone
from app import create_app


class TestHelloWorldEndpoint:
    """Test cases for the hello world endpoint."""

    def test_hello_world_success(self, client):
        """Test that hello world endpoint returns correct response."""
        response = client.get('/')

        assert response.status_code == 200
        assert response.is_json

        data = response.get_json()
        assert data['message'] == 'Hello, World!'
        assert data['status'] == 'success'

    def test_hello_world_method_not_allowed(self, client):
        """Test that POST method is not allowed on hello world endpoint."""
        response = client.post('/')

        assert response.status_code == 405


class TestApiHelloEndpoint:
    """Test cases for the /api/hello endpoint."""

    def test_api_hello_without_name(self, client):
        """Test that /api/hello endpoint returns default greeting without name parameter."""
        response = client.get('/api/hello')

        assert response.status_code == 200
        assert response.is_json

        data = response.get_json()
        assert data['message'] == 'Hello, World!'
        assert data['status'] == 'success'

    def test_api_hello_with_name(self, client):
        """Test that /api/hello endpoint returns personalized greeting with name parameter."""
        response = client.get('/api/hello?name=Alice')

        assert response.status_code == 200
        assert response.is_json

        data = response.get_json()
        assert data['message'] == 'Hello, Alice!'
        assert data['status'] == 'success'

    def test_api_hello_with_different_names(self, client):
        """Test that /api/hello endpoint handles different name values."""
        names = ['Bob', 'Charlie', 'Developer']

        for name in names:
            response = client.get(f'/api/hello?name={name}')
            data = response.get_json()

            assert response.status_code == 200
            assert data['message'] == f'Hello, {name}!'
            assert data['status'] == 'success'

    def test_api_hello_content_type(self, client):
        """Test that /api/hello endpoint returns JSON content type."""
        response = client.get('/api/hello')

        assert response.content_type == 'application/json'

    def test_api_hello_method_not_allowed(self, client):
        """Test that POST method is not allowed on /api/hello endpoint."""
        response = client.post('/api/hello')

        assert response.status_code == 405


class TestHealthCheckEndpoint:
    """Test cases for the health check endpoint."""

    def test_health_check_success(self, client):
        """Test that health check endpoint returns healthy status with timestamp."""
        response = client.get('/health')

        assert response.status_code == 200
        assert response.is_json

        data = response.get_json()
        assert data['status'] == 'healthy'
        assert 'timestamp' in data

        # Verify timestamp is in valid ISO8601 format
        try:
            datetime.fromisoformat(data['timestamp'].replace('Z', '+00:00'))
        except ValueError:
            pytest.fail(f"Invalid ISO8601 timestamp format: {data['timestamp']}")

    def test_health_check_response_structure(self, client):
        """Test that health check endpoint returns correct response structure."""
        response = client.get('/health')

        assert response.status_code == 200
        assert response.is_json

        data = response.get_json()

        # Verify response has exactly the expected keys
        expected_keys = {'status', 'timestamp'}
        assert set(data.keys()) == expected_keys, f"Expected keys {expected_keys}, got {set(data.keys())}"

        # Verify status field is a string
        assert isinstance(data['status'], str), "Status should be a string"
        assert data['status'] == 'healthy', "Status should be 'healthy'"

        # Verify timestamp field is a string
        assert isinstance(data['timestamp'], str), "Timestamp should be a string"

        # Verify timestamp is not empty
        assert len(data['timestamp']) > 0, "Timestamp should not be empty"

        # Verify timestamp is in valid ISO8601 format
        try:
            parsed_time = datetime.fromisoformat(data['timestamp'].replace('Z', '+00:00'))
            # Verify timestamp is recent (within last 5 seconds)
            time_diff = abs((datetime.now(timezone.utc) - parsed_time).total_seconds())
            assert time_diff < 5, f"Timestamp should be recent, but was {time_diff} seconds ago"
        except ValueError as e:
            pytest.fail(f"Invalid ISO8601 timestamp format: {data['timestamp']}, error: {e}")

    def test_health_check_method_not_allowed(self, client):
        """Test that POST method is not allowed on health check endpoint."""
        response = client.post('/health')

        assert response.status_code == 405


class TestErrorHandlers:
    """Test cases for error handlers."""

    def test_404_error_handler(self, client):
        """Test that 404 errors return JSON response."""
        response = client.get('/nonexistent-route')

        assert response.status_code == 404
        assert response.is_json

        data = response.get_json()
        assert data['error'] == 'Not Found'
        assert 'message' in data


class TestAppConfiguration:
    """Test cases for application configuration."""

    def test_development_config(self):
        """Test that development configuration is loaded correctly."""
        app = create_app('development')

        assert app.config['DEBUG'] is True
        assert app.config['TESTING'] is False
        assert app.config['ENV'] == 'development'

    def test_testing_config(self):
        """Test that testing configuration is loaded correctly."""
        app = create_app('testing')

        assert app.config['TESTING'] is True
        assert app.config['DEBUG'] is True
        assert app.config['ENV'] == 'testing'

    def test_production_config(self):
        """Test that production configuration has correct settings."""
        app = create_app('production')

        assert app.config['DEBUG'] is False
        assert app.config['TESTING'] is False
        assert app.config['ENV'] == 'production'


class TestContentType:
    """Test cases for response content types."""

    def test_hello_world_content_type(self, client):
        """Test that hello world endpoint returns JSON content type."""
        response = client.get('/')

        assert response.content_type == 'application/json'

    def test_health_check_content_type(self, client):
        """Test that health check endpoint returns JSON content type."""
        response = client.get('/health')

        assert response.content_type == 'application/json'
