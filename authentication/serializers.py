from rest_framework import serializers, status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from user_management.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                if not user.is_verified:
                    response_data = {
                        'data':{
                            'status': 'error',
                            'code': status.HTTP_400_BAD_REQUEST,
                            'message': "User account isn't verified.",
                            'errors': ["User account isn't verified."],
                        }
                    }
                    raise serializers.ValidationError(response_data)
                
                refresh = RefreshToken.for_user(user)
                refresh['email'] = user.email
                refresh['role'] = user.role
                response_data = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Successfully logged in.',
                    'data':{
                        'access_token': str(refresh.access_token),
                        'refresh_token': str(refresh),
                    }
                }
                return response_data
            else:
                response_data = {
                    'data':{
                        'status': 'error',
                        'code': status.HTTP_401_UNAUTHORIZED,
                        'message': 'Wrong email or password.',
                        'errors': ['Wrong email or password.'],
                    }
                }
                raise serializers.ValidationError(response_data)
        else:
            response_data = {
                'data':{
                    'status': 'error',
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': '"email" and "password" are required.',
                    'errors': ['"email" and "password" are required.'],
                }
            }
            raise serializers.ValidationError(response_data)

class ResetPasswordSerializer(serializers.ModelSerializer):
    token = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ['token', 'password']
    

