from dataclasses import dataclass
from typing import List, Optional


@dataclass
class UserDTO:
    email: str
    username: str
    password: str
    country: str
    language: str
    categories: List[str]
    notification_channel: str
    telegram_user_id: Optional[str] = None

    def __init__(
        self,
        email: str,
        username: str,
        password: str,
        country: str,
        language: str,
        categories: List[str],
        notification_channel: str,
        telegram_user_id: Optional[str] = None,
    ):
        self.email = email
        self.username = username
        self.password = password
        self.country = country
        self.language = language
        self.categories = categories
        self.notification_channel = notification_channel
        self.telegram_user_id = telegram_user_id
