from typing import Dict
from accessor_client import UsersDBAccessorClient
from dto import UserDTO
from user import User
import uuid
import logging
import json
from datetime import datetime
from http import HTTPStatus

logger = logging.getLogger(__name__)


class UserManagerEngine:
    def __init__(self):
        logger.info("Initializing UserManagerEngine")
        self.db_accessor = UsersDBAccessorClient()

    def create_user(self, user_dto: UserDTO) -> Dict:
        """Creates a user and handles errors like duplicate user ID or email."""
        try:
            logger.info("Processing create_user request")
            if not self._validate_user(user_dto):
                return {
                    "error": "Invalid user data",
                    "status_code": HTTPStatus.BAD_REQUEST,
                }

            while True:  # Retry logic for duplicate user_id
                user = User(
                    user_id=str(uuid.uuid4()),
                    email=user_dto.email,
                    username=user_dto.username,
                    password=user_dto.password,
                    country=user_dto.country,
                    language=user_dto.language,
                    categories=user_dto.categories,
                    created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    updated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    is_active=True,
                    notification_channel=user_dto.notification_channel,
                    telegram_user_id=user_dto.telegram_user_id,
                )
                logger.info(f"Creating user: {user}")
                response = self.db_accessor.create_user(user)

                if response.get("error"):
                    error_message = response["error"]
                    logger.error(f"Error creating user: {error_message}")

                    if "User id already exists" in error_message:
                        logger.info("User ID conflict, generating a new one...")
                        continue  # Generate a new user_id and retry
                    return {
                        "error": error_message,
                        "status_code": HTTPStatus.BAD_REQUEST,
                    }

                logger.info("User created successfully")
                return {"success": True, "status_code": HTTPStatus.CREATED}

        except Exception as e:
            logger.error(f"Unexpected error in create_user: {str(e)}", exc_info=True)
            return {
                "error": "Internal server error",
                "status_code": HTTPStatus.INTERNAL_SERVER_ERROR,
            }

    def get_user_preferences(self, email: str, password: str) -> Dict:
        """Retrieves user preferences and identifies specific errors."""
        try:
            logger.info("Processing get_user_preferences request")
            if not email or not password:
                return {
                    "error": "Email and password are required",
                    "status_code": HTTPStatus.BAD_REQUEST,
                }

            response = self.db_accessor.get_user_preferences(email, password)
            if response.get("error"):
                error_message = response["error"]
                logger.error(f"Error retrieving preferences: {error_message}")

                if "User not found" in error_message:
                    return {
                        "error": "User not found",
                        "status_code": HTTPStatus.NOT_FOUND,
                    }
                if "Invalid password" in error_message:
                    return {
                        "error": "Invalid password",
                        "status_code": HTTPStatus.UNAUTHORIZED,
                    }

                return {"error": error_message, "status_code": HTTPStatus.BAD_REQUEST}

            logger.info("Preferences retrieved successfully")
            return {
                "success": True,
                "preferences": response,
                "status_code": HTTPStatus.OK,
            }

        except Exception as e:
            logger.error(
                f"Unexpected error in get_user_preferences: {str(e)}", exc_info=True
            )
            return {
                "error": "Internal server error",
                "status_code": HTTPStatus.INTERNAL_SERVER_ERROR,
            }

    def update_user_by_email(
        self, user_dto: UserDTO, old_email: str, old_password: str
    ) -> Dict:
        """Updates a user by email with error handling."""
        try:
            logger.info("Processing update_user_by_email request")
            if not self._validate_user(user_dto):
                return {
                    "error": "Invalid user data",
                    "status_code": HTTPStatus.BAD_REQUEST,
                }

            new_user = User(
                user_id="",
                email=user_dto.email,
                username=user_dto.username,
                password=user_dto.password,
                country=user_dto.country,
                language=user_dto.language,
                categories=user_dto.categories,
                created_at="",
                updated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                is_active=True,
                notification_channel=user_dto.notification_channel,
                telegram_user_id=user_dto.telegram_user_id,
            )
            response = self.db_accessor.update_user_by_email(
                new_user, old_email, old_password
            )

            if response.get("error"):
                error_message = response["error"]
                logger.error(f"Error updating user: {error_message}")

                if "User not found" in error_message:
                    return {
                        "error": "User not found",
                        "status_code": HTTPStatus.NOT_FOUND,
                    }
                if "Invalid password" in error_message:
                    return {
                        "error": "Invalid password",
                        "status_code": HTTPStatus.UNAUTHORIZED,
                    }

                return {"error": error_message, "status_code": HTTPStatus.BAD_REQUEST}

            logger.info("User updated successfully")
            return {"success": True, "status_code": HTTPStatus.OK}

        except Exception as e:
            logger.error(
                f"Unexpected error in update_user_by_email: {str(e)}", exc_info=True
            )
            return {
                "error": "Internal server error",
                "status_code": HTTPStatus.INTERNAL_SERVER_ERROR,
            }

    def delete_user_by_email(self, email: str, password: str) -> Dict:
        """Deletes a user by email with error handling."""
        try:
            logger.info("Processing delete_user_by_email request")
            if not email or not password:
                return {
                    "error": "Email and password are required",
                    "status_code": HTTPStatus.BAD_REQUEST,
                }

            response = self.db_accessor.delete_user_by_email(email, password)
            if response.get("error"):
                error_message = response["error"]
                logger.error(f"Error deleting user: {error_message}")

                if "User not found" in error_message:
                    return {
                        "error": "User not found",
                        "status_code": HTTPStatus.NOT_FOUND,
                    }
                if "Invalid password" in error_message:
                    return {
                        "error": "Invalid password",
                        "status_code": HTTPStatus.UNAUTHORIZED,
                    }

                return {"error": error_message, "status_code": HTTPStatus.BAD_REQUEST}

            logger.info("User deleted successfully")
            return {"success": True, "status_code": HTTPStatus.OK}

        except Exception as e:
            logger.error(
                f"Unexpected error in delete_user_by_email: {str(e)}", exc_info=True
            )
            return {
                "error": "Internal server error",
                "status_code": HTTPStatus.INTERNAL_SERVER_ERROR,
            }

    @staticmethod
    def _validate_user(user: UserDTO) -> bool:
        return bool(user.email and user.password and user.username)
