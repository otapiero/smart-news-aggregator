from dapr.ext.grpc import App, InvokeMethodResponse, InvokeMethodRequest

from news_db_accessor import NewsDBAccessor
import logging
import json

logger = logging.getLogger(__name__)


app = App()
news_db_accessor = NewsDBAccessor()


@app.method(name="get_news")
def get_news(request: InvokeMethodRequest) -> InvokeMethodResponse:
    try:
        request_data = request.data.decode("utf-8")
        request_json = json.loads(request_data)
        language = request_json.get("language", "english")
        country = request_json.get("country", "us")
        categories = request_json.get("categories", [])
        logger.info(
            f"Fetching news for language: {language}, country: {country}, categories: {categories}"
        )
        news = {}
        for category in categories:
            news[category] = get_news_by_category(category, language, country)
            logger.info(
                f"Fetched {len(news[category])} articles for category: {category}"
            )

        response_data = {"status": "success", "data": news}

        return InvokeMethodResponse(
            json.dumps(response_data).encode("utf-8"), "application/json"
        )
    except Exception as e:
        logger.error(f"Error fetching news: {e}")
        return InvokeMethodResponse(
            json.dumps({"status": "error", "message": str(e)}).encode("utf-8"),
            "application/json",
        )


def get_news_by_category(category, language, country):
    try:
        logger.info(
            f"Fetching news for category: {category}, language: {language}, country: {country}"
        )
        news = news_db_accessor.get_news(
            category=category, language=language, country=country
        )
        return news
    except Exception as e:
        logger.error(f"Error fetching news: {e}")
        return []


@app.method(name="update_news")
def update_news(request: InvokeMethodRequest) -> InvokeMethodResponse:
    try:
        request_data = request.data.decode("utf-8")
        request_json = json.loads(request_data)
        language = request_json["language"]
        country = request_json["country"]
        category = request_json["category"]
        new_articles = request_json["articles"]
        update_news_by_category(category, language, country, new_articles)
        response_data = {"status": "success", "message": "News updated successfully."}
        return InvokeMethodResponse(
            json.dumps(response_data).encode("utf-8"), "application/json"
        )
    except KeyError as e:
        logger.error(f"Missing required field in update request: {e}")
        return InvokeMethodResponse(
            json.dumps(
                {"status": "error", "message": f"Missing required field: {e}"}
            ).encode("utf-8"),
            "application/json",
        )
    except Exception as e:
        logger.error(f"Error updating news: {e}")
        return InvokeMethodResponse(
            json.dumps({"status": "error", "message": str(e)}).encode("utf-8"),
            "application/json",
        )


def update_news_by_category(category, language, country, news):
    try:
        logger.info(
            f"Updating news for category: {category}, language: {language}, country: {country}"
        )
        news_db_accessor.update_news(
            category=category,
            language=language,
            country=country,
            new_articles=news,
        )
    except Exception as e:
        logger.error(f"Error updating news: {e}")


def main():
    logging.basicConfig(level=logging.INFO)
    logger.info("Starting News DB Accessor service...")
    app.run(50058)


if __name__ == "__main__":
    main()
