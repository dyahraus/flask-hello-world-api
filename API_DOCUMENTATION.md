# API Documentation

## Base URL

```
http://localhost:5001
```

For production deployments, replace with your deployed URL.

## API Endpoints

### 1. Root Hello World

Returns a simple hello world message.

**Endpoint:** `GET /`

**Query Parameters:** None

**Request Headers:** None required

**Example Request:**

```bash
curl -X GET http://localhost:5001/
```

**Example Request (with headers):**

```bash
curl -X GET http://localhost:5001/ \
  -H "Accept: application/json"
```

**Success Response:**

**Code:** `200 OK`

```json
{
  "message": "Hello, World!",
  "status": "success"
}
```

**Response Headers:**

```
Content-Type: application/json
Access-Control-Allow-Origin: * (if CORS enabled)
```

---

### 2. API Hello with Optional Name

Returns a personalized greeting or default hello world message.

**Endpoint:** `GET /api/hello`

**Query Parameters:**

| Parameter | Type   | Required | Description                      |
|-----------|--------|----------|----------------------------------|
| name      | string | No       | Name to personalize the greeting |

**Request Headers:** None required

**Example Request (without name):**

```bash
curl -X GET http://localhost:5001/api/hello
```

**Success Response (without name):**

**Code:** `200 OK`

```json
{
  "message": "Hello, World!",
  "status": "success"
}
```

**Example Request (with name):**

```bash
curl -X GET "http://localhost:5001/api/hello?name=Alice"
```

**Success Response (with name):**

**Code:** `200 OK`

```json
{
  "message": "Hello, Alice!",
  "status": "success"
}
```

**Example Request (URL encoded special characters):**

```bash
curl -X GET "http://localhost:5001/api/hello?name=John%20Doe"
```

**Success Response:**

**Code:** `200 OK`

```json
{
  "message": "Hello, John Doe!",
  "status": "success"
}
```

**JavaScript/Fetch Example:**

```javascript
// Without name parameter
fetch('http://localhost:5001/api/hello')
  .then(response => response.json())
  .then(data => console.log(data));

// With name parameter
fetch('http://localhost:5001/api/hello?name=Alice')
  .then(response => response.json())
  .then(data => console.log(data));
```

**Python/Requests Example:**

```python
import requests

# Without name parameter
response = requests.get('http://localhost:5001/api/hello')
print(response.json())

# With name parameter
response = requests.get('http://localhost:5001/api/hello', params={'name': 'Alice'})
print(response.json())
```

---

### 3. Health Check

Returns the health status of the application with a UTC timestamp. Used for monitoring and deployment verification.

**Endpoint:** `GET /health`

**Query Parameters:** None

**Request Headers:** None required

**Example Request:**

```bash
curl -X GET http://localhost:5001/health
```

**Example Request (with verbose output):**

```bash
curl -X GET http://localhost:5001/health -v
```

**Success Response:**

**Code:** `200 OK`

```json
{
  "status": "healthy",
  "timestamp": "2025-10-07T18:34:56.789012+00:00"
}
```

**Response Fields:**

| Field     | Type   | Description                                    |
|-----------|--------|------------------------------------------------|
| status    | string | Health status, always "healthy" when responding |
| timestamp | string | ISO 8601 formatted UTC timestamp              |

**JavaScript/Fetch Example:**

```javascript
fetch('http://localhost:5001/health')
  .then(response => response.json())
  .then(data => {
    console.log('Status:', data.status);
    console.log('Timestamp:', data.timestamp);
  });
```

**Python/Requests Example:**

```python
import requests
from datetime import datetime

response = requests.get('http://localhost:5001/health')
data = response.json()

print(f"Status: {data['status']}")
print(f"Timestamp: {data['timestamp']}")

# Parse timestamp
timestamp = datetime.fromisoformat(data['timestamp'])
print(f"Parsed time: {timestamp}")
```

**Use Cases:**

- Kubernetes liveness/readiness probes
- Load balancer health checks
- Monitoring system integration
- Deployment verification

---

## Error Responses

### 404 Not Found

Returned when requesting a non-existent endpoint.

**Example Request:**

```bash
curl -X GET http://localhost:5001/nonexistent
```

**Error Response:**

**Code:** `404 Not Found`

```json
{
  "error": "Not Found",
  "message": "The requested resource was not found"
}
```

