from typing import List, Dict

import google.generativeai as genai

import json
import time
from collections import deque
import typing_extensions
import logging


class Article(typing_extensions.TypedDict):
    title: str
    body: str


class RateLimiter:
    def __init__(self, max_requests_per_minute: int, max_requests_per_day: int):
        self.max_requests_per_minute = max_requests_per_minute
        self.max_requests_per_day = max_requests_per_day
        self.minute_requests = deque()  # Tracks requests within the last minute
        self.day_requests = deque()  # Tracks requests within the last 24 hours

    def can_make_request(self) -> bool:
        current_time = time.time()

        # Remove expired requests (older than 1 minute for minute tracking)
        while self.minute_requests and current_time - self.minute_requests[0] > 60:
            self.minute_requests.popleft()

        # Remove expired requests (older than 24 hours for daily tracking)
        while self.day_requests and current_time - self.day_requests[0] > 86400:
            self.day_requests.popleft()

        if (
            len(self.minute_requests) < self.max_requests_per_minute
            and len(self.day_requests) < self.max_requests_per_day
        ):
            self.minute_requests.append(current_time)
            self.day_requests.append(current_time)
            return True

        return False

    def remaining_requests(self) -> Dict[str, int]:
        return {
            "minute_remaining": self.max_requests_per_minute
            - len(self.minute_requests),
            "daily_remaining": self.max_requests_per_day - len(self.day_requests),
        }


class LLMApiAccessor:
    def __init__(
        self,
        api_key: str,
        max_requests_per_minute: int = 14,
        max_requests_per_day: int = 1400,
    ):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash-latest")
        self.rate_limiter = RateLimiter(max_requests_per_minute, max_requests_per_day)
        self.logger = logging.getLogger(__name__)

    def summarize_articles(self, articles: List[Dict]) -> List[Dict]:
        if not self.rate_limiter.can_make_request():
            self.logger.error("Rate limit exceeded. Please try again later.")
            raise RuntimeError("Rate limit exceeded. Please try again later.")
        batched_prompt = self._create_batch_prompt(articles)
        self.logger.info(f"Summarizing {len(articles)} articles in one request.")

        result = self.model.generate_content(
            batched_prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json", response_schema=list[Article]
            ),
        )
        self.logger.info(f"Result: {result.text}")
        summaries = self._split_summaries(result.text)
        remaining_requests = self.rate_limiter.remaining_requests()
        self.logger.info(
            f"Remaining requests: per minute: {remaining_requests['minute_remaining']}, per day: {remaining_requests['daily_remaining']}"
        )

        return summaries

    def _create_batch_prompt(self, articles: List[Dict]) -> str:
        """Create a single prompt combining all articles for batch processing."""
        batched_prompt = "\n\n".join(
            f"Article {i+1}:\n{article['body']}" for i, article in enumerate(articles)
        )
        return f"""Given the following articles content:
                {batched_prompt}
                Tasks:
                for each article separately:
                1. Summarize the content of the article into a very short concise paragraph.
                2. Generate a short title for each article separately."""

    def _split_summaries(self, response_text: str) -> List[Dict]:
        """
        Process the result of the API response if it returns a structured list of articles.
        """
        try:
            summaries = json.loads(response_text)
            if not isinstance(summaries, list):
                raise ValueError("Response is not a list of summaries as expected.")
            return summaries
        except json.JSONDecodeError as e:
            self.logger.error(f"Error decoding response: {response_text}. Error: {e}")
            raise RuntimeError("Failed to decode the API response.")
        except ValueError as e:
            self.logger.error(
                f"Unexpected response format: {response_text}. Error: {e}"
            )
            raise RuntimeError("Invalid API response format.")
