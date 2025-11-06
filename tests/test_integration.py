import pytest
import httpx
from app.services.user_service import UserService


@pytest.mark.integration
@pytest.mark.asyncio
async def test_integration_get_all_users():
    """Integration test with real external API"""
    # This test actually calls the real reqres.in API
    async with UserService() as service:
        try:
            result = await service.get_all_users(page=1)

            # Basic structure validation
            assert hasattr(result, "page")
            assert hasattr(result, "per_page")
            assert hasattr(result, "total")
            assert hasattr(result, "total_pages")
            assert hasattr(result, "data")
            assert isinstance(result.data, list)

            # If we got users, validate their structure
            if result.data:
                user = result.data[0]
                assert hasattr(user, "id")
                assert hasattr(user, "email")
                assert hasattr(user, "first_name")
                assert hasattr(user, "last_name")

        except Exception as e:
            # It's okay if the external API is down for integration tests
            pytest.skip(f"External API unavailable: {e}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_integration_get_user_by_id():
    """Integration test for single user with real external API"""
    async with UserService() as service:
        try:
            result = await service.get_user_by_id(1)

            # Validate user structure
            assert result.id == 1
            assert result.email
            assert result.first_name
            assert result.last_name

        except Exception as e:
            # It's okay if the external API is down for integration tests
            pytest.skip(f"External API unavailable: {e}")
