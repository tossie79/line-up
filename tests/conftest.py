import pytest
import asyncio
from typing import AsyncGenerator
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.main import app
from app.core.config import settings
from app.services.user_service import UserService


# ---------------- Event loop fixture ----------------
@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# ---------------- FastAPI Test Clients ----------------
@pytest.fixture
def test_client() -> TestClient:
    """Synchronous test client for FastAPI."""
    return TestClient(app)


@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """Async test client for FastAPI."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


# ---------------- Custom Marks ----------------
def pytest_configure(config):
    """Register custom pytest marks."""
    config.addinivalue_line(
        "markers", "integration: mark a test as an integration test"
    )


# ---------------- UserService Fixtures ----------------
class MockUserService:
    """Mocked UserService for unit tests."""

    def __init__(
        self,
        users_per_page=6,
        total_users=12,
        raise_user_not_found=False,
        raise_api_error=False,
    ):
        self.users_per_page = users_per_page
        self.total_users = total_users
        self.raise_user_not_found = raise_user_not_found
        self.raise_api_error = raise_api_error

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def get_all_users(self, page=1):
        if self.raise_api_error:
            from app.core.exceptions import ExternalAPIError

            raise ExternalAPIError("Service unavailable")
        from app.models.user import User, UserList

        data = [
            User(
                id=1,
                email="george.bluth@reqres.in",
                first_name="George",
                last_name="Bluth",
                avatar="https://reqres.in/img/faces/1-image.jpg",
            )
        ]
        return UserList(
            page=page,
            per_page=self.users_per_page,
            total=self.total_users,
            total_pages=(self.total_users + self.users_per_page - 1)
            // self.users_per_page,
            data=data,
        )

    async def get_user_by_id(self, user_id):
        if self.raise_api_error:
            from app.core.exceptions import ExternalAPIError

            raise ExternalAPIError("Service unavailable")
        if self.raise_user_not_found:
            from app.core.exceptions import UserNotFoundError

            raise UserNotFoundError(user_id)
        from app.models.user import User

        return User(
            id=user_id,
            email="george.bluth@reqres.in",
            first_name="George",
            last_name="Bluth",
            avatar="https://reqres.in/img/faces/1-image.jpg",
        )


@pytest.fixture
def mock_user_service() -> MockUserService:
    """Fixture providing a mocked UserService for unit tests."""
    return MockUserService()


@pytest.fixture
def real_user_service() -> UserService:
    """Fixture providing the real UserService for integration tests."""
    return UserService()
