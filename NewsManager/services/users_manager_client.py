import logging
import asyncio
from typing import List, Dict

from dapr.clients import DaprClient
import json


class AsyncHTTPUsersManagerClient:
    def __init__(self, app_id):
        self.logger = logging.getLogger(__name__)
        self.client = DaprClient()
        self.app_id = app_id

    async def get_user_preferences(self, email: str, password: str) -> Dict[str, str]:
        try:
            self.logger.info(f"Getting preferences for user: {email}")
            data = {"email": email, "password": password}
            response = await self.client.invoke_method_async(
                app_id=self.app_id,
                method_name="GetUserPreferencesByEmailAddress",
                data=json.dumps(data).encode("utf-8"),
                content_type="application/grpc",
            )
            self.logger.info(f"Received preferences: {response.data}")
            data = json.loads(response.data.decode("utf-8"))
            if "error" in data:
                return {"error": data["error"]}
            elif "success" in data:
                return data["preferences"]
            else:
                return {"error": "Invalid response from Dapr"}

        except Exception as e:
            self.logger.error(f"Error getting user preferences: {e}")
            return {"error": str(e)}
