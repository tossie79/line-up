import pytest
from pydantic import ValidationError
from app.models.user import User, UserList


def test_user_model_valid():
    """Test User model with valid data"""
    user_data = {
        "id": 1,
        "email": "test@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "avatar": "https://example.com/avatar.jpg",
    }

    user = User(**user_data)

    assert user.id == 1
    assert user.email == "test@example.com"
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.avatar == "https://example.com/avatar.jpg"


def test_user_model_invalid():
    """Test User model with invalid data"""
    invalid_data = {
        "id": "not_an_int",  # Should be int
        "email": "not_an_email",  # Invalid email format
        "first_name": 123,  # Should be string
    }

    with pytest.raises(ValidationError):
        User(**invalid_data)


def test_user_model_missing_required():
    """Test User model with missing required fields"""
    incomplete_data = {
        "id": 1,
        "email": "test@example.com",
        # Missing first_name and last_name
    }

    with pytest.raises(ValidationError):
        User(**incomplete_data)


def test_user_list_model():
    """Test UserList model"""
    user_list_data = {
        "page": 1,
        "per_page": 6,
        "total": 12,
        "total_pages": 2,
        "data": [
            {
                "id": 1,
                "email": "test1@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "avatar": "https://example.com/avatar1.jpg",
            },
            {
                "id": 2,
                "email": "test2@example.com",
                "first_name": "Jane",
                "last_name": "Smith",
                "avatar": "https://example.com/avatar2.jpg",
            },
        ],
    }

    user_list = UserList(**user_list_data)

    assert user_list.page == 1
    assert user_list.per_page == 6
    assert user_list.total == 12
    assert user_list.total_pages == 2
    assert len(user_list.data) == 2
    assert user_list.data[0].email == "test1@example.com"
