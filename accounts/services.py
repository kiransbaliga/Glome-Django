from django.utils.safestring import mark_safe
import threading
from django.conf import settings
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError, EmailMessage

class EmailThread(threading.Thread):
    def __init__(self, subject, body, to_email, content_subtype=None, *args, **kwargs):
        self.subject = subject
        self.to_email = [to_email,]
        self.body = body
        self.content_subtype = content_subtype
        threading.Thread.__init__(self)

    def run(self, *args, **kwargs):
        msg = EmailMessage(
            self.subject,
            self.body,
            settings.DEFAULT_FROM_EMAIL,
            self.to_email,
            *args,
            **kwargs
        )
        if self.content_subtype is not None:
            msg.content_subtype = self.content_subtype
        try:
            msg.send()
            print("Email send: " + self.to_email[0])
        except BadHeaderError:
            print("Invalid header found")


class EmailService:
    @classmethod
    def send_otp_to_user(cls,user):
        EmailThread(
            subject="Please verify your email",
            body=f'Hello your OTP is {user.otp}.\n\n You OTP is valid for {settings.OTP_VALIDITY_MINS} mins',
            to_email=user.email
        ).start()
        