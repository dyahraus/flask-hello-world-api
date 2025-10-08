# Flask Hello World API

A simple Flask API that returns a hello world message with basic health check endpoint.

## Features

- RESTful API endpoint returning JSON hello world message
- Health check endpoint for monitoring
- Environment-based configuration (development, testing, production)
- Comprehensive test coverage with pytest
- Production-ready setup with error handling
- Easy deployment to cloud platforms (Heroku, Railway, Render, etc.)

## Tech Stack

- **Backend**: Flask 3.0.0, Python 3.11
- **Testing**: pytest 7.4.3, pytest-flask 1.3.0
- **WSGI Server**: Gunicorn 21.2.0

## Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- virtualenv (recommended)

## Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd flask-hello-world-api
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Set up environment variables

Copy the example environment file and configure as needed:

```bash
cp .env.example .env
```

Edit `.env` with your preferred settings:
- `FLASK_ENV`: Set to `development` or `production`
- `FLASK_DEBUG`: Set to `True` for development, `False` for production
- `SECRET_KEY`: Generate a secure random key for production

## Running the Application

### Development Mode

```bash
python app.py
```

The API will be available at `http://localhost:5000`

### Production Mode

Using Gunicorn (recommended):

```bash
gunicorn app:app
```

By default, Gunicorn runs on `http://localhost:8000`

With custom settings:

```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
```

## API Endpoints

The API provides three main endpoints:

- **GET** `/` - Root hello world message
- **GET** `/api/hello` - Personalized greeting with optional name parameter
- **GET** `/health` - Health check with timestamp

### Quick Examples

#### Root Endpoint
```bash
# Basic request
curl http://localhost:5001/

# With verbose output to see headers
curl -v http://localhost:5001/

# Pretty-print JSON response (using jq)
curl -s http://localhost:5001/ | jq
```

**Expected Response:**
```json
{
  "message": "Hello, World!",
  "status": "success",
  "timestamp": "2024-01-15T10:30:00.123456"
}
```

#### API Hello Endpoint
```bash
# Basic greeting
curl http://localhost:5001/api/hello

# Personalized greeting with name parameter
curl "http://localhost:5001/api/hello?name=Developer"

# URL-encoded name with spaces
curl "http://localhost:5001/api/hello?name=John%20Doe"

# Using -G flag for GET parameters
curl -G http://localhost:5001/api/hello --data-urlencode "name=Jane Smith"
```

**Expected Responses:**
```json
// Default greeting
{
  "message": "Hello, World!",
  "status": "success"
}

// Personalized greeting
{
  "message": "Hello, Developer!",
  "status": "success"
}
```

#### Health Check Endpoint
```bash
# Basic health check
curl http://localhost:5001/health

# Include response headers
curl -i http://localhost:5001/health

# Silent mode with formatted output
curl -s http://localhost:5001/health | jq

# Save response to file
curl http://localhost:5001/health -o health_check.json
```

**Expected Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.123456",
  "uptime": "0:05:23.456789"
}
```

#### Advanced Testing Examples

**Testing with Different HTTP Methods:**
```bash
# HEAD request (check if endpoint exists without fetching body)
curl -I http://localhost:5001/health

# OPTIONS request (check allowed methods)
curl -X OPTIONS http://localhost:5001/api/hello -i
```

**Performance Testing:**
```bash
# Measure response time
curl -w "\nTime: %{time_total}s\n" http://localhost:5001/api/hello

# Multiple requests with timing
for i in {1..10}; do
  curl -w "Request $i - Time: %{time_total}s\n" -s -o /dev/null http://localhost:5001/health
done
```

**Testing with Custom Headers:**
```bash
# Add custom headers
curl -H "User-Agent: TestClient/1.0" \
     -H "Accept: application/json" \
     http://localhost:5001/api/hello

# Test with specific content type
curl -H "Content-Type: application/json" http://localhost:5001/api/hello
```

**Error Handling Tests:**
```bash
# Test non-existent endpoint (should return 404)
curl -i http://localhost:5001/api/nonexistent

# Test with invalid parameters
curl "http://localhost:5001/api/hello?invalid=param"
```

**Scripted Testing:**
```bash
#!/bin/bash
# Simple test script to verify all endpoints

