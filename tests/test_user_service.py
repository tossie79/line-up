import pytest
import httpx
from unittest.mock import AsyncMock, patch
from app.services.user_service import UserService
from app.core.exceptions import ExternalAPIError, UserNotFoundError


@pytest.mark.asyncio
async def test_user_service_context_manager():
    """Test that UserService properly manages HTTP client"""
    async with UserService() as service:
        assert service.client is not None
        # client should not be closed while inside the context manager
        assert not service.client.is_closed

    # after exiting, the client should be closed
    assert service.client.is_closed


@pytest.mark.asyncio
async def test_get_all_users_invalid_page():
    """Test get_all_users with invalid page parameter"""
    async with UserService() as service:
        with pytest.raises(ExternalAPIError) as exc_info:
            await service.get_all_users(page=0)
        assert "Page number must be greater than 0" in str(exc_info.value)


@pytest.mark.asyncio
async def test_get_user_by_id_invalid_id():
    """Test get_user_by_id with invalid user ID"""
    async with UserService() as service:
        with pytest.raises(ExternalAPIError) as exc_info:
            await service.get_user_by_id(0)
        assert "User ID must be greater than 0" in str(exc_info.value)


@pytest.mark.asyncio
async def test_get_all_users_success():
    """Test successful get_all_users call (mocked _make_request)"""
    mock_response_data = {
        "page": 1,
        "per_page": 6,  
        "total": 12,
        "total_pages": 2,
        "data": [
            {
                "id": 1,
                "email": "george.bluth@reqres.in",
                "first_name": "George",
                "last_name": "Bluth",
                "avatar": "https://reqres.in/img/faces/1-image.jpg",
            }
        ],
    }

    # Mock the _make_request method to avoid real API calls
    with patch.object(
        UserService, "_make_request", new_callable=AsyncMock
    ) as mock_request:
        mock_request.return_value = mock_response_data

        async with UserService() as service:
            result = await service.get_all_users(page=1)

            # Verify the structure and values match the mocked API response
            assert result.page == mock_response_data["page"]
            assert (
                result.per_page == mock_response_data["per_page"]
            ), f"expected per_page {mock_response_data['per_page']}, got {result.per_page}"
            assert result.total == mock_response_data["total"]
            assert len(result.data) == 1


@pytest.mark.asyncio
async def test_get_user_by_id_success():
    """Test successful get_user_by_id call"""
    mock_response_data = {
        "data": {
            "id": 1,
            "email": "george.bluth@reqres.in",
            "first_name": "George",
            "last_name": "Bluth",
            "avatar": "https://reqres.in/img/faces/1-image.jpg",
        }
    }

    with patch.object(
        UserService, "_make_request", new_callable=AsyncMock
    ) as mock_request:
        mock_request.return_value = mock_response_data

        async with UserService() as service:
            result = await service.get_user_by_id(1)

            assert result.id == 1
            assert result.email == "george.bluth@reqres.in"


@pytest.mark.asyncio
async def test_get_user_by_id_not_found():
    """Test get_user_by_id with non-existent user by mocking _make_request to raise domain error"""
    with patch.object(
        UserService, "_make_request", new_callable=AsyncMock
    ) as mock_request:
        # Have the patched _make_request raise the translated domain error
        mock_request.side_effect = UserNotFoundError(999)

        async with UserService() as service:
            with pytest.raises(UserNotFoundError) as exc_info:
                await service.get_user_by_id(999)

            assert "999" in str(exc_info.value)


@pytest.mark.asyncio
async def test__make_request_translates_404_to_user_not_found():
    """
    Test that _make_request translates an httpx.HTTPStatusError for 404 into UserNotFoundError.
    This patches the underlying client.get to return a 404 response with a request attached,
    so response.raise_for_status() will raise HTTPStatusError and _make_request will translate it.
    """
    # Build a 404 Response that has an associated Request (required for raise_for_status to include it)
    fake_request = httpx.Request("GET", "https://example.com/users/999")
    response_404 = httpx.Response(404, request=fake_request)

    async with UserService() as service:
        # patch the instance's client.get so _make_request executes its normal logic
        with patch.object(service.client, "get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = response_404

            # calling _make_request should result in UserNotFoundError for a 404 response
            with pytest.raises(UserNotFoundError):
                await service._make_request("/users/999")
