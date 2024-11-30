from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import dotenv
import os
import logging


logger = logging.getLogger(__name__)
dotenv.load_dotenv()


def send_email(to_email, subject, body):
    """
    Sends an email using SendGrid's API.

    :param to_email: Recipient's email address.
    :param subject: Subject of the email.
    :param body: HTML content of the email.
    """
    message = Mail(
        from_email=os.getenv("SENDER_EMAIL"),
        to_emails=to_email,
        subject=subject,
        html_content=body,
    )

    try:
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        response = sg.send(message)
        logger.info(f"Email sent successfully to {to_email}.")
        logger.info(f"Response: {response.status_code, response.body}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return False


# import requests
# from config import MAILGUN_API_KEY, MAILGUN_DOMAIN, EMAIL_USER
#
#
# def send_email(to_email, subject, body):
#     """
#     Sends an email using Mailgun's API.
#
#     :param to_email: Recipient's email address.
#     :param subject: Subject of the email.
#     :param body: HTML content of the email.
#     """
#     # Prepare the Mailgun API endpoint
#     mailgun_url = f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages"
#
#     # Prepare the email payload
#     data = {
#         "from": "Excited User <mailgun@sandbox29ed736ece854d0e98a218d82a691b24.mailgun.org>",  # Example: "you@yourdomain.com"
#         "to": to_email,
#         "subject": subject,
#         "html": body,
#     }
#
#     # Make the API call
#     response = requests.post(
#         "https://api.mailgun.net/v3/sandbox29ed736ece854d0e98a218d82a691b24.mailgun.org/messages",
#         auth=("api", "8cddb1c8851eb6e9538ba4fc37a5a5cb-6df690bb-9ba5abfb"),
#         data=data,
#     )
#
#     # Check for success
#     if response.status_code == 200:
#         print(f"Email sent successfully to {to_email}.")
#         return True
#     else:
#         print(f"Failed to send email: {response.status_code} - {response.text}")
#         return False
#
#
# def send_simple_message():
#     return requests.post(
#         "https://api.mailgun.net/v3/sandbox29ed736ece854d0e98a218d82a691b24.mailgun.org/messages",
#         auth=("api", "8cddb1c8851eb6e9538ba4fc37a5a5cb-6df690bb-9ba5abfb"),
#         data={
#             "from": "Excited User <mailgun@sandbox29ed736ece854d0e98a218d82a691b24.mailgun.org>",
#             "to": ["oht862@gmail.com"],
#             "subject": "Hello world",
#             "text": "Testing some Mailgun awesomeness!",
#         },
#     )
#
#
# if __name__ == "__main__":
#     to_email = "oht862@gmail.com"
#     subject = "Hello from Mailgun!"
#     body = (
#         "<h1>Welcome to Our Service</h1><p>This is a sample email sent via Mailgun.</p>"
#     )
#
#     send_email(to_email, subject, body)
#     # send_simple_message()
