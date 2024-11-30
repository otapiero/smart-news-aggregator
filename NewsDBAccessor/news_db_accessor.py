import redis
import json
from datetime import datetime


class NewsDBAccessor:
    def __init__(self, redis_host="redis", redis_port=6379, max_articles=10):
        self.max_articles = max_articles
        self.client = redis.StrictRedis(
            host=redis_host, port=redis_port, decode_responses=True
        )

    def _get_news_key(self, category, language, country):
        return f"news:{category}:{language}:{country}"

    def update_news(self, category, language, country, new_articles):
        try:
            key = self._get_news_key(category, language, country)
            now = datetime.now().timestamp()

            # Add new articles
            for article in new_articles:
                self.client.zadd(key, {json.dumps(article): now})

            # Ensure we only keep the 10 most recent articles
            excess_count = self.client.zcard(key) - self.max_articles
            if excess_count > 0:
                self.client.zpopmin(key, excess_count)
        except Exception as e:
            raise Exception(f"Error updating news: {e}")

    def get_news(self, category, language, country):
        try:
            key = self._get_news_key(category, language, country)
            articles = self.client.zrange(key, 0, -1, withscores=True)
            return [
                {
                    "article": json.loads(article),
                    "timestamp": datetime.fromtimestamp(score).isoformat(),
                }
                for article, score in articles
            ]
        except Exception as e:
            raise Exception(f"Error fetching news: {e}")
