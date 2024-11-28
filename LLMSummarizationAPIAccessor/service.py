from typing import List, Dict
from dapr.ext.grpc import App, InvokeMethodResponse
import logging
import os
import json
from dotenv import load_dotenv
from llm_accessor import LLMApiAccessor
from news_article import NewsArticle

load_dotenv()

app = App()
llm_api_accessor = LLMApiAccessor(
    api_key=os.getenv("GENERATIVE_API_KEY"),
    max_requests_per_minute=14,
    max_requests_per_day=1400,
)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@app.method(name="summarize")
def summarize(request) -> InvokeMethodResponse:
    try:
        logger.info("Received request to summarize articles...")
        request_data = parse_request_data(request)

        summarized_articles = process_articles(request_data)

        response = create_success_response(summarized_articles)
        logger.info("Summarized articles successfully.")
        return response

    except json.JSONDecodeError as e:
        return handle_error(
            f"JSON Decode Error: {e}",
            {"status": "error", "message": "Invalid JSON format."},
            400,
        )
    except RuntimeError as e:
        return handle_error(
            f"Rate limit exceeded: {e}",
            {
                "status": "error",
                "message": "Rate limit exceeded. Please wait and try again later.",
            },
            429,
        )
    except Exception as e:
        return handle_error(
            f"Error summarizing articles: {e}",
            {"status": "error", "message": str(e)},
            500,
        )


def parse_request_data(request) -> Dict[str, List[dict]]:
    """Parse and decode the incoming request data."""
    request_data = request.data.decode("utf-8")
    return json.loads(request_data)


def process_articles(request_data: Dict[str, List[dict]]) -> Dict[str, List[dict]]:
    """Process and summarize articles by category."""
    summarized_articles = {}

    for category, articles in request_data.items():
        logger.info(f"Summarizing articles for category: {category}")

        articles_to_summarize = [
            NewsArticle.from_dict(article).to_dict_for_llm() for article in articles
        ]
        summarized_data = llm_api_accessor.summarize_articles(articles_to_summarize)

        summarized_articles[category] = update_articles_with_summary(
            articles, summarized_data
        )

    return summarized_articles


def update_articles_with_summary(original_articles, summarized_data):
    """Combine original articles with summaries."""
    return [
        NewsArticle(
            title=summary["title"],
            body=summary["body"],
            image=original_article["image"],
            url=original_article["url"],
            dateTimePub=original_article["dateTimePub"],
            category=original_article["category"],
        ).to_dict()
        for original_article, summary in zip(original_articles, summarized_data)
    ]


def create_success_response(data: Dict) -> InvokeMethodResponse:
    """Create a success response."""
    logger.info("Creating success response...")
    response = json.dumps({"status": "success", "data": data}).encode("utf-8")
    return InvokeMethodResponse(data=response, content_type="application/json")


def handle_error(
    log_message: str, response_data: Dict, status_code: int
) -> InvokeMethodResponse:
    """Log an error and return an error response."""
    logger.error(log_message)
    error_response = json.dumps(response_data).encode("utf-8")
    return InvokeMethodResponse(
        data=error_response,
        content_type="application/json",
        headers=(("internal-status", str(status_code)),),
    )


if __name__ == "__main__":
    logger.info("Starting LLM summarization service...")
    try:
        app.run(50054)
    except KeyboardInterrupt:
        logging.info("Shutting down gracefully...")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
