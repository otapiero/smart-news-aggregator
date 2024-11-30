from typing import Dict
import logging
import requests
import config
from user import User
import json

logger = logging.getLogger(__name__)


class UsersDBAccessorClient:
    def __init__(self):
        self.address = f"http://localhost:{config.DAPR_HTTP_PORT}/v1.0/invoke/{config.DB_ACCESSOR_APP_ID}/method"

    def create_user(self, user: User) -> Dict:
        """Send a POST request to create a user."""
        try:
            logger.info(f"Creating user: {user}")
            response = requests.post(f"{self.address}/CreateUser", json=user.to_dict())
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error creating user: {e}")
            return {"error": str(e)}

    def get_user_preferences(self, email: str, password: str) -> Dict:
        """Send a GET request to retrieve user preferences."""
        try:
            logger.info(f"Getting preferences for user: {email}")
            params = {"email": email, "password": password}
            response = requests.get(
                f"{self.address}/GetUserPreferencesByEmailAddress", params=params
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error getting user preferences: {e}")
            return {"error": str(e)}

    def update_user(self, user: User) -> Dict:
        """Send a PUT request to update a user by ID."""
        try:
            logger.info(f"Updating user: {user}")
            response = requests.put(f"{self.address}/UpdateUser", json=user.to_dict())
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error updating user: {e}")
            return {"error": str(e)}

    def update_user_by_email(self, user: User, email: str, password: str) -> Dict:
        """Send a PUT request to update a user by email."""
        try:
            logger.info(f"Updating user by email: {email}")
            data = {
                "user": user.to_dict(),
                "email": email,
                "password": password,
            }
            response = requests.put(f"{self.address}/UpdateUserByEmail", json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error updating user by email: {e}")
            return {"error": str(e)}

    def delete_user(self, user_id: str) -> Dict:
        """Send a DELETE request to delete a user by ID."""
        try:
            logger.info(f"Deleting user by ID: {user_id}")
            params = {"user_id": user_id}
            response = requests.delete(f"{self.address}/DeleteUser", params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error deleting user: {e}")
            return {"error": str(e)}

    def delete_user_by_email(self, email: str, password: str) -> Dict:
        """Send a DELETE request to delete a user by email."""
        try:
            logger.info(f"Deleting user by email: {email}")
            params = {"email": email, "password": password}
            response = requests.delete(
                f"{self.address}/DeleteUserByEmail", params=params
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error deleting user by email: {e}")
            return {"error": str(e)}

    def get_user(self, user_id: str) -> Dict:
        """Send a GET request to retrieve a user by ID."""
        try:
            logger.info(f"Getting user with ID: {user_id}")
            params = {"user_id": user_id}
            response = requests.get(f"{self.address}/GetUser", params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error getting user: {e}")
            return {"error": str(e)}
