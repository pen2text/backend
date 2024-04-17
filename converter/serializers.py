from rest_framework import serializers
from utils.jwt_token_utils import verify_token

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