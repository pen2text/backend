from rest_framework import serializers
from .models import RemoteAPITokenManager

class RemoteAPITokenManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = RemoteAPITokenManager
        fields = ['id', 'user', 'name', 'created_at']
        extra_kwargs = {
            'user': {'read_only': True},
            'created_at': {'read_only': True},
        }

