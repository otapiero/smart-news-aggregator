import logging
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

    async def handle_get_news(self, email, password):
        try:
            # Step 1: Validate user and get preferences
            user_preferences = await self.users_manager_client.get_user_preferences(
                email, password
            )
            if "error" in user_preferences:
                return {"status": "error", "message": user_preferences["error"]}

            # Step 2: Check cached news in News DB Accessor
            cached_news = await self.news_db_client.get_cached_news(user_preferences)
            if cached_news:
                self.logger.info("Cached news found, sending to user...")
                await self.email_client.send_news(email, cached_news)
                return {"status": "success", "message": "News sent from cache"}

            # Step 3: Fetch fresh news from News Engine
            fresh_news = await self.news_engine_client.get_fresh_news(user_preferences)
            if not fresh_news:
                return {"status": "error", "message": "Failed to fetch news"}

            # Step 4: Send the news via Email API Accessor
            await self.email_client.send_news(email, fresh_news)
            return {"status": "success", "message": "Fresh news sent"}

        except Exception as e:
            self.logger.error(f"Error in handle_get_news: {e}")
            return {"status": "error", "message": "Internal service error"}
