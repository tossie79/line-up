from fastapi.testclient import TestClient
from app.main import app
from app.models.user import User, UserList
from app.core.exceptions import UserNotFoundError, ExternalAPIError
from app.core.dependencies import get_user_service

client = TestClient(app)


# ---------------- Generic async mock ----------------
class MockUserService:
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
            raise ExternalAPIError("Service unavailable")
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
            raise ExternalAPIError("Service unavailable")
        if self.raise_user_not_found:
            raise UserNotFoundError(user_id)
        return User(
            id=user_id,
            email="george.bluth@reqres.in",
            first_name="George",
            last_name="Bluth",
            avatar="https://reqres.in/img/faces/1-image.jpg",
        )


# ---------------- Helper to override ----------------
def override_user_service(mock_service):
    app.dependency_overrides[get_user_service] = lambda: mock_service


# ---------------- Tests ----------------
def test_get_all_users_success():
    mock = MockUserService()
    override_user_service(mock)
    response = client.get("/api/v1/user/")
    data = response.json()
    assert response.status_code == 200
    assert data["per_page"] == 6
    assert data["page"] == 1
    assert data["total"] == 12
    assert data["data"][0]["email"] == "george.bluth@reqres.in"
    app.dependency_overrides.clear()


def test_get_all_users_pagination():
    mock = MockUserService()
    override_user_service(mock)
    response = client.get("/api/v1/user/?page=2")
    data = response.json()
    assert response.status_code == 200
    assert data["page"] == 2
    assert data["per_page"] == 6
    app.dependency_overrides.clear()


def test_get_user_by_id_success():
    mock = MockUserService()
    override_user_service(mock)
    response = client.get("/api/v1/user/1")
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == 1
    assert data["email"] == "george.bluth@reqres.in"
    app.dependency_overrides.clear()


def test_get_user_by_id_not_found():
    mock = MockUserService(raise_user_not_found=True)
    override_user_service(mock)
    response = client.get("/api/v1/user/999")
    data = response.json()
    assert response.status_code == 404
    assert "999" in data["detail"]
    app.dependency_overrides.clear()


def test_external_api_error():
    mock = MockUserService(raise_api_error=True)
    override_user_service(mock)
    response = client.get("/api/v1/user/")
    # Depends on how ExternalAPIError is mapped in HTTPException
    assert response.status_code in (500, 503)
    app.dependency_overrides.clear()