BASE_URL="http://localhost:5001"
echo "Testing Flask API endpoints..."

echo "\n1. Testing root endpoint:"
curl -s $BASE_URL/ | jq

echo "\n2. Testing API hello endpoint:"
curl -s $BASE_URL/api/hello | jq

echo "\n3. Testing personalized greeting:"
curl -s "$BASE_URL/api/hello?name=Tester" | jq

echo "\n4. Testing health endpoint:"
curl -s $BASE_URL/health | jq

echo "\n✓ All tests completed"
```

### Complete API Documentation

For detailed API documentation including:
- Complete request/response examples
- Error handling
- Multiple language examples (curl, Python, JavaScript)
- CORS configuration
- Testing strategies

See **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** for comprehensive documentation.

## Testing

### Run all tests

```bash
pytest
```

### Run tests with coverage

```bash
pytest --cov=. --cov-report=html
```

Coverage report will be generated in `htmlcov/index.html`

### Run tests with verbose output

```bash
pytest -v
```

### Run specific test file

```bash
pytest tests/test_app.py
```

## Project Structure

```
flask-hello-world-api/
├── app.py                   # Main Flask application entry point
├── config.py                # Configuration classes for different environments
├── requirements.txt         # Python dependencies with pinned versions
├── runtime.txt             # Python version specification for deployment
├── Procfile                # Process definition for cloud deployments
├── .env.example            # Example environment variables template
├── .gitignore              # Git ignore patterns for Python projects
├── README.md               # Project documentation
├── API_DOCUMENTATION.md    # Comprehensive API documentation with examples
└── tests/
    ├── conftest.py         # Pytest fixtures and test configuration
    └── test_app.py         # Unit tests for API endpoints
```

## Configuration

The application uses environment-based configuration defined in `config.py`:

- **DevelopmentConfig**: For local development with debug mode enabled
- **ProductionConfig**: For production deployment with debug mode disabled
- **TestingConfig**: For running tests

Configuration is automatically selected based on the `FLASK_ENV` environment variable.

## Deployment

This application can be deployed to various platforms. The repository includes `runtime.txt` and `Procfile` for easy deployment to cloud platforms.

### Heroku

Heroku is a cloud platform that makes it easy to deploy web applications.

#### Prerequisites
- [Heroku account](https://signup.heroku.com/)
- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) installed

#### Deployment Steps

1. **Login to Heroku**:
```bash
heroku login
```

2. **Create a new Heroku app**:
```bash
heroku create your-app-name
```

3. **Set environment variables**:
```bash
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')
```

4. **Deploy the application**:
```bash
git push heroku main
```

5. **Open your deployed app**:
```bash
heroku open
```

6. **View logs** (if needed):
```bash
heroku logs --tail
```

#### Verifying Deployment

```bash
# Check the health endpoint
curl https://your-app-name.herokuapp.com/health

# Test the API
curl https://your-app-name.herokuapp.com/api/hello
```

### Railway

Railway offers a simple deployment experience with automatic builds and deployments.

#### Deployment Steps

1. **Sign up at [Railway](https://railway.app/)**

2. **Install Railway CLI** (optional):
```bash
npm install -g @railway/cli
```

3. **Deploy via CLI**:
```bash
# Login to Railway
railway login

# Initialize project
railway init

# Deploy
railway up
```

4. **Or deploy via GitHub**:
   - Connect your GitHub repository in the Railway dashboard
   - Railway will automatically detect the Procfile and runtime.txt
   - Set environment variables in the dashboard:
     - `FLASK_ENV=production`
     - `SECRET_KEY=<your-secret-key>`
   - Deploy with automatic builds on push

5. **Get your deployment URL**:
```bash
railway open
```

### Render

Render provides automatic deployments from Git with zero-config setup.

#### Deployment Steps

1. **Sign up at [Render](https://render.com/)**

2. **Create a New Web Service**:
   - Click "New +" and select "Web Service"
   - Connect your GitHub/GitLab repository
   - Render will auto-detect your settings

3. **Configure the service**:
   - **Name**: `flask-hello-world-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app` (or leave blank to use Procfile)

4. **Set Environment Variables**:
   - `FLASK_ENV=production`
   - `SECRET_KEY=<generate-a-secure-key>`
   - `PYTHON_VERSION=3.11.0`

5. **Deploy**:
   - Click "Create Web Service"
   - Render will build and deploy automatically

6. **Access your app**:
   - Your app will be available at `https://your-app-name.onrender.com`

