import json
import logging

import psycopg2
from user import User
from config import Config
import time
import asyncio


class UsersDBAccessor:
    def __init__(self):
        self._connection = self.connect_to_db()
        if self._connection:
            self.create_table()

    def connect_to_db(self, retries=3):
        for i in range(retries):
            try:
                connection = psycopg2.connect(
                    host=Config.DB_HOST,
                    port=Config.DB_PORT,
                    dbname=Config.DATABASE_NAME,
                    user=Config.DB_USER_NAME,
                    password=Config.DB_PASSWORD,
                )
                logging.info("Connected to the PostgresSQL database successfully.")
                return connection
            except psycopg2.OperationalError as e:
                logging.info(f"Database connection failed: {e}. Retrying in 5 seconds...")
                time.sleep(5)
        raise Exception(
            "Failed to connect to the PostgresSQL database after multiple attempts."
        )

    def create_table(self):
        with self._connection.cursor() as cursor:
            cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS users (
                user_id VARCHAR PRIMARY KEY,
                email TEXT UNIQUE,
                username TEXT,
                password TEXT,
                country TEXT,
                language TEXT,
                categories JSONB,
                created_at TIMESTAMP,
                updated_at TIMESTAMP,
                is_active BOOLEAN,
                notification_channel TEXT,
                telegram_user_id TEXT
            );
            """
            )
            self._connection.commit()
            logging.info("Table created successfully")

    async def disconnect(self):
        self._connection.close()

    async def create_user(self, user: User):
        with self._connection.cursor() as cursor:
            query = """
            INSERT INTO users (
                user_id, email, username, password, country, language, categories, created_at, updated_at, is_active, notification_channel, telegram_user_id
            )
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
            RETURNING user_id;
            """
            cursor.execute(
                query,
                (
                    user.user_id,
                    user.email,
                    user.username,
                    user.password,
                    user.country,
                    user.language,
                    json.dumps(user.categories),
                    user.created_at,
                    user.updated_at,
                    user.is_active,
                    user.notification_channel,
                    user.telegram_user_id,
                ),
            )
            self._connection.commit()

            return cursor.fetchone()[0]

    async def get_user_by_id(self, user_id: str):
        with self._connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE user_id = %s;", (user_id,))
            result = cursor.fetchone()
            if result:
                user_data = dict(
                    zip(
                        [
                            "user_id",
                            "email",
                            "username",
                            "password",
                            "country",
                            "language",
                            "categories",
                            "created_at",
                            "updated_at",
                            "is_active",
                            "notification_channel",
                            "telegram_user_id",
                        ],
                        result,
                    )
                )
                user_data["categories"] = user_data["categories"] or []
                return User.from_dict(user_data)
            return None

    async def update_user_by_id( self, user_id: str, user: User ):
        with self._connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE users
                SET email = %s, username = %s, password = %s, country = %s, language = %s, categories = %s, created_at = %s, updated_at = %s, is_active = %s, notification_channel = %s, telegram_user_id = %s
                WHERE user_id = %s;
                """,
                (
                    user.email,
                    user.username,
                    user.password,
                    user.country,
                    user.language,
                    json.dumps(user.categories),
                    user.created_at,
                    user.updated_at,
                    user.is_active,
                    user.notification_channel,
                    user.telegram_user_id,
                    user_id,
                ),
            )
            self._connection.commit()

    async def delete_user_by_id(self, user_id: str):
        with self._connection.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE user_id = %s;", (user_id,))
            self._connection.commit()

    # important discalimair : in current implementation I don't have authentication for the system,
    # so I'm using email and password for authentication, in the future I should use a token and the user_id
    async def get_user_by_email(self, email: str):
        with self._connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE email = %s;", (email,))
            result = cursor.fetchone()
            if result:
                user_data = dict(
                    zip(
                        [
                            "user_id",
                            "email",
                            "username",
                            "password",
                            "country",
                            "language",
                            "categories",
                            "created_at",
                            "updated_at",
                            "is_active",
                            "notification_channel",
                            "telegram_user_id",
                        ],
                        result,
                    )
                )
                user_data["categories"] = user_data["categories"] or []
                return User.from_dict(user_data)
            return None

    async def update_user_by_email( self, email: str, user: User ):
        with self._connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE users
                SET email = %s, username = %s, password = %s, country = %s, language = %s, categories = %s, created_at = %s, updated_at = %s, is_active = %s, notification_channel = %s, telegram_user_id = %s
                WHERE email = %s;
                """,
                (
                    user.email,
                    user.username,
                    user.password,
                    user.country,
                    user.language,
                    json.dumps(user.categories),
                    user.created_at,
                    user.updated_at,
                    user.is_active,
                    user.notification_channel,
                    user.telegram_user_id,
                    email,
                ),
            )
            self._connection.commit()

    async def delete_user_by_email(self, email: str):
        # this will not really delete the user, it will only set the is_active to False
        with self._connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE users
                SET is_active = %s
                WHERE email = %s;
                """,
                (False, email),
            )
            self._connection.commit()
