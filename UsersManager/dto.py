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
