from rest_framework import serializers
from . import models
from package_manager.models import PackagePlanDetails, PlanType



class ChapaPaymentInitializationSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True, allow_null=False)
    usage_limit = serializers.IntegerField(required=False, allow_null=True)

    def validate_id(self, value):
        package = PackagePlanDetails.objects.filter(id=value).first()
        if not package:
            raise serializers.ValidationError("Package not found")
        
        if package.plan_type in [PlanType.FREE_PACKAGE, PlanType.FREE_UNREGISTERED_PACKAGE, PlanType.PREMIER_TRIAL_PACKAGE]:
            raise serializers.ValidationError("You cannot subscribe to a free package")
        
        return value

    def validate_usage_limit(self, value):
        package_id = self.initial_data.get('id')
        
        if not package_id:
            raise serializers.ValidationError("id is required to validate usage_limit")

        try:
            package = PackagePlanDetails.objects.get(id=package_id)
        except PackagePlanDetails.DoesNotExist:
            raise serializers.ValidationError("Package not found")
        
        if package.plan_type in [PlanType.CUSTOM_LIMITED_USAGE, PlanType.NON_EXPIRING_LIMITED_USAGE]:
            if value is None:
                raise serializers.ValidationError("usage_limit is required for this package")
            elif value < 1:
                raise serializers.ValidationError("usage_limit must be greater than 0")
        
        return value
    
    class Meta:
        model = models.ChapaTransactions
        fields = ['id', 'usage_limit']

        
    def create(self, validated_data):
        return models.ChapaTransactions.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.response_dump = validated_data.get('response_dump', instance.response_dump)
        instance.checkout_url = validated_data.get('checkout_url', instance.checkout_url)
        instance.save()
        return instance


