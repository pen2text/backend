import datetime
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from utils.jwt_token_utils import generate_jwt_token
import os

EMAIL_VERIFICATION_PATH = os.getenv('EMAIL_VERIFICATION_PATH')
FRONTEND_PASSWORD_REST_PATH = os.getenv('FRONTEND_PASSWORD_REST_PATH')

def send_email(html_content, subject, receiver_email):
    try:
        email = EmailMessage(
            subject = subject,
            body = html_content,
            to = [receiver_email],
        )
        
        email.content_subtype = 'html'
        email.send()
        return True
    
    except Exception as e:
        return False

def send_verification_email(user):
    payload = {
        'email': user.email,
        'id': str(user.id),
        'token_type': 'email_verification'
    }
    jwt_token = generate_jwt_token(payload)

    verification_url = EMAIL_VERIFICATION_PATH + jwt_token

    data = {
        'name': user.first_name + " " + user.last_name,
        'year': datetime.datetime.now().year,
        'date': datetime.date.today(),
        'messageType': "verification email",
        'body': "",
        'link': verification_url,
    }
    
    html_content = render_to_string('temp.html', data)
    subject = "Please Verify Your Email Address"
    receiver_email = user.email
    
    if send_email(html_content, subject, receiver_email):
        print("Email sent successfully!")
    else:
        print("Failed to send email.")

def send_reset_password_email(user):
    payload = {
        'email': user.email,
        'id': str(user.id),
        'token_type': 'password_reset'
    }
    jwt_token = generate_jwt_token(payload)
    reset_password_url = FRONTEND_PASSWORD_REST_PATH + jwt_token
    
    data = {
        'name': user.first_name + " " + user.last_name,
        'year': datetime.datetime.now().year,
        'date': datetime.date.today(),
        'messageType': "verification email",
        'body': "",
        'link': reset_password_url,
    }
    
    
    html_content = render_to_string('temp.html', data)
    subject = "Password Reset"
    receiver_email = user.email
    
    if send_email(html_content, subject, receiver_email):
        return True
    else:
        return False