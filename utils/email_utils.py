from django.core.mail import EmailMessage

def send_email(content, subject, receiver_email):
    try:
        email = EmailMessage(
            subject=subject,
            body=content,
            to=[receiver_email],
        )
        
        email.send()
        return True
    
    except Exception as e:
        print(f"An error occurred while sending the email: {e}")
        return False
