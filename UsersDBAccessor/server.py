
from dapr.ext.grpc import App, InvokeMethodResponse
from pyexpat.errors import messages

from user import User
from users_db_accessor import UsersDBAccessor
import protos.users_db_accessor_pb2 as users_db_accessor_pb2
import logging
import asyncio

logging.basicConfig(level=logging.INFO)
app = App()

users_db_accessor = UsersDBAccessor()


app.method(name="CreateUser")


def CreateUser(request):
    try:
        logging.info("Creating user")
        request_proto = users_db_accessor_pb2.CreateUserRequest()
        request_proto.ParseFromString(request.data)
        user = User.from_proto(request_proto.user)
        # check if user already exists in the database by email
        if users_db_accessor.get_user_by_email(user.email):
            logging.error("User already exists")
            return InvokeMethodResponse(
                data=b'{"error": "user email already exists"}',
                content_type="application/json",
                headers=(("internal-status", "400"),),
            )
        # check if user already exists in the database by user_id
        if users_db_accessor.get_user_by_id(user.user_id):
            logging.error("User already exists")
            return InvokeMethodResponse(
                data=b'{"error": "User id already exists"}',
                content_type="application/json",
                headers=(("internal-status", "400"),),
            )
        users_db_accessor.create_user(user)
        logging.info(f"Created user with id {user.user_id}")
        return users_db_accessor_pb2.CreateUserResponse(
            bool=True, message="User created", headers=(("internal-status", "201"),)
        )
    except Exception as e:
        logging.error(f"Error creating user: {str(e)}")
        return InvokeMethodResponse(
            data=b'{"error": "Internal error"}',
            content_type="application/json",
            headers=(("internal-status", "500"),),
        )


@app.method(name="GetUser")
async def GetUser(request):
    try:
        logging.info("Getting user")
        request_proto = users_db_accessor_pb2.ByIdRequest()
        request_proto.ParseFromString(request.data)
        user = await users_db_accessor.get_user_by_id(request_proto.user_id)
        if not user:
            logging.error("User not found")
            return InvokeMethodResponse(
                data=b'{"error": "User not found"}',
                content_type="application/json",
                headers=(("internal-status", "404"),),
            )
        logging.info(f"Getting user with id {request_proto.user_id}")
        return users_db_accessor_pb2.GetUserResponse(
            user=user.to_proto(),message="success"
            ,headers=(("internal-status", "200"),)
        )
    except Exception as e:
        logging.error(f"Error getting user: {str(e)}")
        return InvokeMethodResponse(
            data=b'{"error": "Internal error"}',
            content_type="application/json",
            headers=(("internal-status", "500"),),
        )


@app.method(name="GetUserPreferencesByEmailAddress")
async def GetUserPreferencesByEmailAddress(request):
    try:
        logging.info("Getting user preferences")
        request_proto = users_db_accessor_pb2.ByEmailRequest()
        request_proto.ParseFromString(request.data)
        user = await users_db_accessor.get_user_by_email(request_proto.email)
        if not user:
            logging.error("User not found")
            return users_db_accessor_pb2.GetUserPreferencesResponse(
                message="Email User not found", headers=(("internal-status", "404"),)
            )
        if user.password != request_proto.password:
            logging.error(f"Invalid password for user {user.email}")
            return users_db_accessor_pb2.GetUserPreferencesResponse(
                message=f"Invalid password for user {user.email}", headers=(("internal-status", "401"),)
            )
        logging.info(f"Getting user preferences with email {request_proto.email}")
        return users_db_accessor_pb2.GetUserPreferencesResponse(
            categories = user.categories,
            language = user.language,
            country = user.country,
            telegram_user_id = user.telegram_user_id,
            email = user.email,
            notification_channel = user.notification_channel,
            username = user.username,
            message = "success",
            headers=(("internal-status", "200"),),
        )
    except Exception as e:
        logging.error(f"Error getting user preferences: {str(e)}")
        return InvokeMethodResponse(
            data=b'{"error": "Internal error"}',
            content_type="application/json",
            headers=(("internal-status", "500"),),
        )

