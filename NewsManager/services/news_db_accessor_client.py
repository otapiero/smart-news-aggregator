import logging
from dapr.clients import DaprClient
import json


class AsyncHTTPNewsDBAccessorClient:
    def __init__(self, app_id):
        self.logger = logging.getLogger(__name__)
        self.client = DaprClient()
        self.app_id = app_id

    async def get_cached_news(self, preferences):
        try:
            self.logger.info("Checking cache for news...")
            response = await self.client.invoke_method_async(
                app_id=self.app_id,
                method_name="get-cached-news",
                data=json.dumps(preferences).encode("utf-8"),
                content_type="application/json",
            )
            if response.status_code == 200:
                news = json.loads(response.data.decode("utf-8"))
                return news.get("data", [])
            return None
        except Exception as e:
            self.logger.error(f"Error checking cached news: {e}")
            return None

    async def update_news ( self, user_preferences, fresh_news):
        try:
            self.logger.info("Updating cache with fresh news...")
            data = {"preferences": user_preferences, "news": fresh_news}
            response = await self.client.invoke_method_async(
                app_id=self.app_id,
                method_name="update-news",
                data=json.dumps(data).encode("utf-8"),
                content_type="application/json",
            )
            if response.status_code == 200:
                self.logger.info("Cache updated successfully")
                return True
            else:
                self.logger.error(f"Failed to update cache: {response.text()}")
                return False
        except Exception as e:
            self.logger.error(f"Error updating cache: {e}")
            return False
