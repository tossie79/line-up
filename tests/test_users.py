import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Line-Up User API" in data["message"]


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_get_all_users():
    """Test getting all users"""
    response = client.get("/api/v1/user/")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "page" in data
    assert "total" in data


def test_get_user_by_id():
    """Test getting user by ID"""
    response = client.get("/api/v1/user/1")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "email" in data
    assert "first_name" in data
    assert "last_name" in data


def test_get_nonexistent_user():
    """Test getting a user that doesn't exist"""
    response = client.get("/api/v1/user/9999")
    assert response.status_code == 404
