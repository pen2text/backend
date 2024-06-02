from rest_framework import serializers
from package_manager.models import PackagePlanDetails, PlanType


class ChapaPaymentInitializationSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True, allow_null=False)
    usage_limit = serializers.IntegerField(required=False, allow_null=True)

    def validate(self, data):
        package_id = data['id']
        
        try:
            print('package_id: ', package_id)
            package = PackagePlanDetails.objects.get(id=package_id)
        except PackagePlanDetails.DoesNotExist:
            raise serializers.ValidationError({'id': "id doesn't found"})
        
        if package.plan_type in [PlanType.CUSTOM_LIMITED_USAGE, PlanType.NON_EXPIRING_LIMITED_USAGE]:
            usage_limit = data.get('usage_limit')
            if not usage_limit:
                raise serializers.ValidationError({'usage_limit': "usage_limit is required for this package"})
            elif usage_limit < 1:
                raise serializers.ValidationError({'usage_limit': "usage_limit must be greater than 0"})
        
        return data
    
    class Meta:
        fields = ['id', 'usage_limit']
