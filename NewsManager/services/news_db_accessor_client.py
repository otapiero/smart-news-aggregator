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
