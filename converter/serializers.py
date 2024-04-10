from rest_framework import serializers


class ConverterSerializer(serializers.Serializer):
    index = serializers.IntegerField()
    image = serializers.ImageField()
    
    class Meta:
        fields = ['index', 'image', 'text-content', 'state']
        extra_kwargs = {
            'image': {'write_only': True},
            'text-content': {'read_only': True},
            'state': {'read_only': True},
        }