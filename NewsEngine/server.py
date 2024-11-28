from flask import Flask, request, jsonify
from services.news_api_accessor_client import AsyncGRPCNewsApiClient
from services.llm_api_accessor_client import AsyncGRPCLLMApiClient
import logging
import asyncio

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Clients for News API Accessor and LLM API Accessor
news_api_client = AsyncGRPCNewsApiClient("newsapi_accessor")
llm_api_client = AsyncGRPCLLMApiClient("llm_summarization_accessor")


@app.route("/get-fresh-news", methods=["GET"])
async def get_fresh_news():
    try:
        logger.info("Received request for fresh news...")
        preferences = request.json
        categories = preferences.get("categories", [])
        language = preferences.get("language", "en")
        country = preferences.get("country", "us")

        # Step 1: Fetch raw news from News API Accessor
        raw_news = await news_api_client.get_news_by_categories(
            categories, language, country
        )
        if not raw_news:
            return jsonify({"status": "error", "message": "No news found"}), 404

        logger.info("Fetched raw news. Sending for summarization...")

        # Step 2: Summarize news using LLM API Accessor
        summarized_news = await llm_api_client.summarize(raw_news)
        logger.info(f"len of summarized_news: {len(summarized_news)}")
        logger.info("Summarized news successfully. Returning to News Manager.")
        return jsonify({"status": "success", "data": summarized_news}), 200

    except Exception as e:
        logger.error(f"Error in get_fresh_news: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
