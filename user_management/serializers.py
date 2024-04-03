import re
from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'gender', 'date_of_birth', 'email', 'role', 'password', 'is_verified', 'created_at', 'updated_at')
        extra_kwargs = {
            'password': {'write_only': True}, 
            'id': {'read_only': True},  
            'is_verified': {'read_only': True},  
            'role': {'read_only': True},  
        }
 

    def validate_gender(self, value):
        if value.lower() not in ['male', 'female']:
            raise serializers.ValidationError("Invalid value for gender field.")
        return value
            
    def validate_password(self, value):
        if value:
            if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,30}$', value):
                raise serializers.ValidationError("Password must contain at least one lowercase letter, one uppercase letter, one digit, one special character, and be between 8 and 30 characters long.")
        return value


    def save(self, **kwargs):
        user = User(
            email=self.validated_data['email'],
            first_name=self.validated_data.get('first_name', ''),
            last_name=self.validated_data.get('last_name', ''),
            gender=self.validated_data.get('gender', ''),
            date_of_birth=self.validated_data.get('date_of_birth', ''),
        )
        # Set and hash the password
        user.set_password(self.validated_data['password'])
        user.save()
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    date_of_birth = serializers.DateField()

    def validate_gender(self, value):
        if value.lower() not in ['male', 'female']:
            raise serializers.ValidationError("Invalid value for gender field.")
        return value

    def validate_password(self, value):
        if value:
            if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,30}$', value):
                raise serializers.ValidationError("Password must contain at least one lowercase letter, one uppercase letter, one digit, one special character, and be between 8 and 30 characters long.")
        return value

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'gender', 'date_of_birth', 'email', 'role', 'password', 'is_verified', 'created_at', 'updated_at')
        extra_kwargs = {
            'password': {'write_only': True}, 
            'is_verified': {'read_only': True},  
            'role': {'read_only': True},  
            'email': {'read_only': True},  
        }

    def update(self, instance, validated_data):
        if 'password' not in validated_data:
            validated_data['password'] = instance.password
        else:
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)


