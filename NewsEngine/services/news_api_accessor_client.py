import logging
from typing import List, Dict

from dapr.clients import DaprClient
import json

from services.news_article import NewsArticle

logger = logging.getLogger(__name__)


class AsyncGRPCNewsApiClient:
    def __init__(self, app_id):
        self.app_id = app_id
        self.dapr_client = DaprClient()
        self.logger = logging.getLogger(__name__)

    async def get_news_by_categories(
        self, categories, language, country
    ) -> Dict[str, List[NewsArticle]]:
        try:
            self.logger.info(
                f"Getting news for categories: {categories}, language: {language}, country: {country}"
            )
            response = await self.dapr_client.invoke_method_async(
                app_id=self.app_id,
                method_name="get_news_by_categories",
                content_type="application/grpc",
                data=json.dumps(
                    {"categories": categories, "language": language, "country": country}
                ).encode("utf-8"),
            )
            self.logger.info(f"GOT RESPONSE: {response.status_code}")

            data = json.loads(response.data.decode("utf-8"))

            if data["status"] == "success":
                news_articles = await self._extract_articles_by_category(data)
                return news_articles
            elif data["status"] == "error":
                self.logger.error(f"Error getting news: {data['message']}")
                return {}
            else:
                self.logger.error(f"Invalid response from Dapr: {data}")
                return {}

        except Exception as e:
            self.logger.error(f"Error getting news by categories: {e}")
            return {}

    async def _extract_articles_by_category(
        self, parsed_data
    ) -> Dict[str, List[NewsArticle]]:
        """
        Extracts articles grouped by category, each containing the body, title, image URL, and URL.

        Args:
            data (bytes): The raw data object containing article information in JSON format.

        Returns:
            dict: A dictionary where each key is a category, and the value is a list of articles.
        """
        try:
            categorized_articles = {}

            # Navigate to the articles within the data
            for category_data in parsed_data.get("data", []):
                category = category_data.get("category", "Unknown")
                articles = []

                for article in category_data.get("articles", []):
                    # Extract required fields
                    article_info = {
                        "title": article.get("title", "No Title"),
                        "body": article.get("body", "No Body"),
                        "image": article.get("image", "No Image URL"),
                        "url": article.get("url", "No URL"),
                        "dateTimePub": article.get("dateTimePub", "No Date"),
                        "category": category,
                    }
                    article = NewsArticle.from_dict(article_info)
                    articles.append(article)

                # Store articles in the appropriate category list
                if category not in categorized_articles:
                    categorized_articles[category] = []
                categorized_articles[category].extend(articles)

            return categorized_articles
        except (json.JSONDecodeError, AttributeError, TypeError) as e:
            print(f"Error processing data: {e}")
            return {}
