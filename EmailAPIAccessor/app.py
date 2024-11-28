from dapr.ext.grpc import App, InvokeMethodResponse
from email_formatter import format_email_content
from email_sender import send_email
import json
import logging
import dotenv
import os

logger = logging.getLogger(__name__)
app = App()


@app.method(name="send-email")
def send_email_route(request):
    try:
        logger.info("Received request to send email...")
        request_data = json.loads(request.data.decode("utf-8"))
        email = request_data.get("email", "")
        articles = request_data.get("news", [])

        if not email or not articles:
            return InvokeMethodResponse(
                data=json.dumps(
                    {"status": "error", "message": "Invalid request"}
                ).encode("utf-8"),
                headers=(("internal-status", "400"),),
            )

        # Format the email content
        email_content = format_email_content(articles)

        # Send the email
        success = send_email(email, "Your Personalized News", email_content)

        if success:
            logger.info("Email sent successfully.")
            return InvokeMethodResponse(
                data=json.dumps({"status": "success"}).encode("utf-8"),
                headers=(("internal-status", "200"),),
            )
        else:
            logger.info("Failed to send email.")
            return InvokeMethodResponse(
                data=json.dumps(
                    {"status": "error", "message": "Failed to send email"}
                ).encode("utf-8"),
                headers=(("internal-status", "500"),),
            )

    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return InvokeMethodResponse(
            data=json.dumps({"status": "error", "message": str(e)}).encode("utf-8"),
            headers=(("internal-status", "500"), ("internal-error", str(e))),
        )


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    dotenv.load_dotenv()
    logger.info("Starting server...")
    app.run(50055)
    logger.info("Server stopped.")
