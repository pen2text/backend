from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from utils.email_utils import send_verification_email
from user_management.models import Users


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(email=email, password=password)
        
        if not user:
            raise serializers.ValidationError({'user': 'Wrong email or password.'})
        
        if not user.is_verified:
            send_verification_email(user)
            raise serializers.ValidationError({'user': 'Please verify your email address, email has been sent.'})
        
        refresh = RefreshToken.for_user(user)
        refresh['email'] = user.email
        refresh['role'] = user.role
        
        response_data = {
            'status': 'OK',
            'message': 'User logged in successfully.',
            'data':{
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
            }
        }
        return response_data

class ResetPasswordSerializer(serializers.ModelSerializer):
    token = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    class Meta:
        model = Users
        fields = ['token', 'password']
    

