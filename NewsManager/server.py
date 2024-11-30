from dapr.ext.grpc import App
from news_service import NewsService
from config import Config
import logging
import json


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = App()
news_service = NewsService()


@app.binding(name="newsqueue")
def newsqueue(request):
    logger.info("Getting news...")
    try:
        data_request = json.loads(request.data.decode("utf-8"))

        email = data_request.get("email")
        password = data_request.get("password")
        logger.info(f"Email: {email}")

        if not email or not password:
            logger.error("Email or password not provided")
            return

        # Call the service layer to handle the operation flow
        response = news_service.handle_get_news(email, password)
        if response["status"] == "error":
            logger.error(f"Error getting news: {response['message']}")
            return

        logger.info("successfully sent news")

        return

    except Exception as e:
        logger.error(f"Error processing get-news request: {e}")
        return


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger.info("Starting server...")
    app.run(Config.APP_PORT)
