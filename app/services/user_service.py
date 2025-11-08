import httpx
from typing import Optional, List
from app.core.config import settings
from app.core.exceptions import ExternalAPIError, UserNotFoundError
from app.models.user import User, UserList
from app.core.logger import logger


class UserService:
    """Service layer for user operations"""

    def __init__(self):
        self.base_url = settings.REQRES_BASE_URL
        self.api_key = settings.REQRES_API_KEY
        self.client = httpx.AsyncClient(timeout=30.0)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    def _build_headers(self) -> dict:
        """Build headers with API key in the designated header"""
        headers = {
            "Content-Type": "application/json",
            "User-Agent": f"{settings.PROJECT_NAME}/{settings.PROJECT_VERSION}",
        }

        # Add API key header
        if self.api_key:
            headers[settings.API_KEY_HEADER] = self.api_key

        return headers

    async def _make_request(self, endpoint: str) -> dict:
        """
        Make HTTP request to external API with headers including API key
        """
        url = f"{self.base_url}{endpoint}"
        headers = self._build_headers()

        try:
            logger.info(f"Making request to {url}")

            response = await self.client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                logger.error("Invalid API key - unauthorized")
                raise ExternalAPIError("Invalid API key - unauthorized")
            elif e.response.status_code == 403:
                logger.error("API key missing or insufficient permissions")
                raise ExternalAPIError("API key missing or insufficient permissions")
            elif e.response.status_code == 404:
                user_id = endpoint.split("/")[-1]
                if user_id.isdigit():
                    logger.warning(f"User not found: {user_id}")
                    raise UserNotFoundError(int(user_id))
                logger.error("Resource not found")
                raise ExternalAPIError("Resource not found")
            elif e.response.status_code == 429:
                logger.error("Rate limit exceeded")
                raise ExternalAPIError("Rate limit exceeded")
            else:
                logger.error(f"External API returned {e.response.status_code}")
                raise ExternalAPIError(
                    f"External API returned {e.response.status_code}"
                )
        except httpx.RequestError as e:
            logger.error(f"Request failed: {str(e)}")
            raise ExternalAPIError(f"Request failed: {str(e)}")

    async def get_all_users(self, page: int = 1) -> UserList:
        """
        Get paginated list of users
        """
        try:
            if page < 1:
                raise ExternalAPIError("Page number must be greater than 0")

            endpoint = f"/users?page={page}"
            data = await self._make_request(endpoint)

            if "data" not in data:
                raise ExternalAPIError("Invalid response structure from external API")

            # Process users with individual error handling
            users: List[User] = []
            for user_data in data["data"]:
                try:
                    users.append(User(**user_data))
                except Exception as e:
                    logger.warning(f"Skipping invalid user data: {e}")
                    continue  # Skip invalid users but continue processing

            logger.info(f"Retrieved {len(users)} users from page {page}")
            return UserList(
                page=data.get("page", page),
                per_page=data.get("per_page", 0),
                total=data.get("total", 0),
                total_pages=data.get("total_pages", 0),
                data=users,
            )

        except ExternalAPIError as e:
            logger.error(f"Error fetching users for page {page}: {e}")
            raise

    async def get_user_by_id(self, user_id: int) -> User:
        """
        Get user by ID
        """
        try:
            if user_id < 1:
                raise ExternalAPIError("User ID must be greater than 0")

            endpoint = f"/users/{user_id}"
            data = await self._make_request(endpoint)

            if "data" not in data:
                logger.warning(f"User not found: {user_id}")
                raise UserNotFoundError(user_id)

            logger.info(f"Retrieved user {user_id}")
            return User(**data["data"])

        except UserNotFoundError:
            logger.warning(f"User not found: {user_id}")
            raise
        except ExternalAPIError as e:
            logger.error(f"Error fetching user {user_id}: {e}")
            raise
