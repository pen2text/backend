from rest_framework import serializers
from . import models
from package_manager.models import PackagePlanDetails


class PackageSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    usage_limit = serializers.IntegerField(required=False)
    
    def validate_id(self, value):
        try:
            PackagePlanDetails.objects.get(id=value)
            return value
        except PackagePlanDetails.DoesNotExist:
            raise serializers.ValidationError("Package doesn't found")
    
class ChapaTransactionSerializer(serializers.ModelSerializer):
    package = PackageSerializer()
    
    class Meta:
        model = models.ChapaTransactions
        fields = ['id', 'amount', 'currency', 'email', 'phone_number', 'first_name', 'last_name', 'payment_title', 'description', 'package']
        kwargs = {
            'id': {'read_only': True},
            'amount': {'required': True},
            'currency': {'required': True},
            'email': {'required': True},
            'phone_number': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'payment_title': {'required': True},
            'description': {'required': True},
        }
        
    def create(self, validated_data):
        return models.ChapaTransactions.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.response_dump = validated_data.get('response_dump', instance.response_dump)
        instance.checkout_url = validated_data.get('checkout_url', instance.checkout_url)
        instance.save()
        return instance


