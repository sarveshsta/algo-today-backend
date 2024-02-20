from twilio.rest import Client
from algo.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core import mail


def send_otp(otp, to_number):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    client.messages.create(
            body = f'Greetings, your OTP for Algo-Today is {otp}. Please do not share it with anyone.',
            from_= '+12136529736',
            to = '+91' + str(to_number)
        )


# def reset_passwordMail(to_email, otp):
#     subject = 'Account Verification'
#     from_email = 'Growatpace <info@growatpace.com>'
#     to = to_email
#     subject = "Password Reset Requested"
#     email_template_name = "email/password_reset_otp.txt"
#     c = {
#         "otp": otp
#     }
#     email = render_to_string(email_template_name, c)
#     mail.send_mail(subject, strip_tags(email), from_email, [to])
#     return True


