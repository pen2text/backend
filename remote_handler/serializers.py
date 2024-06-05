from rest_framework import serializers
from .models import RemoteAPITokenManagers

class RemoteAPITokenManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = RemoteAPITokenManagers
        fields = ['id', 'user', 'name', 'token', 'created_at']
        extra_kwargs = {
            'user': {'read_only': True},
            'created_at': {'read_only': True},
            'token': {'read_only': True},
        }

