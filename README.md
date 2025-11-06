# Line-Up User API #
A FastAPI-based REST API that provides user data by integrating with the reqres.in mock API

## Features ##

 - FastAPI - Modern, fast web framework with automatic API documentation
 - Async/Await - Full asynchronous support for better performance
 - Dependency Injection - Clean separation of concerns with proper resource management
 - Comprehensive Error Handling - Graceful error handling and meaningful error messages
 - Type Safety - Full type hints with Pydantic validation
 - Testing - Comprehensive test suite with both unit and integration tests
 - Docker Support - Containerized deployment ready for production
 - API Documentation - Automatic OpenAPI documentation at /docs

 ##  API Endpoints ##

 ```
 
Method	   Endpoint	            Description
GET	       /	                Root endpoint with API information
GET	       /health	            Health check endpoint
GET	       /api/v1/user/	    Get paginated list of users
GET	       /api/v1/user/{id}	Get user by ID

 ```
 ### Example Requests ###
 ```bash
# Get all users (page 1)
curl http://localhost:8000/api/v1/user/

# Get users page 2
curl "http://localhost:8000/api/v1/user/?page=2"

# Get user by ID
curl http://localhost:8000/api/v1/user/1

# Health check
curl http://localhost:8000/health
 ```
 ##  Installation & Setup ##

 ### Prerequisites ###
 - Python 3.11+
 - Docker 

 ### Method 1: Using Docker (Recommended) ###

 ```bash
# Clone the repository
git clone <repository-url>
cd lineup-user-api

# Build and run with Docker Compose
docker-compose up --build

# The API will be available at http://localhost:8000

 ```

  ### Method 2: Local Development ###

  ```bash
# Clone the repository
git clone <repository-url>
cd lineup-user-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
  ```

## Project Structure ##
```bash
lineup-user-api/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── core/
│   │   ├── config.py          # Application configuration
│   │   ├── dependencies.py    # Dependency injection
│   │   └── exceptions.py      # Custom exceptions
│   ├── api/
│   │   └── endpoints/
│   │       └── users.py       # User API endpoints
│   ├── services/
│   │   └── user_service.py    # Business logic and external API integration
│   ├── models/
│   │   └── user.py            # Pydantic models
├── tests/
│   ├── conftest.py            # pytest configuration and fixtures
│   ├── test_models.py         # Model tests
│   ├── test_user_service.py   # Service layer tests
│   ├── test_api_endpoints.py  # API endpoint tests
│   └── test_integration.py    # Integration tests
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
```

## Testing ##
### Running Tests ###

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run only unit tests (fast)
pytest -m "not integration"

# Run only integration tests
pytest -m integration

# Run specific test file
pytest tests/test_user_service.py -v

```

### Test Structure ###
 - Unit Tests: Mock external dependencies for fast, isolated testing
 - Integration Tests: Test with real external API (marked with @pytest.mark.integration)
 - API Tests: Test HTTP endpoints with FastAPI TestClient


 ## Configuration ##
  - Environment variables are configured in `.env.example`
  - Copy `.env.example` to `.env`:
 ```bash
    cp .env.example .env

```

## API Documentation ##
Once running, access the interactive API documentation:
 - Swagger UI: http://localhost:8000/docs
 - ReDoc: http://localhost:8000/redoc

 ## Code Quality ##
 ### Type Checking ###

```bash
mypy app/
```

  ### Code Formatting ###

  ```bash
black app/ tests/
```

## Docker ##
### Build Image ###

```bash
docker build -t lineup-user-api .

```

### Run Container ###

```bash
docker run -p 8000:8000 --env-file .env lineup-user-api

```


### Development with Docker Compose ###

```bash
docker-compose up --build
docker-compose down  # Stop containers

```


## Design Decisions ## 
### Architecture ### 
 - FastAPI for its performance, automatic docs, and type safety
 - Async/Await throughout for better I/O performance
 - Dependency Injection for testability and clean separation
 - Pydantic for data validation and serialization

### Error Handling ### 
 - Custom exception hierarchy for different error scenarios
 - Proper HTTP status codes and meaningful error messages
 - Graceful handling of external API failures

### Testing ###
 - Comprehensive test coverage with pytest
 - Mock external dependencies for reliable unit tests
 - Configurable mock services for different test scenarios
 - Both sync and async test clients

## API Response Examples ##

### Get All Users ###

```bash
/api/v1/user
{
  "page": 1,
  "per_page": 6,
  "total": 12,
  "total_pages": 2,
  "data": [
   {
      "email": "george.bluth@reqres.in",
      "first_name": "George",
      "last_name": "Bluth",
      "avatar": "https://reqres.in/img/faces/1-image.jpg",
      "id": 1
    },
    {
      "email": "janet.weaver@reqres.in",
      "first_name": "Janet",
      "last_name": "Weaver",
      "avatar": "https://reqres.in/img/faces/2-image.jpg",
      "id": 2
    },
  ]
}
```

### Get User by ID ###

```bash
/api/v1/user/11
{
  "email": "george.edwards@reqres.in",
  "first_name": "George",
  "last_name": "Edwards",
  "avatar": "https://reqres.in/img/faces/11-image.jpg",
  "id": 11
}
```

### Error Response ###

```bash
/api/v1/user/999
{
  "detail": "User with id 999 not found"
}
```