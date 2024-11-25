from dapr.ext.grpc import App, InvokeMethodResponse
from email_formatter import format_email_content
from email_sender import send_email
import json
import dotenv
import os
app = App()


@app.method(name="send-email")
def send_email_route(request):
    try:
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
            return InvokeMethodResponse(
                data=json.dumps({"status": "success"}).encode("utf-8"),
                headers=(("internal-status", "200"),),
            )
        else:
            return InvokeMethodResponse(
                data=json.dumps(
                    {"status": "error", "message": "Failed to send email"}
                ).encode("utf-8"),
                headers=(("internal-status", "500"),),
            )

    except Exception as e:
        return InvokeMethodResponse(
            data=json.dumps({"status": "error", "message": str(e)}).encode("utf-8"),
            headers=(("internal-status", "500"), ("internal-error", str(e))),
        )


if __name__ == "__main__":
    app.run(50055)
