from rest_framework import serializers
from user_management.models import User

class ResetPasswordSerializer(serializers.ModelSerializer):
    token = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ['token', 'password']
    
