from typing import AsyncGenerator
from app.services.user_service import UserService

async def get_user_service() -> AsyncGenerator[UserService, None]:
    """
    Dependency injection for UserService.
    
    Provides an async context manager that automatically handles
    resource cleanup (HTTP client connection pooling).
    
    Yields:
        UserService: Initialized UserService instance
    """
    async with UserService() as service:
        yield service

