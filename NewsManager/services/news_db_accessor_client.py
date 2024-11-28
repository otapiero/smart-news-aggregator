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
            data = {
                "language": preferences.get("language"),
                "country": preferences.get("country"),
                "categories": preferences.get("categories"),
            }
            self.logger.info("Checking cache for news...")
            response = await self.client.invoke_method_async(
                app_id=self.app_id,
                method_name="get_news",
                data=json.dumps(data).encode("utf-8"),
                content_type="application/json",
            )
            if response.status_code == 200:
                news = json.loads(response.data.decode("utf-8"))
                return news.get("data", [])
            return None
        except Exception as e:
            self.logger.error(f"Error checking cached news: {e}")
            return None

    async def update_news(self, language, country, category, news):
        try:
            self.logger.info("Updating cache with fresh news...")
            data = {
                "language": language,
                "country": country,
                "category": category,
                "articles": news,
            }
            response = await self.client.invoke_method_async(
                app_id=self.app_id,
                method_name="update_news",
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
