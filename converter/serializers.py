from rest_framework import serializers
from utils.jwt_token_utils import verify_token
from PIL import Image as PILImage


class ConverterSerializer(serializers.Serializer):
    image = serializers.ImageField()
    
    class Meta:
        fields = ['image', 'text-content', 'state']
        extra_kwargs = {
            'image': {'write_only': True},
            'text-content': {'read_only': True},
            'state': {'read_only': True},
        }

class ImageUploadSerializer(serializers.Serializer):
    images = serializers.ListField(
        child = serializers.ImageField(max_length=100, allow_empty_file=False, use_url=False)
    )

    def validate_images(self, images):
        for image in images:
            if image.size > 10 * 1024 * 1024:  # 10MB
                raise serializers.ValidationError("Image file should not exceed 10MB in size")

            try:
                img = PILImage.open(image)
                img.verify()
            except (IOError, SyntaxError):
                raise serializers.ValidationError("File is not an image file")
        
        return images
    
class RemoteConverterSerializer(serializers.Serializer):
    index = serializers.IntegerField()
    image = serializers.ImageField()
    access_key = serializers.CharField()
    
    def validate_access_key(self, value):
        if not value:
            raise serializers.ValidationError('Access key is required')

        try:
            token = verify_token(value, 'remote-access-key')
            return token
        except ValueError as e:
            raise serializers.ValidationError(str(e))
    
    class Meta:
        fields = ['index', 'image', 'text-content', 'state', 'access_key']
        extra_kwargs = {
            'image': {'write_only': True},
            'text-content': {'read_only': True},
            'state': {'read_only': True},
        }