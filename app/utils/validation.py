from typing import Dict, Any, List
from app.core.exceptions import ExternalAPIError, DataValidationError
from app.models.user import User

class DataValidator:
    """Utility class for data validation operations"""
    
    @staticmethod
    def validate_user_data(user_data: Dict[str, Any]) -> User:
        """
        Validate and create User object from raw data
        
        Args:
            user_data: Raw user data from external API
            
        Returns:
            User: Validated User object
            
        Raises:
            ExternalAPIError: If user data is invalid
        """
        try:
            return User(**user_data)
        except Exception as e:
            # Log the invalid data for debugging
            print(f" Invalid user data: {user_data}, error: {e}")
            raise ExternalAPIError(f"Invalid user data received from external API: {str(e)}")
    
    @staticmethod
    def validate_user_list_response(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate user list API response structure
        
        Args:
            data: Raw response from external API
            
        Returns:
            Dict: Validated data
            
        Raises:
            ExternalAPIError: If response structure is invalid
        """
        try:
            # Check if required fields exist
            required_fields = ["page", "per_page", "total", "total_pages", "data"]
            for field in required_fields:
                if field not in data:
                    raise ExternalAPIError(f"Missing required field '{field}' in API response")
            
            # Validate data types
            if not isinstance(data["data"], list):
                raise ExternalAPIError("Invalid data format: 'data' should be a list")
            
            # Validate pagination fields are integers
            pagination_fields = ["page", "per_page", "total", "total_pages"]
            for field in pagination_fields:
                if not isinstance(data[field], int):
                    raise ExternalAPIError(f"Invalid data type for '{field}': expected integer")
            
            return data
            
        except ExternalAPIError:
            # Re-raise our custom errors
            raise
        except Exception as e:
            # Catch any unexpected errors during validation
            raise ExternalAPIError(f"Failed to validate API response: {str(e)}")
    
    @staticmethod
    def validate_page_parameter(page: int) -> None:
        """
        Validate page parameter
        
        Args:
            page: Page number to validate
            
        Raises:
            ExternalAPIError: If page is invalid
        """
        if page < 1:
            raise ExternalAPIError("Page number must be greater than 0")
    
    @staticmethod
    def validate_user_id(user_id: int) -> None:
        """
        Validate user ID parameter
        
        Args:
            user_id: User ID to validate
            
        Raises:
            ExternalAPIError: If user ID is invalid
        """
        if user_id < 1:
            raise ExternalAPIError("User ID must be greater than 0")