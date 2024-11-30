import logging
from datetime import datetime, timedelta
from typing import Dict, List

from services.users_manager_client import AsyncHTTPUsersManagerClient
from services.news_db_accessor_client import AsyncHTTPNewsDBAccessorClient
from services.news_engine_client import AsyncHTTPNewsEngineClient
from services.email_api_accessor_client import AsyncHTTPEmailAPIClient
from config import Config


class NewsService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.users_manager_client = AsyncHTTPUsersManagerClient(
            Config.USERS_MANAGER_SERVICE_APP_ID
        )
        self.news_db_client = AsyncHTTPNewsDBAccessorClient(
            Config.NEWS_DB_ACCESSOR_SERVICE_APP_ID
        )
        self.news_engine_client = AsyncHTTPNewsEngineClient(
            Config.NEWS_ENGINE_SERVICE_APP_ID
        )
        self.email_client = AsyncHTTPEmailAPIClient(
            Config.EMAIL_API_ACCESSOR_SERVICE_APP_ID
        )

    def handle_get_news(self, email, password):
        try:
            # Step 1: Validate user and get preferences
            user_preferences = self.users_manager_client.get_user_preferences(
                email, password
            )
            if "error" in user_preferences:
                return {"status": "error", "message": user_preferences["error"]}

            # Step 2: Check cached news in News DB Accessor
            cached_news = self.news_db_client.get_cached_news(user_preferences)
            self.logger.info(f"gotten cached news length: {len(cached_news.values())}")
            if any(cached_news.values()):
                filtered_cached_news = self._filter_old_articles(
                    cached_news, max_age_minutes=Config.CACHED_NEWS_MAX_AGE_MINUTES
                )
                if len(filtered_cached_news.values()) > Config.NUM_ARTICLES_TO_SEND:
                    news_to_send = self._choose_articles_to_send(
                        filtered_cached_news, num_articles=Config.NUM_ARTICLES_TO_SEND
                    )
                    self.logger.info(f"Sending cached news: {news_to_send}")
                    self.email_client.send_news(email, news_to_send)
                    return {"status": "success", "message": "Cached news sent"}

            # Step 3: Fetch fresh news from News Engine
            fresh_news = self.news_engine_client.get_fresh_news(user_preferences)
            if not fresh_news:  # if failed to fetch news send old news
                self.logger.info("Failed to fetch news")
                return self._handle_fallback(cached_news, email)

            # chose 5 articles to send
            news_to_send = self._choose_articles_to_send(
                fresh_news, num_articles=Config.NUM_ARTICLES_TO_SEND
            )
            self._update_news_cache(user_preferences, fresh_news)

            self.email_client.send_news(email, news_to_send)
            return {"status": "success", "message": "Fresh news sent"}

        except Exception as e:
            self.logger.error(f"Error in handle_get_news: {e}")
            return {"status": "error", "message": "Internal service error"}

    def _handle_fallback(self, cached_news: dict, email: str) -> dict:
        if cached_news:
            self.logger.info("Sending cached news due to fresh news fetch failure")
            cached_news = self._filter_old_articles(
                cached_news, max_age_minutes=60 * 24 * 365
            )
            news_to_send = self._choose_articles_to_send(
                cached_news, num_articles=Config.NUM_ARTICLES_TO_SEND
            )
            self.email_client.send_news(email, news_to_send)
            return {"status": "success", "message": "Cached news sent"}
        return {"status": "error", "message": "Failed to fetch news"}

    def _choose_articles_to_send(
        self, news: Dict[str, List[dict]], num_articles: int = 5
    ) -> List[dict]:
        """
        Choose articles to send from fresh_news, prioritizing articles with URLs and images.
        """
        news_to_send = []
        categories = list(news.keys())
        i = 0
        while len(news_to_send) < num_articles:
            articles_list = news[categories[i % len(categories)]]
            if articles_list:
                articles_list.sort(key=self._article_priority, reverse=True)
                news_to_send.append(articles_list.pop(0))
            i += 1
        return news_to_send

    def _article_priority(self, article: dict) -> int:
        """
        Return priority score based on the presence of URL and image.
        """
        return bool(article.get("url")) + bool(article.get("image"))

    def _filter_old_articles(
        self, cached_news: dict, max_age_minutes: int = 60
    ) -> dict:
        """
        Filters out articles older than max_age_minutes from each category in cached_news.
        """
        now = datetime.now()
        max_age = timedelta(minutes=max_age_minutes)
        filtered_news = {
            category: [
                article["article"]
                for article in articles
                if now - datetime.fromisoformat(article["timestamp"].replace("Z", ""))
                <= max_age
            ]
            for category, articles in cached_news.items()
        }
        return filtered_news

    def _update_news_cache(self, user_preferences: dict, fresh_news: dict):
        """
        Update the news cache in the News DB Accessor.
        """
        for category, articles in fresh_news.items():
            if articles:
                self.logger.info(f"Updating news for category: {category}")
                self.news_db_client.update_news(
                    user_preferences["language"],
                    user_preferences["country"],
                    category,
                    articles,
                )
