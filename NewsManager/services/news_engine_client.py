import logging
from dapr.clients import DaprClient
import json


class AsyncHTTPNewsEngineClient:
    def __init__(self, dapr_http_port):
        self.logger = logging.getLogger(__name__)
        self.client = DaprClient()
        self.dapr_http_port = dapr_http_port

    def get_fresh_news(self, preferences):
        try:
            self.logger.info("Fetching fresh news from News Engine...")
            response = self.client.invoke_method(
                app_id="news_engine",
                method_name="get-fresh-news",
                data=json.dumps(preferences).encode("utf-8"),
                content_type="application/json",
            )
            if response.status_code == 200:
                data_response = json.loads(response.data.decode("utf-8"))
                news = data_response.get("data", [])
                if data_response.get("status") == "success":
                    self.logger.info("Successfully fetched news from News Engine")
                    return news
                else:
                    self.logger.error(
                        f"Error fetching news from News Engine: {data_response.get('message')}"
                    )
            return []
        except Exception as e:
            self.logger.error(f"Error fetching news from News Engine: {e}")
            return []
