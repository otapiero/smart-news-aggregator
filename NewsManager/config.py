import os


class Config:
    DEBUG = os.getenv("DEBUG", True)
    APP_PORT = os.getenv("APP_PORT", 5000)
    EMAIL_API_ACCESSOR_SERVICE_APP_ID = os.getenv(
        "EMAIL_API_ACCESSOR_SERVICE_APP_ID", "email_api_accessor"
    )
    NEWS_ENGINE_SERVICE_APP_ID = os.getenv("NEWS_ENGINE_SERVICE_APP_ID", "news_engine")
    NEWS_DB_ACCESSOR_SERVICE_APP_ID = os.getenv(
        "NEWS_DB_ACCESSOR_SERVICE_APP_ID", "news_db_accessor"
    )
    NEWS_API_APP_ID = os.getenv("NEWS_API_APP_ID", "newsapi_accessor")
    DAPR_HTTP_PORT = os.getenv("DAPR_HTTP_PORT", "3500")
    USERS_MANAGER_SERVICE_APP_ID = os.getenv(
        "USERS_MANAGER_SERVICE_APP_ID", "users_manager"
    )
