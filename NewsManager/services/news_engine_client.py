import logging
from dapr.clients import DaprClient
import json


class AsyncHTTPNewsEngineClient:
    def __init__(self, dapr_http_port):
        self.logger = logging.getLogger(__name__)
        self.client = DaprClient()
        self.dapr_http_port = dapr_http_port

    async def get_fresh_news(self, preferences):
        try:
            self.logger.info("Fetching fresh news from News Engine...")
            response = await self.client.invoke_method_async(
                app_id="news_engine",
                method_name="get-fresh-news",
                data=json.dumps(preferences).encode("utf-8"),
                content_type="application/json",
            )
            if response.status_code == 200:
                news = json.loads(response.data.decode("utf-8"))
                return news.get("data", [])
            return []
        except Exception as e:
            self.logger.error(f"Error fetching news from News Engine: {e}")
            return []
