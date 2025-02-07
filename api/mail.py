
from django.conf import settings
from django.core import mail
from django.core.mail import EmailMessage

from typing import Sequence, List


def send_email(subject: str, email_body: str, recipients: Sequence[str], sender_email=settings.EMAIL_HOST_USER,):
        """Util function to send mail"""
        email = EmailMessage(subject, body=email_body, from_email=sender_email, to=recipients)
        email.send()
