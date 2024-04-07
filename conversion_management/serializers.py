from rest_framework import serializers
from .models import ConversionHistory
from utils.upload_to_cloudinary import upload_image

class ConversionHistorySerializer(serializers.ModelSerializer):
    image_file = serializers.ImageField(write_only=True)

    class Meta:
        model = ConversionHistory
        fields = ('id', 'image_file', 'text_content', 'image_url', 'created_at', 'updated_at')
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},
            'image_url': {'read_only': True},
            'CreatedAt': {'read_only': True},
            'UpdatedAt': {'read_only': True},
        }
        
    def create(self, validated_data):
        image = validated_data.pop('image_file')
        res = upload_image(image)
        validated_data['image_url'] = res['url']
        return super().create(validated_data)
     
class ConversionHistoryUpdateSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    
    class Meta:
        model = ConversionHistory
        fields = ('id', 'user', 'text_content', 'image_url', 'created_at', 'updated_at')
        extra_kwargs = {
            'user': {'read_only': True},
            'image_url': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }
        
