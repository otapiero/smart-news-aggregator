from dapr.ext.grpc import App, InvokeMethodResponse, InvokeMethodRequest
import logging
import asyncio
import os
import json
from dotenv import load_dotenv

from news_connector import NewsApiConnector
from news_api_config import NewsApiConfig

load_dotenv()

app = App()
news_api_connector = NewsApiConnector(api_key=os.getenv("NEWS_API_AI_API_KEY"))

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


@app.method(name="get_news")
def get_news(request):
    try:
        request_data = request.data.decode("utf-8")
        request_json = json.loads(request_data)
        language = request_json.get("language", "english")
        country = request_json.get("country", "us")
        category = request_json.get("category", "")
        logging.info(
            f"Getting news for language: {language}, country: {country}, category: {category}"
        )
        news = news_api_connector.get_news(
            language=language, country=country, category=category
        )
        response = json.dumps({"status": "success", "data": news}).encode("utf-8")
        return InvokeMethodResponse(
            data=response,
            content_type="application/json",
            headers=(("internal-status", "200"),),
        )
    except json.JSONDecodeError as e:
        logging.error(f"JSON Decode Error: {e}")
        error_response = json.dumps(
            {"status": "error", "message": "Invalid JSON"}
        ).encode("utf-8")
        return InvokeMethodResponse(
            data=error_response,
            content_type="application/json",
            headers=(("internal-status", "400"), ("internal-error", str(e))),
        )
    except Exception as e:
        logging.error(f"Error getting news: {e}")
        error_response = json.dumps({"status": "error", "message": str(e)}).encode(
            "utf-8"
        )
        return InvokeMethodResponse(
            data=error_response,
            headers=(
                ("internal-status", "500"),
                ("internal-error", str(e)),
            ),
        )


@app.method(name="get_news_by_topic")
def get_news_by_topic(request):
    try:
        request_json = json.loads(request.data.decode("utf-8"))
        topic = request_json.get("topic")
        language = request_json.get("language", "english")
        country = request_json.get("country", "us")
        logging.info(
            f"Getting news for topic: {topic}, language: {language}, country: {country}"
        )
        news = news_api_connector.get_news_by_topic(
            topic=topic, language=language, country=country
        )
        response = json.dumps({"status": "success", "data": news}).encode("utf-8")
        return InvokeMethodResponse(
            data=response,
            headers=(("internal-status", "200"),),
            content_type="application/json",
        )
    except json.JSONDecodeError as e:
        logging.error(f"JSON Decode Error: {e}")
        error_response = json.dumps(
            {"status": "error", "message": "Invalid JSON"}
        ).encode("utf-8")
        return InvokeMethodResponse(
            data=error_response,
            content_type="application/json",
            headers=(("internal-status", "400"), ("internal-error", str(e))),
        )
    except Exception as e:
        logging.error(f"Error getting news by topic: {e}")
        error_response = json.dumps({"status": "error", "message": str(e)}).encode(
            "utf-8"
        )
        return InvokeMethodResponse(
            data=error_response,
            headers=(
                ("internal-status", "500"),
                ("internal-error", str(e)),
            ),
        )


@app.method(name="get_news_by_categories")
def get_news_by_categories(request):
    try:
        logging.info("Getting news for categories")
        request_json = json.loads(request.data.decode("utf-8"))
        categories = request_json.get("categories", [])
        language = request_json.get("language", "english")
        country = request_json.get("country", "us")
        logging.info(
            f"Getting news for categories: {categories}, language: {language}, country: {country}"
        )
        news = news_api_connector.get_news_by_categories(
            categories=categories, language=language, country=country
        )
        response = json.dumps({"status": "success", "data": news}).encode("utf-8")
        return InvokeMethodResponse(
            data=response,
            headers=(("internal-status", "200"),),
            content_type="application/json",
        )

    except json.JSONDecodeError as e:
        logging.error(f"JSON Decode Error: {e}")
        error_response = json.dumps(
            {"status": "error", "message": "Invalid JSON"}
        ).encode("utf-8")
        return InvokeMethodResponse(
            data=error_response,
            content_type="application/json",
            headers=(("internal-status", "400"), ("internal-error", str(e))),
        )
    except Exception as e:
        logging.error(f"Error getting news by categories: {e}")
        error_response = json.dumps({"status": "error", "message": str(e)}).encode(
            "utf-8"
        )
        return InvokeMethodResponse(
            data=error_response,
            headers=(
                ("internal-status", "500"),
                ("internal-error", str(e)),
            ),
        )


@app.method(name="get_available_options")
def get_available_options(request):
    try:
        logging.info("Getting available options")
        options = NewsApiConfig.get_available_options()
        response = json.dumps({"status": "success", "data": options}).encode("utf-8")
        return InvokeMethodResponse(
            data=response,
            headers=(("internal-status", "200"),),
            content_type="application/json",
        )

    except json.JSONDecodeError as e:
        logging.error(f"JSON Decode Error: {e}")
        error_response = json.dumps(
            {"status": "error", "message": "Invalid JSON"}
        ).encode("utf-8")
        return InvokeMethodResponse(
            data=error_response,
            content_type="application/json",
            headers=(("internal-status", "400"), ("internal-error", str(e))),
        )
    except Exception as e:
        logging.error(f"Error getting available options: {e}")
        error_response = json.dumps({"status": "error", "message": str(e)}).encode(
            "utf-8"
        )
        return InvokeMethodResponse(
            data=error_response,
            headers=(
                ("internal-status", "500"),
                ("internal-error", str(e)),
            ),
        )


@app.method(name="health")
def health():
    return InvokeMethodResponse(
        data=json.dumps({"status": "ok"}).encode("utf-8"),
        content_type="application/json",
        headers=(("internal-status", "200"),),
    )


if __name__ == "__main__":

    logging.info("Starting NewsApiAccessor app...")
    try:
        app.run(50052)
    except KeyboardInterrupt:
        logging.info("Shutting down gracefully...")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
