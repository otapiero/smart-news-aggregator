import os


class Config:
    APP_PORT = int(os.getenv("APP_PORT", 5000))
    DEBUG = bool(os.getenv("DEBUG", True))
    USERS_MANAGER_APP_ID = os.getenv("USERS_MANAGER_APP_ID", "users_manager")
    NEWS_MANAGER_APP_ID = os.getenv("NEWS_MANAGER_APP_ID", "news_manager")
