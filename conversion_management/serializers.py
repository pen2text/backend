from rest_framework import serializers
from .models import ConversionHistories

class ConversionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversionHistories
        fields = ('id', 'text_content', 'image_url', 'created_at', 'updated_at')
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},
            'image_url': {'read_only': True},
            'CreatedAt': {'read_only': True},
            'UpdatedAt': {'read_only': True},
        }
        
    # def create(self, validated_data):
    #     return super().create(validated_data)
     
class ConversionHistoryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversionHistories
        fields = ('id', 'user', 'text_content', 'image_url', 'created_at', 'updated_at')
        extra_kwargs = {
            'user': {'read_only': True},
            'image_url': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }
        
    def update(self, instance, validated_data):
        instance.text_content = validated_data.get('text_content', instance.text_content)
        instance.save()
        return instance