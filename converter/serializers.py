from rest_framework import serializers


class ConverterSerializer(serializers.Serializer):
    index = serializers.IntegerField()
    image = serializers.ImageField()
    
    class Meta:
        fields = ['index', 'image', 'text-content', 'status']
        extra_kwargs = {
            'text-content': {'read_only': True},
            'status': {'read_only': True}
        }