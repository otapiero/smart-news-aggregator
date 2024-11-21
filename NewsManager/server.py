from flask import Flask, request, jsonify
from news_service import NewsService
from config import Config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = Flask(__name__)

news_service = NewsService()


@app.route(
    "/get-news", methods=["POST"]
)
async def get_news():
    logger.info("Getting news...")
    try:
        data = request.json
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        # Call the service layer to handle the operation flow
        response = await news_service.handle_get_news(email, password)
        return jsonify(response), 200 if response.get("status") == "success" else 500

    except Exception as e:
        logger.error(f"Error processing get-news request: {e}")
        return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger.info("Starting server...")
    app.run(host="0.0.0.0", port=Config.APP_PORT, debug=Config.DEBUG)
