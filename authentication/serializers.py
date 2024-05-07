from rest_framework import serializers, status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from user_management.models import Users
from utils.email_utils import send_email
from utils.jwt_token_utils import generate_jwt_token, verify_token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('id', 'username', 'email')

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        
        user = authenticate(email=email, password=password)
        if user:
            if not user.is_verified:
                payload = {
                    'email': user.email,
                    'id': str(user.id),
                    'token_type': 'email_verification'
                }
                jwt_token = generate_jwt_token(payload)

                # Retrieve content, subject, and receiver_email
                verification_url = f'http://localhost:8000/api/users/verify-email/{jwt_token}'
                content = "Content for email verification. " + verification_url 
                subject = "Email Verification"
                receiver_email = user.email
                
                # Send the email
                if send_email(content, subject, receiver_email):
                    print("Email sent successfully!")
                else:
                    print("Failed to send email.")
                    
                response_data = {
                    'status': 'FAILED',
                    'message': "User account isn't verified.",
                }
                raise serializers.ValidationError(response_data)
            
            refresh = RefreshToken.for_user(user)
            refresh['email'] = user.email
            refresh['role'] = user.role
            response_data = {
                'status': 'OK',
                'message': 'Successfully logged in.',
                'data':{
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                }
            }
            return response_data
        else:
            response_data = {
                'user': 'Wrong email or password.',
            }
            raise serializers.ValidationError(response_data)

class ResetPasswordSerializer(serializers.ModelSerializer):
    token = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    class Meta:
        model = Users
        fields = ['token', 'password']
    