### DigitalOcean App Platform

DigitalOcean App Platform offers a platform-as-a-service (PaaS) solution.

#### Deployment Steps

1. **Sign up at [DigitalOcean](https://www.digitalocean.com/)**

2. **Create a new app**:
   - Go to Apps → Create App
   - Connect your GitHub repository
   - DigitalOcean will detect the Python app automatically

3. **Configure the app**:
   - Confirm Python version from `runtime.txt`
   - Build command: `pip install -r requirements.txt`
   - Run command: `gunicorn app:app --bind 0.0.0.0:$PORT`

4. **Set Environment Variables**:
   ```
   FLASK_ENV=production
   SECRET_KEY=<your-secret-key>
   ```

5. **Deploy**:
   - Review and create the app
   - DigitalOcean will build and deploy

### Google Cloud Platform (Cloud Run)

Cloud Run is a fully managed platform for running containerized applications.

#### Prerequisites
- [Google Cloud account](https://cloud.google.com/)
- [gcloud CLI](https://cloud.google.com/sdk/docs/install) installed

#### Deployment Steps

1. **Authenticate with Google Cloud**:
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

2. **Build the container image**:
```bash
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/flask-hello-world-api
```

3. **Deploy to Cloud Run**:
```bash
gcloud run deploy flask-hello-world-api \
  --image gcr.io/YOUR_PROJECT_ID/flask-hello-world-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars FLASK_ENV=production,SECRET_KEY=your-secret-key
```

4. **Get the service URL**:
```bash
gcloud run services describe flask-hello-world-api --region us-central1 --format 'value(status.url)'
```

### AWS Elastic Beanstalk

AWS Elastic Beanstalk simplifies deployment and scaling of web applications.

#### Prerequisites
- [AWS account](https://aws.amazon.com/)
- [EB CLI](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install.html) installed

#### Deployment Steps

1. **Initialize Elastic Beanstalk**:
```bash
eb init -p python-3.11 flask-hello-world-api --region us-east-1
```

2. **Create an environment and deploy**:
```bash
eb create flask-hello-world-env
```

3. **Set environment variables**:
```bash
eb setenv FLASK_ENV=production SECRET_KEY=your-secret-key
```

4. **Open your application**:
```bash
eb open
```

5. **Update deployment**:
```bash
eb deploy
```

### Docker

Docker allows you to containerize your application for consistent deployments across any platform.

#### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) installed

#### Using the Dockerfile

A `Dockerfile` is included in the project root.

**Build the Docker image**:
```bash
docker build -t flask-hello-world-api .
```

**Run the container**:
```bash
docker run -d -p 5000:5000 \
  -e FLASK_ENV=production \
  -e SECRET_KEY=your-secret-key \
  --name flask-api \
  flask-hello-world-api
```

**View logs**:
```bash
docker logs -f flask-api
```

**Stop the container**:
```bash
docker stop flask-api
```

**Remove the container**:
```bash
docker rm flask-api
```

#### Docker Compose

Create a `docker-compose.yml` for easier management:

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=your-secret-key-here
    restart: unless-stopped
```

**Run with Docker Compose**:
```bash
docker-compose up -d
```

**Stop with Docker Compose**:
```bash
docker-compose down
```

#### Pushing to Docker Hub

```bash
# Tag your image
docker tag flask-hello-world-api username/flask-hello-world-api:latest

# Login to Docker Hub
docker login

# Push to Docker Hub
docker push username/flask-hello-world-api:latest
```

### Deployment Checklist

Before deploying to production, ensure:

- [ ] `FLASK_ENV` is set to `production`
- [ ] `FLASK_DEBUG` is set to `False` (or not set)
- [ ] Strong `SECRET_KEY` is configured
- [ ] Environment variables are set securely (not in code)
- [ ] HTTPS is enabled on your platform
- [ ] Health check endpoint (`/health`) is accessible
- [ ] Application logs are monitored
- [ ] Dependencies are up to date
- [ ] Tests are passing (`pytest`)

### Testing Production Deployment

After deployment, verify the application is working:

```bash
# Replace YOUR_DOMAIN with your actual domain
export API_URL="https://YOUR_DOMAIN"

# Test root endpoint
curl $API_URL/

# Test API endpoint
curl $API_URL/api/hello

# Test with parameter
curl "$API_URL/api/hello?name=Production"

# Test health check
curl $API_URL/health
```

### Continuous Deployment

For automatic deployments on git push:

- **Heroku**: Automatic deployments via GitHub integration
- **Railway**: Enable auto-deploy from Git
- **Render**: Automatic deploys on push to main branch
- **GitHub Actions**: Use the following workflow (`.github/workflows/deploy.yml`):

```yaml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to production
        run: |
          # Add your deployment commands here
          # Example: git push heroku main
```

## Environment Variables

The application uses environment variables for configuration. All variables have sensible defaults, so you can run the application without setting any environment variables. However, it's recommended to configure them for production deployments.

### Core Flask Settings

| Variable | Description | Default | Required | Notes |
|----------|-------------|---------|----------|-------|
| `FLASK_ENV` | Environment mode | `development` | No | Options: `development`, `production`, `testing` |
| `SECRET_KEY` | Secret key for session management and security | `dev-secret-key-change-in-production` | **Yes (Production)** | Use a strong random key in production. Generate with: `python -c 'import secrets; print(secrets.token_hex(32))'` |
| `DEBUG` | Enable Flask debug mode | `False` (base), `True` (development) | No | Automatically enabled in development, disabled in production |
| `TESTING` | Enable testing mode | `False` | No | Automatically set to `True` in testing environment |

### Server Configuration

| Variable | Description | Default | Required | Notes |
|----------|-------------|---------|----------|-------|
| `HOST` | Host address to bind to | `0.0.0.0` | No | Use `0.0.0.0` to accept connections from any IP |
| `PORT` | Port number for the application | `5000` (base), `5001` (development) | No | Cloud platforms may override this (e.g., Heroku sets `$PORT`) |

### Application Metadata

| Variable | Description | Default | Required | Notes |
|----------|-------------|---------|----------|-------|
| `APP_NAME` | Application name | `Flask Hello World API` | No | Used for logging and identification |
| `APP_VERSION` | Application version | `1.0.0` | No | Semantic versioning recommended |

### JSON Output Settings

| Variable | Description | Default | Required | Notes |
|----------|-------------|---------|----------|-------|
| `JSONIFY_PRETTYPRINT_REGULAR` | Pretty-print JSON responses | `True` | No | Set to `False` in production for smaller response size |
| `JSON_SORT_KEYS` | Sort JSON keys alphabetically | `False` | No | Set to `True` for consistent key ordering |

### Security Settings

| Variable | Description | Default | Required | Notes |
|----------|-------------|---------|----------|-------|
| `SESSION_COOKIE_SECURE` | Require HTTPS for cookies | `True` (production), `False` (development) | No | **Must be `True` in production with HTTPS** |
| `SESSION_COOKIE_HTTPONLY` | Prevent JavaScript access to cookies | `True` | No | Security best practice, keep enabled |
| `SESSION_COOKIE_SAMESITE` | SameSite cookie policy | `Lax` | No | Options: `Strict`, `Lax`, `None` |

### CORS Configuration

| Variable | Description | Default | Required | Notes |
|----------|-------------|---------|----------|-------|
| `CORS_ENABLED` | Enable Cross-Origin Resource Sharing | `True` | No | Set to `False` if CORS is not needed |
| `CORS_ORIGINS` | Allowed CORS origins | `*` | No | Use `*` for all origins or specify: `https://example.com,https://app.example.com` |

### Logging Configuration

| Variable | Description | Default | Required | Notes |
|----------|-------------|---------|----------|-------|
| `LOG_LEVEL` | Logging level | `INFO` | No | Options: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` |
| `LOG_FORMAT` | Log message format | `%(asctime)s - %(name)s - %(levelname)s - %(message)s` | No | Python logging format string |

### Environment-Specific Defaults

The application provides different defaults based on the environment:

**Development Environment** (`FLASK_ENV=development`):
- `DEBUG=True` (debug mode enabled)
- `PORT=5001` (runs on port 5001)
- `SESSION_COOKIE_SECURE=False` (allows HTTP for local development)

**Production Environment** (`FLASK_ENV=production`):
- `DEBUG=False` (debug mode disabled)
- `TESTING=False` (testing mode disabled)
- `SESSION_COOKIE_SECURE=True` (requires HTTPS)
- **Warning**: Default `SECRET_KEY` will be insecure; you **must** set a strong key

**Testing Environment** (`FLASK_ENV=testing`):
- `TESTING=True` (testing mode enabled)
- `DEBUG=True` (debug mode enabled for better error messages)
- `SESSION_COOKIE_SECURE=False` (allows HTTP for test client)
- Uses test-specific secret key

### Setting Environment Variables

**Using .env file** (recommended for development):

1. Copy the example file:
```bash
cp .env.example .env
```

2. Edit `.env` and customize values:
```bash
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
PORT=5001
DEBUG=True
```

3. The application will automatically load `.env` if you use a package like `python-dotenv`

**Using export commands** (Unix/Linux/macOS):
```bash
export FLASK_ENV=production
export SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')
export PORT=8080
```

**Using set commands** (Windows CMD):
```cmd
set FLASK_ENV=production
set SECRET_KEY=your-secret-key
set PORT=8080
```

**Using environment variable prefixes** (one-time use):
```bash
FLASK_ENV=production SECRET_KEY=my-key python app.py
```

**Using cloud platform interfaces**:
- Heroku: `heroku config:set SECRET_KEY=your-key`
- Railway: Set in Railway dashboard or `railway variables`
- Render: Set in Environment section of web service settings
- AWS: Use Elastic Beanstalk console or `eb setenv`

### Production Environment Variable Example

For production deployments, set these minimum variables:

```bash
FLASK_ENV=production
SECRET_KEY=<generate-a-strong-random-key>
DEBUG=False
SESSION_COOKIE_SECURE=True
CORS_ORIGINS=https://yourdomain.com
LOG_LEVEL=WARNING
```

### Security Best Practices

1. **Never commit `.env` files** - They're in `.gitignore` for a reason
2. **Use strong SECRET_KEY** - Generate with: `python -c 'import secrets; print(secrets.token_hex(32))'`
3. **Enable HTTPS in production** - Set `SESSION_COOKIE_SECURE=True`
4. **Restrict CORS origins** - Don't use `*` in production; specify allowed domains
5. **Disable DEBUG** - Always set `DEBUG=False` in production
6. **Use environment-specific configs** - Leverage `FLASK_ENV` to automatically apply secure defaults

## Security Notes

- Always set a strong `SECRET_KEY` in production
- Never commit `.env` file to version control
- Use HTTPS in production environments
- Keep dependencies up to date with security patches
- Review `config.py` for production security settings

## Development

### Adding New Dependencies

1. Install the package:
```bash
pip install package-name
```

2. Update requirements.txt:
```bash
pip freeze > requirements.txt
```

### Code Style

The project follows PEP 8 style guidelines. Consider using tools like:
- `black` for code formatting
- `flake8` for linting
- `mypy` for type checking

Example:

```bash
pip install black flake8 mypy
black .
flake8 .
mypy .
```

## Troubleshooting

### Port Already in Use

If port 5000 is already in use, specify a different port:

```bash
PORT=8080 python app.py
```

Or with Gunicorn:

```bash
gunicorn --bind 0.0.0.0:8080 app:app
```

### Import Errors

Ensure your virtual environment is activated and all dependencies are installed:

```bash
source venv/bin/activate  # On macOS/Linux
pip install -r requirements.txt
```

### Tests Failing

Make sure you're in the project root directory and the virtual environment is activated:

```bash
cd flask-hello-world-api
source venv/bin/activate
pytest
```

### Module Not Found Errors

If you get `ModuleNotFoundError`, ensure you've installed all dependencies:

```bash
pip install -r requirements.txt
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For issues, questions, or contributions, please open an issue in the GitHub repository.

## Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [pytest Documentation](https://docs.pytest.org/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Heroku Python Support](https://devcenter.heroku.com/articles/python-support)
