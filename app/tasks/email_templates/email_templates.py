from app.database import settings
import smtplib


class EmailTemplate:
    @classmethod
    def sent_message_confirmation(cls, func, *args, **kwargs):
        message = func(*args, **kwargs)
        with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.login(settings.SMTP_USER, settings.SMTP_PASS)
            server.send_message(message)
