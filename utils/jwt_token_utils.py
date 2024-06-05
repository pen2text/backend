import os
import jwt
import datetime
from remote_handler.models import RemoteAPITokenManagers
from user_management.models import Users
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


SECRET_KEY = os.getenv('SECRET_KEY')

def generate_jwt_token(payload, expiry_minutes=60):

    # Calculate expiry time
    expiry_time = datetime.datetime.now() + datetime.timedelta(minutes=expiry_minutes)
    
    # Add expiry time to payload
    payload['exp'] = expiry_time
    
    # Generate JWT token
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    
    return token

    
def verify_token(token, token_type):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = decoded_token['id']
        user = Users.objects.filter(id=user_id).first()
        
        if not user or token_type != decoded_token['token_type']:
            raise ValueError("Token get expired or invalid token, please request a new one.")
        
        if token_type == 'pen2text-api-key':
            if RemoteAPITokenManagers.objects.filter(user=user, token=token).first() is None:
                raise ValueError("Token get expired or invalid token, please request a new one.")
            
        return user
    except Exception as e:
        raise ValueError(e)


class PrivateKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        private_key = request.headers.get('PEN-TEXT-API-KEY')

        if not private_key:
            return None

        try:
            user = verify_token(private_key, "pen2text-api-key")
        except Exception as e:
            raise AuthenticationFailed(str(e))

        return (user, None)