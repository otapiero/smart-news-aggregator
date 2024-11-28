from flask import Flask, request, jsonify
from dapr.clients import DaprClient
import logging
import json

from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
dapr_client = DaprClient()


@app.route("/users", methods=["POST", "GET", "PUT", "DELETE"])
def manage_users():
    """Handles CRUD operations for users."""
    try:
        # Route the request based on the method
        if request.method == "POST":
            logger.info("Creating a new user")
            data = request.json
            response = dapr_client.invoke_method(
                app_id=Config.USERS_MANAGER_APP_ID,
                method_name="CreateUser",
                content_type="application/json",
                data=json.dumps(data).encode("utf-8"),
            )
        elif request.method == "GET":
            logger.info("Getting user preferences")
            response = dapr_client.invoke_method(
                app_id=Config.USERS_MANAGER_APP_ID,
                method_name="GetUserPreferencesByEmailAddress",
                content_type="application/json",
                data=json.dumps(request.json).encode("utf-8"),
            )
        elif request.method == "PUT":
            logger.info("Updating a user")
            response = dapr_client.invoke_method(
                app_id=Config.USERS_MANAGER_APP_ID,
                method_name="UpdateUserByEmail",
                content_type="application/json",
                data=json.dumps(request.json).encode("utf-8"),
            )
        elif request.method == "DELETE":
            logger.info("Deleting a user")
            response = dapr_client.invoke_method(
                app_id=Config.USERS_MANAGER_APP_ID,
                method_name="DeleteUserByEmail",
                content_type="application/json",
                data=json.dumps(request.json).encode("utf-8"),
            )
        else:
            return jsonify({"error": "Unsupported HTTP method"}), 405

        # Return the response from the backend service
        return jsonify(response.json()), response.status_code

    except Exception as e:
        logger.error(f"Error managing users: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


@app.route("/news", methods=["POST"])
def get_news():
    """Handles requests to fetch news."""
    try:
        logger.info("Fetching news")
        response = dapr_client.invoke_method(
            app_id=Config.NEWS_MANAGER_APP_ID,
            method_name="get-news",
            content_type="application/json",
            data=json.dumps(request.json).encode("utf-8"),
        )
        return jsonify(response.json()), response.status_code
    except Exception as e:
        logger.error(f"Error fetching news: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


if __name__ == "__main__":
    logger.info("Starting BFF...")
    app.run(host="0.0.0.0", port=5003)
