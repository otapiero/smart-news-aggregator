from services.news_article import NewsArticle
import logging
from typing import List, Dict

from dapr.clients import DaprClient

import json


class AsyncGRPCLLMApiClient:

    def __init__(self, app_id: str):
        self.app_id = app_id
        self.logger = logging.getLogger(__name__)
        self.dapr_client = DaprClient()

    async def summarize(
        self, articles: Dict[str, List[NewsArticle]]
    ) -> Dict[str, List[Dict]]:
        """
        Summarizes articles grouped by categories.

        Args:
            articles: A dictionary where the key is the category, and the value is a list of NewsArticle objects.

        Returns:
            A dictionary of summarized articles grouped by category, or an empty dict on failure.
        """
        try:
            # Convert NewsArticle objects to dictionaries
            articles_dict = {
                category: [article.to_dict() for article in articles_list]
                for category, articles_list in articles.items()
            }

            # Send the request
            return await self._summarize(articles_dict)
        except Exception as e:
            self.logger.error(f"Unexpected error preparing summarization request: {e}")
            return {}

    async def _summarize(
        self, articles_dict: Dict[str, List[Dict]]
    ) -> Dict[str, List[Dict]]:
        try:
            self.logger.info("Sending request to summarize articles...")
            response = await self.dapr_client.invoke_method_async(
                app_id=self.app_id,
                method_name="summarize",
                content_type="application/json",  # Adjusted to match service.py
                data=json.dumps(articles_dict).encode("utf-8"),
            )

            # Log status and decode response
            self.logger.info(
                f"Received response with status code: {response.status_code}"
            )
            response_data = json.loads(response.data.decode("utf-8"))

            if response_data["status"] == "success":
                self.logger.info("Summarization successful.")
                return response_data["data"]
            elif response_data["status"] == "error":
                self.logger.error(f"Error from service: {response_data['message']}")
                if response.status_code == 429:
                    self.logger.warning("Rate limit exceeded.")
                return {}
            else:
                self.logger.error(f"Unexpected response format: {response_data}")
                return {}

        except json.JSONDecodeError as e:
            self.logger.error(f"Error decoding response JSON: {e}")
            return {}

        except Exception as e:
            self.logger.error(f"Error during summarization request: {e}")
            return {}
