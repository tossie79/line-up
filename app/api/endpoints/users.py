from fastapi import APIRouter, Depends, Query, HTTPException
from app.core.dependencies import get_user_service
from app.services.user_service import UserService
from app.models.user import User, UserList
from app.core.exceptions import UserNotFoundError, ExternalAPIError

router = APIRouter()

@router.get(
    "/user/",
    response_model=UserList,
    summary="Get all users",
    description="Retrieve a paginated list of users from the external API"
)
async def get_all_users(
    page: int = Query(1, ge=1, description="Page number"),
    user_service: UserService = Depends(get_user_service) 
) -> UserList:
    """
    Get a paginated list of users.
    
    - **page**: Page number (default: 1, minimum: 1)
    - **returns**: UserList object with pagination info and user data
    """
    try:
        return await user_service.get_all_users(page=page)
    except ExternalAPIError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get(
    "/user/{user_id}",
    response_model=User,
    summary="Get user by ID",
    description="Retrieve a specific user by their ID"
)
async def get_user_by_id(
    user_id: int,
    user_service: UserService = Depends(get_user_service)  
) -> User:
    """
    Get a specific user by ID.
    
    - **user_id**: The ID of the user to retrieve
    - **returns**: User object with details
    """
    try:
        return await user_service.get_user_by_id(user_id)
    except UserNotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except ExternalAPIError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)