import os
import jwt
import datetime
from user_management.models import User
SECRET_KEY = os.getenv('SECRET_KEY')
EXPIRY_MINUTES = 60

def generate_jwt_token(payload):

    # Calculate expiry time
    expiry_time = datetime.datetime.now() + datetime.timedelta(minutes=EXPIRY_MINUTES)
    
    # Add expiry time to payload
    payload['exp'] = expiry_time
    
    # Generate JWT token
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    
    return token

    
def verify_token(token):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_email = decoded_token['email']
        
        user = User.objects.filter(email=user_email).first()
        if not user:
            raise ValueError("Invalid token")
        return user
    
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")