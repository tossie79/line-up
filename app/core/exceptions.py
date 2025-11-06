from fastapi import HTTPException
from typing import Any, Dict, Optional


class UserAPIException(HTTPException):
    """Base exception for User API errors"""

    def __init__(
        self, status_code: int, detail: str, headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class ExternalAPIError(UserAPIException):
    """Raised when the external API fails"""

    def __init__(self, detail: str = "External service unavailable"):
        super().__init__(status_code=503, detail=detail)


class UserNotFoundError(UserAPIException):
    """Raised when a user is not found"""

    def __init__(self, user_id: int):
        super().__init__(status_code=404, detail=f"User with id {user_id} not found")


class AuthenticationError(UserAPIException):
    """Raised when API key authentication fails"""

    def __init__(self, detail: str = "API key authentication failed"):
        super().__init__(status_code=401, detail=detail)


class RateLimitError(UserAPIException):
    """Raised when rate limit is exceeded"""

    def __init__(self, detail: str = "Rate limit exceeded"):
        super().__init__(status_code=429, detail=detail)


class APIKeyError(UserAPIException):
    """Raised when there are API key configuration issues"""

    def __init__(self, detail: str = "API key configuration error"):
        super().__init__(status_code=500, detail=detail)
