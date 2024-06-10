from rest_framework import serializers
from PIL import Image as PILImage


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

class ConvertSerializer(serializers.Serializer):
    pass 