---

### 500 Internal Server Error

Returned when an unexpected server error occurs.

**Error Response:**

**Code:** `500 Internal Server Error`

```json
{
  "error": "Internal Server Error",
  "message": "An unexpected error occurred"
}
```

---

## Response Format

All responses are returned in JSON format with the following characteristics:

- **Content-Type:** `application/json`
- **Character Encoding:** UTF-8
- **Status Codes:** HTTP standard status codes (200, 404, 500, etc.)

---

## CORS (Cross-Origin Resource Sharing)

CORS is enabled by default for all endpoints. Configuration can be adjusted via environment variables:

- **CORS_ENABLED:** Enable/disable CORS (default: `true`)
- **CORS_ORIGINS:** Comma-separated list of allowed origins (default: `*`)

**Example CORS Headers:**

```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: Content-Type
```

---

## Rate Limiting

Currently, no rate limiting is implemented. For production use, consider implementing rate limiting using:

- Flask-Limiter
- Nginx rate limiting
- API Gateway rate limiting (if using cloud platforms)

---

## Authentication

Currently, no authentication is required for any endpoints. This is a simple hello world API intended for demonstration purposes.

For production applications requiring authentication, consider implementing:

- JWT (JSON Web Tokens)
- OAuth 2.0
- API Keys
- Basic Authentication

---

## Testing the API

### Using cURL

```bash
# Test root endpoint
curl http://localhost:5001/

# Test API hello endpoint
curl http://localhost:5001/api/hello

# Test with name parameter
curl "http://localhost:5001/api/hello?name=Developer"

# Test health check
curl http://localhost:5001/health

# Test 404 error
curl http://localhost:5001/notfound
```

### Using HTTPie

```bash
# Test root endpoint
http GET http://localhost:5001/

# Test API hello endpoint
http GET http://localhost:5001/api/hello

# Test with name parameter
http GET http://localhost:5001/api/hello name==Developer

# Test health check
http GET http://localhost:5001/health
```

### Using Postman

1. Import the following collection or create requests manually:
   - **GET** `http://localhost:5001/`
   - **GET** `http://localhost:5001/api/hello`
   - **GET** `http://localhost:5001/api/hello?name=YourName`
   - **GET** `http://localhost:5001/health`

2. Verify the response status codes and JSON structure

### Using Python

```python
import requests

base_url = 'http://localhost:5001'

# Test all endpoints
endpoints = [
    '/',
    '/api/hello',
    '/api/hello?name=Python',
    '/health'
]

for endpoint in endpoints:
    response = requests.get(f'{base_url}{endpoint}')
    print(f'\nEndpoint: {endpoint}')
    print(f'Status: {response.status_code}')
    print(f'Response: {response.json()}')
```

---

## OpenAPI/Swagger Specification

For API documentation with interactive UI, consider implementing OpenAPI (Swagger) specification using:

- Flask-RESTX
- Flasgger
- flask-swagger-ui

Example OpenAPI specification snippet:

```yaml
openapi: 3.0.0
info:
  title: Flask Hello World API
  version: 1.0.0
  description: A simple Flask API that returns hello world messages
paths:
  /:
    get:
      summary: Root hello world endpoint
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                  status:
                    type: string
  /api/hello:
    get:
      summary: API hello with optional name parameter
      parameters:
        - name: name
          in: query
          schema:
            type: string
          required: false
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                  status:
                    type: string
  /health:
    get:
      summary: Health check endpoint
      responses:
        '200':
          description: Healthy status
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                  timestamp:
                    type: string
                    format: date-time
```

---

## Performance Considerations

- All endpoints are lightweight and respond quickly
- No database queries or external API calls
- Suitable for high-traffic scenarios with proper deployment configuration
- Consider using Gunicorn with multiple workers for production

**Recommended Gunicorn Configuration:**

```bash
gunicorn --bind 0.0.0.0:5001 --workers 4 --threads 2 app:app
```

---

## Versioning

Currently, the API is unversioned. For future development, consider implementing API versioning:

- URL path versioning: `/v1/api/hello`, `/v2/api/hello`
- Header versioning: `Accept: application/vnd.api.v1+json`
- Query parameter versioning: `/api/hello?version=1`

---

## Support and Issues

For questions, issues, or feature requests, please refer to the project repository or contact the development team.
