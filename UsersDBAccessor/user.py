from typing import List

import protos.users_db_accessor_pb2 as users_db_accessor_pb2

"""message User {
    string user_id = 1;
    string email = 2;
    string username = 3;
    string country = 4;
    string language = 5;
    repeated string categories = 6;
    string created_at = 7;
    string updated_at = 8;
    bool is_active = 9;
    string notification_channel = 10;
    string telegram_user_id = 11;
}"""


class User:
    def __init__(
        self,
        user_id: str,
        email: str,
        username: str,
        password: str,
        country: str,
        language: str,
        categories: List[str],
        created_at: str,
        updated_at: str,
        is_active: bool,
        notification_channel: str,
        telegram_user_id: str = "",
    ):
        self.user_id = user_id
        self.email = email
        self.username = username
        self.password = password
        self.country = country
        self.language = language
        self.categories = categories
        self.created_at = created_at
        self.updated_at = updated_at
        self.is_active = is_active
        self.notification_channel = notification_channel
        self.telegram_user_id = telegram_user_id

    def __repr__(self):
        return f"User(user_id={self.user_id}, email={self.email}, username={self.username})"

    def __eq__(self, other):
        return isinstance(other, User) and self.to_dict() == other.to_dict()

    def to_proto(self):
        user = users_db_accessor_pb2.User()
        user.user_id = self.user_id
        user.email = self.email
        user.username = self.username
        user.password = self.password
        user.country = self.country
        user.language = self.language
        user.categories.extend(self.categories)
        user.created_at = self.created_at
        user.updated_at = self.updated_at
        user.is_active = self.is_active
        user.notification_channel = self.notification_channel
        user.telegram_user_id = self.telegram_user_id
        return user

    @staticmethod
    def from_proto(user) -> "User":
        try:
            return User(
                user.user_id,
                user.email,
                user.username,
                user.password,
                user.country,
                user.language,
                list(user.categories),
                user.created_at,
                user.updated_at,
                user.is_active,
                user.notification_channel,
                user.telegram_user_id,
            )
        except AttributeError as e:
            raise ValueError(f"Invalid User protobuf message: {e}")

    @staticmethod
    def from_dict(user_dict):
        return User(
            user_dict["user_id"],
            user_dict["email"],
            user_dict["username"],
            user_dict["password"],
            user_dict["country"],
            user_dict["language"],
            user_dict["categories"],
            user_dict["created_at"],
            user_dict["updated_at"],
            user_dict["is_active"],
            user_dict["notification_channel"],
            user_dict["telegram_user_id"],
        )

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "email": self.email,
            "username": self.username,
            "password": self.password,
            "country": self.country,
            "language": self.language,
            "categories": self.categories,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "is_active": self.is_active,
            "notification_channel": self.notification_channel,
            "telegram_user_id": self.telegram_user_id,
        }
