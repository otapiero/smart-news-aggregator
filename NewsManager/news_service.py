import logging
from datetime import datetime

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
            logging.info(f"cached_news: {cached_news}")
            # check the time of the last update
            # if it is more than 60 minutes, then update the cache
            if cached_news:
                last_update = cached_news.get("last_update")
                if last_update:
                    last_update = datetime.strptime(last_update, "%Y-%m-%d %H:%M:%S")
                    if (datetime.now() - last_update).total_seconds() <= 3600: # send cached news
                        await self.email_client.send_news(email, cached_news["news"])
                        return {"status": "success", "message": "Cached news sent"}

            # Step 3: Fetch fresh news from News Engine
            fresh_news = await self.news_engine_client.get_fresh_news(user_preferences)
            if not fresh_news: # if failed to fetch news send old news
                logging.info("Failed to fetch news")

                if cached_news:
                    logging.info("Sending cached news")
                    await self.email_client.send_news(email, cached_news["news"])
                    logging.info("Cached news sent")
                    return {"status": "success", "message": "Cached news sent"}
                return {"status": "error", "message": "Failed to fetch news"}

            # chose 5 articles (from all categories) to send
            news_to_send = []
            for category in fresh_news:
                news_to_send.extend(category["articles"][0])
            fresh_news = news_to_send[:5]
            # Step 4: Update the cache in News DB Accessor
            await self.news_db_client.update_news(user_preferences, fresh_news)



            # Step 4: Send the news via Email API Accessor
            await self.email_client.send_news(email, fresh_news)
            return {"status": "success", "message": "Fresh news sent"}

        except Exception as e:
            self.logger.error(f"Error in handle_get_news: {e}")
            return {"status": "error", "message": "Internal service error"}
