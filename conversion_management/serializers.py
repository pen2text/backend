from rest_framework import serializers
from .models import ConversionHistory


class ConversionHistorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ConversionHistory
        fields = ('id', 'user_id', 'TextContent', 'ImageURL', 'CreatedAt', 'UpdatedAt')
        extra_kwargs = {
            'id': {'read_only': True},
            'CreatedAt': {'read_only': True},
            'UpdatedAt': {'read_only': True},
        }
    
    
class ConversionHistoryUpdateSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    
    class Meta:
        model = ConversionHistory
        fields = ('id','TextContent', 'ImageURL', 'CreatedAt', 'UpdatedAt')
        extra_kwargs = {
            'ImageURL': {'read_only': True},
            'UpdatedAt': {'read_only': True},
            'CreatedAt': {'read_only': True},
        }
        
