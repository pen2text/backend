from rest_framework import serializers
from .models import User

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
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'gender', 'date_of_birth', 'email', 'role', 'password', 'is_verified', 'created_at', 'updated_at')
        extra_kwargs = {
            'password': {'write_only': True}, 
            'is_verified': {'read_only': True},  
            'role': {'read_only': True},  
            'email': {'read_only': True},  
        }
        
        def to_internal_value(self, data):
                data['id'] = self.context['view'].kwargs['id']
                return super().to_internal_value(data)
