from flask import Flask, request

from user import User
from users_db_accessor import UsersDBAccessor
import logging
import asyncio
from http import HTTPStatus

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
users_db_accessor = UsersDBAccessor()


@app.route("/CreateUser", methods=["POST"])
async def CreateUser():
    try:
        logger.info("Creating user")
        user = request.json
        logger.info(f"User: {user}")
        user = User.from_dict(user)
        # check if user already exists in the database by email
        if await users_db_accessor.get_user_by_email(user.email):
            logger.error("User already exists")
            return {"error": "user email already exists"}, HTTPStatus.BAD_REQUEST
        # check if user already exists in the database by user_id
        if await users_db_accessor.get_user_by_id(user.user_id):
            logger.error("User already exists")
            return {"error": "User id already exists"}, HTTPStatus.BAD_REQUEST
        await users_db_accessor.create_user(user)
        logger.info(f"Created user with id {user.user_id}")
        return {"success": True}, HTTPStatus.OK

    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        return {"error": "Internal error"}, HTTPStatus.INTERNAL_SERVER_ERROR


@app.route("/GetUser", methods=["GET"])
async def GetUser():
    try:
        logger.info("Getting user")
        user_id = request.args.get("user_id")
        user = await users_db_accessor.get_user_by_id(user_id)
        if not user:
            logger.error("User not found")
            return {"error": "User not found"}, HTTPStatus.NOT_FOUND
        logger.info(f"Getting user with id {user_id}")
        return user.to_dict(), HTTPStatus.OK
    except Exception as e:
        logger.error(f"Error getting user: {str(e)}")
        return {"error": "Internal error"}, HTTPStatus.INTERNAL_SERVER_ERROR


@app.route("/GetUserPreferencesByEmailAddress", methods=["GET"])
async def GetUserPreferencesByEmailAddress():
    try:
        logger.info("Getting user preferences")
        email = request.args.get("email")
        password = request.args.get("password")
        user = await users_db_accessor.get_user_by_email(email)
        if not user:
            logger.error("User not found")
            return {"error": "User not found"}, HTTPStatus.NOT_FOUND
        if user.password != password:
            logger.error(f"Invalid password for user {user.email}")
            return {
                "error": f"Invalid password for user {user.email}"
            }, HTTPStatus.UNAUTHORIZED
        if not user.is_active:
            logger.error(f"User {user.email} is not active")
            return {"error": f"User {user.email} is not active"}, HTTPStatus.FORBIDDEN
        logger.info(f"Getting user preferences with email {email}")
        return user.to_dict(), HTTPStatus.OK
    except Exception as e:
        logger.error(f"Error getting user preferences: {str(e)}")
        return {"error": "Internal error"}, HTTPStatus.INTERNAL_SERVER_ERROR


@app.route("/UpdateUser", methods=["PUT"])
async def UpdateUser():
    try:
        logger.info("Updating user")
        user = request.json
        user = User.from_dict(user)
        old_user = await users_db_accessor.get_user_by_id(user.user_id)
        if not old_user:
            logger.error("User not found")
            return {"error": "User not found"}, HTTPStatus.NOT_FOUND
        await users_db_accessor.update_user_by_id(user_id=user.user_id, user=user)
        logger.info(f"Updated user with id {user.user_id}")
        return {"success": True}, HTTPStatus.OK
    except Exception as e:
        logger.error(f"Error updating user: {str(e)}")
        return {"error": "Internal error"}, HTTPStatus.INTERNAL_SERVER_ERROR


@app.route("/UpdateUserByEmail", methods=["PUT"])
async def UpdateUserByEmail():
    try:
        logger.info("Updating user by email")

        new_user = request.json["user"]
        old_password = request.json["password"]
        old_email = request.json["email"]
        old_user = await users_db_accessor.get_user_by_email(old_email)
        if not old_user:
            logger.error("User not found")
            return {"error": "User not found"}, HTTPStatus.NOT_FOUND
        if old_user.password != old_password:
            logger.error(f"Invalid password for user {old_user.email}")
            return {
                "error": f"Invalid password for user {old_user.email}"
            }, HTTPStatus.UNAUTHORIZED
        new_user = User.from_dict(new_user)
        new_user = merge_user_data(new_user, old_user)
        await users_db_accessor.update_user_by_email(email=old_email, user=new_user)
        logger.info(f"Updated user with email {old_user.email}")
        return {"success": True}, HTTPStatus.OK
    except Exception as e:
        logger.error(f"Error updating user: {str(e)}")
        return {"error": "Internal error"}, HTTPStatus.INTERNAL_SERVER_ERROR


def merge_user_data(new_user: User, old_user: User):
    """
    Merge user data from new_user and old_user, permitting client to update only the fields they want to change.
    """
    for field in [
        "email",
        "username",
        "language",
        "country",
        "categories",
        "notification_channel",
        "telegram_user_id",
    ]:
        setattr(new_user, field, getattr(new_user, field) or getattr(old_user, field))
    new_user.created_at = old_user.created_at
    new_user.updated_at = new_user.updated_at
    return new_user


@app.route("/DeleteUser", methods=["DELETE"])
async def DeleteUser():
    try:
        logger.info("Deleting user")
        user_id = request.args.get("user_id")
        user = await users_db_accessor.get_user_by_id(user_id)
        if not user:
            logger.error("User not found")
            return {"error": "User not found"}, HTTPStatus.NOT_FOUND
        await users_db_accessor.delete_user_by_id(user_id=user.user_id)
        logger.info(f"Deleted user with id {user.user_id}")
        return {"success": True}, HTTPStatus.OK
    except Exception as e:
        logger.error(f"Error deleting user: {str(e)}")
        return {"error": "Internal error"}, HTTPStatus.INTERNAL_SERVER_ERROR


@app.route("/DeleteUserByEmail", methods=["DELETE"])
async def DeleteUserByEmail():
    try:
        logger.info("Deleting user by email")
        email = request.args.get("email")
        password = request.args.get("password")
        user = await users_db_accessor.get_user_by_email(email)
        if not user:
            logger.error("User not found")
            return {"error": "User not found"}, HTTPStatus.NOT_FOUND
        if user.password != password:
            logger.error(f"Invalid password for user {user.email}")
            return {
                "error": f"Invalid password for user {user.email}"
            }, HTTPStatus.UNAUTHORIZED
        await users_db_accessor.delete_user_by_email(email=user.email)
        logger.info(f"Deleted user with email {user.email}")
        return {"success": True}, HTTPStatus.OK
    except Exception as e:
        logger.error(f"Error deleting user: {str(e)}")
        return {"error": "Internal error"}, HTTPStatus.INTERNAL_SERVER_ERROR


if __name__ == "__main__":
    logger.info("Starting server...")
    app.run(port=50057)
    logger.info("Exiting server...")
