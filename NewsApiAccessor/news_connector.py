from typing import Union, Dict, List

import dotenv

from news_api_config import NewsApiConfig
import logging
import time
from eventregistry import EventRegistry, QueryArticlesIter


class NewsApiConnector:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.event_registry = EventRegistry(apiKey=self.api_key)

    def _get_date_range(self):
        """Helper method to get date range for the last 7 days."""
        end_time = time.time()
        start_time = end_time - 86400  # 1 day in seconds
        end_date = time.strftime("%Y-%m-%d", time.localtime(end_time))
        start_date = time.strftime("%Y-%m-%d", time.localtime(start_time))
        return start_date, end_date

    def get_news(
        self, country: str = "us", language: str = "english", category: str = "politics"
    ) -> Dict:
        try:
            logging.info("Getting news")
            start_date, end_date = self._get_date_range()
            country_uri = NewsApiConfig.get_country_uri(country)
            category_uri = NewsApiConfig.get_category_uri(category)
            language_code = NewsApiConfig.get_language_code(language)

            if not country_uri or not category_uri or not language_code:
                return {"error": "Invalid country, category, or language provided"}

            query = QueryArticlesIter(
                sourceLocationUri=country_uri,
                categoryUri=category_uri,
                dataType=["news"],
                lang=language_code,
                dateStart=start_date,
                dateEnd=end_date,
                startSourceRankPercentile=0,
                endSourceRankPercentile=30,
            )

            news_list = []
            for article in query.execQuery(
                self.event_registry, sortBy="date", maxItems=10
            ):
                news_list.append(article)

            logging.info("Got news")
            return {"articles": news_list}
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return {"error": "Internal error"}

    def get_news_by_topic(
        self, topic: str, country: str = "us", language: str = "english"
    ) -> Dict:
        try:
            logging.info("Getting news by topic")
            start_date, end_date = self._get_date_range()
            country_uri = NewsApiConfig.get_country_uri(country)
            language_code = NewsApiConfig.get_language_code(language)

            if not country_uri or not language_code:
                return {"error": "Invalid country or language provided"}

            query = QueryArticlesIter.initWithComplexQuery(
                {
                    "$query": {
                        "$and": [
                            {"keyword": topic},
                            {"sourceLocationUri": country_uri},
                            {"dateStart": start_date, "dateEnd": end_date},
                            {"lang": language_code},
                        ]
                    },
                    "$filter": {
                        "startSourceRankPercentile": 0,
                        "endSourceRankPercentile": 30,
                    },
                }
            )

            news_list = []
            for article in query.execQuery(
                self.event_registry, sortBy="date", maxItems=10
            ):
                news_list.append(article)

            logging.info("Got news by topic")
            return {"articles": news_list}
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return {"error": "Internal error"}

    def get_news_by_categories(
        self, categories: List[str], country: str = "us", language: str = "english"
    ) -> Union[Dict, List[Dict]]:
        try:
            logging.info("Getting news by categories")
            news_by_category = []
            for category in categories:
                category_uri = NewsApiConfig.get_category_uri(category)

                if not category_uri:
                    continue

                category_news = []
                articles = self.get_news(
                    country=country, language=language, category=category
                )

                if "error" in articles:
                    continue

                category_news.extend(articles["articles"])

                news_by_category.append(
                    {"category": category, "articles": category_news}
                )

            logging.info("Got news by categories")
            return news_by_category
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return {"error": "Internal error"}


if __name__ == "__main__":
    dotenv.load_dotenv()
    import os

    news_api_key = os.getenv("NEWS_API_AI_API_KEY")
    news_api_connector = NewsApiConnector(api_key=news_api_key)
    news = news_api_connector.get_news()
    print(news)
    news_by_topic = news_api_connector.get_news_by_topic(topic="elections")
    print(news_by_topic)
    news_by_categories = news_api_connector.get_news_by_categories(
        categories=["politics", "business"]
    )
    print(news_by_categories)
