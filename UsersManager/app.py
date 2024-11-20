from dapr.ext.grpc import App, InvokeMethodResponse

import config
from engine import UserManagerEngine
from dto import UserDTO
import logging
import json
from http import HTTPStatus

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = App()
engine = UserManagerEngine()


def create_response(
    data: dict, status_code: int = HTTPStatus.OK
) -> InvokeMethodResponse:
    """Create a standardized response"""
    return InvokeMethodResponse(
        data=json.dumps(data).encode("utf-8"),
        content_type="application/json",
        headers=(("internal-status", str(status_code)),),
    )


def create_error_response(
    message: str, status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR
) -> InvokeMethodResponse:
    """Create a standardized error response"""
    return create_response({"error": message}, status_code)


@app.method(name="CreateUser")
async def create_user(request):
    try:
        user_data = json.loads(request.data)
        user_dto = UserDTO(**user_data)
        response = engine.create_user(user_dto)
        if "error" in response:
            return create_error_response(
                response["error"], response.get("status_code", HTTPStatus.BAD_REQUEST)
            )
        return create_response(response, HTTPStatus.CREATED)
    except Exception as e:
        logger.error(f"Error in CreateUser: {str(e)}", exc_info=True)
        return create_error_response(f"Internal error: {str(e)}")


@app.method(name="GetUserPreferencesByEmailAddress")
async def get_user_preferences(request):
    try:
        request_data = json.loads(request.data)
        email = request_data.get("email")
        password = request_data.get("password")
        response = engine.get_user_preferences(email, password)
        if "error" in response:
            return create_error_response(
                response["error"], response.get("status_code", HTTPStatus.BAD_REQUEST)
            )
        return create_response(response, HTTPStatus.OK)
    except Exception as e:
        logger.error(
            f"Error in GetUserPreferencesByEmailAddress: {str(e)}", exc_info=True
        )
        return create_error_response(f"Internal error: {str(e)}")


@app.method(name="UpdateUserByEmail")
async def update_user_by_email(request):
    try:
        request_data = json.loads(request.data)
        user_data = request_data.get("user")
        old_email = request_data.get("email")
        old_password = request_data.get("password")

        if not user_data or not old_email or not old_password:
            return create_error_response("Invalid request data", HTTPStatus.BAD_REQUEST)

        user_dto = UserDTO(**user_data)
        response = engine.update_user_by_email(user_dto, old_email, old_password)
        if "error" in response:
            return create_error_response(
                response["error"], response.get("status_code", HTTPStatus.BAD_REQUEST)
            )
        return create_response(response, HTTPStatus.OK)
    except Exception as e:
        logger.error(f"Error in UpdateUserByEmail: {str(e)}", exc_info=True)
        return create_error_response(f"Internal error: {str(e)}")


@app.method(name="DeleteUserByEmail")
async def delete_user_by_email(request):
    try:
        request_data = json.loads(request.data)
        email = request_data.get("email")
        password = request_data.get("password")

        if not email or not password:
            return create_error_response("Invalid request data", HTTPStatus.BAD_REQUEST)

        response = engine.delete_user_by_email(email, password)
        if "error" in response:
            return create_error_response(
                response["error"], response.get("status_code", HTTPStatus.BAD_REQUEST)
            )
        return create_response(response, HTTPStatus.OK)
    except Exception as e:
        logger.error(f"Error in DeleteUserByEmail: {str(e)}", exc_info=True)
        return create_error_response(f"Internal error: {str(e)}")


if __name__ == "__main__":
    logger.info("Starting Users Manager Service...")
    app.run(config.APP_PORT)
