"""
Configuration module for Flask Hello World API.
Provides environment-based configuration with secure defaults using os.getenv().
"""

import os


class Config:
    """Base configuration class with sensible defaults for all settings."""

    # Flask settings - use os.getenv() with sensible defaults
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 'yes')
    TESTING = os.getenv('TESTING', 'False').lower() in ('true', '1', 'yes')

    # Server settings
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', '5000'))

    # Application metadata
    APP_NAME = os.getenv('APP_NAME', 'Flask Hello World API')
    APP_VERSION = os.getenv('APP_VERSION', '1.0.0')

    # JSON settings
    JSONIFY_PRETTYPRINT_REGULAR = os.getenv('JSONIFY_PRETTYPRINT_REGULAR', 'True').lower() in ('true', '1', 'yes')
    JSON_SORT_KEYS = os.getenv('JSON_SORT_KEYS', 'False').lower() in ('true', '1', 'yes')

    # Security settings
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'True').lower() in ('true', '1', 'yes')
    SESSION_COOKIE_HTTPONLY = os.getenv('SESSION_COOKIE_HTTPONLY', 'True').lower() in ('true', '1', 'yes')
    SESSION_COOKIE_SAMESITE = os.getenv('SESSION_COOKIE_SAMESITE', 'Lax')

    # CORS settings
    CORS_ENABLED = os.getenv('CORS_ENABLED', 'True').lower() in ('true', '1', 'yes')
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')

    # Logging settings
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = os.getenv('LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class DevelopmentConfig(Config):
    """Development environment configuration with debug enabled."""

    DEBUG = os.getenv('DEBUG', 'True').lower() in ('true', '1', 'yes')
    ENV = 'development'
    PORT = int(os.getenv('PORT', '5001'))

    # Relaxed security for local development
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False').lower() in ('true', '1', 'yes')


class TestingConfig(Config):
    """Testing environment configuration for unit tests."""

    TESTING = os.getenv('TESTING', 'True').lower() in ('true', '1', 'yes')
    DEBUG = os.getenv('DEBUG', 'True').lower() in ('true', '1', 'yes')
    ENV = 'testing'

    # Use test-specific secret key
    SECRET_KEY = os.getenv('SECRET_KEY', 'test-secret-key-do-not-use-in-production')

    # Relaxed security for testing
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False').lower() in ('true', '1', 'yes')


class ProductionConfig(Config):
    """Production environment configuration with strict settings."""

    DEBUG = False
    TESTING = False
    ENV = 'production'

    # Enforce security settings in production (but still have defaults)
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'True').lower() in ('true', '1', 'yes')

    # Production should use strong secret key from environment
    SECRET_KEY = os.getenv('SECRET_KEY', 'CHANGE-THIS-IN-PRODUCTION-OR-SECURITY-IS-COMPROMISED')


# Configuration dictionary for easy access
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

# Alternative name for config dictionary
config_by_name = config


def get_config(config_name=None):
    """
    Get configuration class based on environment.

    Args:
        config_name: Configuration name ('development', 'production', 'testing').
                    If None, uses FLASK_ENV environment variable.

    Returns:
        Configuration class instance.
    """
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    return config.get(config_name, config['default'])