@app.method(name="UpdateUser")
async def UpdateUser(request):
    try:
        logging.info("Updating user")
        request_proto = users_db_accessor_pb2.UpdateUserRequest()
        request_proto.ParseFromString(request.data)
        user = await users_db_accessor.get_user_by_id(request_proto.user.user_id)
        if not user:
            logging.error("User not found")
            return InvokeMethodResponse(
                data=b'{"error": "User not found"}',
                content_type="application/json",
                headers=(("internal-status", "404"),),
            )
        user = User.from_proto(request_proto.user)
        await users_db_accessor.update_user_by_id(user_id=user.user_id, user=user)

        logging.info(f"Updated user with id {user.user_id}")
        return users_db_accessor_pb2.UpdateUserResponse(
            bool=True, message="User updated", headers=(("internal-status", "200"),)
        )
    except Exception as e:
        logging.error(f"Error updating user: {str(e)}")
        return InvokeMethodResponse(
            data=b'{"error": "Internal error"}',
            content_type="application/json",
            headers=(("internal-status", "500"),),
        )


@app.method(name="UpdateUserByEmail")
async def UpdateUserByEmail(request):
    try:
        logging.info("Updating user by email")
        request_proto = users_db_accessor_pb2.UpdateUserRequest()
        request_proto.ParseFromString(request.data)
        old_user = await users_db_accessor.get_user_by_email(request_proto.email)

        if not old_user:
            logging.error("User not found")
            return InvokeMethodResponse(
                data=b'{"error": "User not found"}',
                content_type="application/json",
                headers=(("internal-status", "404"),),
            )

        if old_user.password != request_proto.password:
            logging.error(f"Invalid password for user {old_user.email}")
            return users_db_accessor_pb2.UpdateUserResponse(
                message=f"Invalid password for user {old_user.email}", headers=(("internal-status", "401"),)
            )

        user = User.from_proto(request_proto.user)

        # Fill empty fields in user with old_user fields
        user.username = user.username or old_user.username
        user.language = user.language or old_user.language
        user.country = user.country or old_user.country
        user.categories = user.categories or old_user.categories
        user.notification_channel = user.notification_channel or old_user.notification_channel
        user.telegram_user_id = user.telegram_user_id or old_user.telegram_user_id

        await users_db_accessor.update_user_by_email(email=old_user.email, user=old_user)
        logging.info(f"Updated user with email {old_user.email}")

        return users_db_accessor_pb2.UpdateUserResponse(
            bool=True, message="User updated", headers=(("internal-status", "200"),)
        )
    except Exception as e:
        logging.error(f"Error updating user: {str(e)}")
        return InvokeMethodResponse(
            data=b'{"error": "Internal error"}',
            content_type="application/json",
            headers=(("internal-status", "500"),),
        )


@app.method(name="DeleteUser")
async def DeleteUser(request):
    try:
        logging.info("Deleting user")
        request_proto = users_db_accessor_pb2.ByIdRequest()
        request_proto.ParseFromString(request.data)
        user = await users_db_accessor.get_user_by_id(request_proto.user_id)
        if not user:
            logging.error("User not found")
            return InvokeMethodResponse(
                data=b'{"error": "User not found"}',
                content_type="application/json",
                headers=(("internal-status", "404"),),
            )
        await users_db_accessor.delete_user_by_id(user_id=user.user_id)
        logging.info(f"Deleted user with id {user.user_id}")
        return users_db_accessor_pb2.DeleteUserResponse(
            bool=True, message="User deleted", headers=(("internal-status", "200"),)
        )
    except Exception as e:
        logging.error(f"Error deleting user: {str(e)}")
        return InvokeMethodResponse(
            data=b'{"error": "Internal error"}',
            content_type="application/json",
            headers=(("internal-status", "500"),),
        )


@app.method(name="DeleteUserByEmail")
async def DeleteUserByEmail(request):
    try:
        logging.info("Deleting user by email")
        request_proto = users_db_accessor_pb2.ByEmailRequest()
        request_proto.ParseFromString(request.data)
        user = await users_db_accessor.get_user_by_email(request_proto.email)
        if not user:
            logging.error("User not found")
            return InvokeMethodResponse(
                data=b'{"error": "User not found"}',
                content_type="application/json",
                headers=(("internal-status", "404"),),
            )
        if user.password != request_proto.password:
            logging.error(f"Invalid password for user {user.email}")
            return users_db_accessor_pb2.DeleteUserResponse(
                message=f"Invalid password for user {user.email}", headers=(("internal-status", "401"),)
            )
        await users_db_accessor.delete_user_by_email(email=user.email)
        logging.info(f"Deleted user with email {user.email}")
        return users_db_accessor_pb2.DeleteUserResponse(
            bool=True, message="User deleted", headers=(("internal-status", "200"),)
        )
    except Exception as e:
        logging.error(f"Error deleting user: {str(e)}")
        return InvokeMethodResponse(
            data=b'{"error": "Internal error"}',
            content_type="application/json",
            headers=(("internal-status", "500"),),
        )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting server...")
    app.run(50052)
    logging.info("Started server")
