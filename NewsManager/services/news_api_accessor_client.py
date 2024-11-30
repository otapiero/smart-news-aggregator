import logging
import asyncio
from typing import List

from dapr.clients import DaprClient
from dapr.ext.grpc import InvokeMethodResponse, InvokeMethodRequest
import json


class AsyncGRPCNewsApiClient:
    def __init__(self, app_id):
        self.app_id = app_id
        self.dapr_client = DaprClient()
        self.logger = logging.getLogger(__name__)

    def get_news_by_categories(self, categories, language, country) -> List[dict]:
        try:
            self.logger.info(
                f"Getting news for categories: {categories}, language: {language}, country: {country}"
            )
            response = self.dapr_client.invoke_method(
                app_id=self.app_id,
                method_name="get_news_by_categories",
                content_type="application/grpc",
                data=json.dumps(
                    {"categories": categories, "language": language, "country": country}
                ).encode("utf-8"),
            )
            self.logger.info(f"Received news: {response.data}")
            data = json.loads(response.data.decode("utf-8"))
            if data["status"] == "success":
                news = data["data"]
                return news
            elif data["status"] == "error":
                self.logger.error(f"Error getting news: {data['message']}")
                return []
            else:
                self.logger.error(f"Invalid response from Dapr: {data}")
                return []

        except Exception as e:
            self.logger.error(f"Error getting news by categories: {e}")
            return []
