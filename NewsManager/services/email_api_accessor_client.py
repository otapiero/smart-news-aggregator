import logging
from dapr.clients import DaprClient
import json


class AsyncHTTPEmailAPIClient:
    def __init__(self, app_id):
        self.logger = logging.getLogger(__name__)
        self.client = DaprClient()
        self.app = app_id

    def send_news(self, email, news):
        try:
            self.logger.info(f"Sending news to {email}")
            data = {"email": email, "news": news}
            response = self.client.invoke_method(
                app_id="email_api_accessor",
                method_name="send-email",
                data=json.dumps(data).encode("utf-8"),
                content_type="application/json",
            )
            if response.status_code == 200:
                self.logger.info(f"News sent successfully to {email}")
                return True
            else:
                self.logger.error(f"Failed to send news to {email}: {response.text()}")
                return False
        except Exception as e:
            self.logger.error(f"Error sending news: {e}")
            return False
