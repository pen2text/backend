from rest_framework import serializers
from package_manager.models import PackagePlanDetails, PlanType


class PackagePlanDetailSerializer(serializers.ModelSerializer):
    
    def validate_plan_type(self, value):
        if value in [PlanType.FREE_PACKAGE, PlanType.FREE_UNREGISTERED_PACKAGE, PlanType.PREMIER_TRIAL_PACKAGE]:
            if PackagePlanDetails.objects.filter(plan_type= value).exists():
                raise serializers.ValidationError('This Package plan type already exists')   
        
        return value    
    
    def validate_usage_limit(self, value):
        plan_type = self.initial_data.get('plan_type')
        
        if plan_type == PlanType.UNLIMITED_USAGE:
            return 0
            # raise serializers.ValidationError('Usage limit cannot be set for unlimited package plans')
        
        if value <= 0:
            raise serializers.ValidationError('Usage limit must be greater than 0')
        return value
    
    def validate_days(self, value):
        plan_type = self.initial_data.get('plan_type')
        
        if plan_type == PlanType.NON_EXPIRING_LIMITED_USAGE:
            return 0
            # raise serializers.ValidationError('Days cannot be set for non expiring package plans')
        
        if value <= 0:
            raise serializers.ValidationError('Days must be greater than 0')
        return value
    
    def validate_name(self, value):
        value = value.lower().strip()
        plan_type = self.initial_data.get('plan_type')
       
        if PackagePlanDetails.objects.filter(name=value.lower(), plan_type=plan_type).exists():
            raise serializers.ValidationError('Package plan with this name and package type already exists')
        
        return value
    
    def validate_price(self, value):
        plan_type = self.initial_data.get('plan_type')

        if plan_type in [PlanType.FREE_PACKAGE, PlanType.FREE_UNREGISTERED_PACKAGE, PlanType.PREMIER_TRIAL_PACKAGE]:
            return 0
            # raise serializers.ValidationError('Price cannot be set for this package plan')
        
        if value <= 0:
            raise serializers.ValidationError('Package price must be greater than 0')
        return value
             
    class Meta:
        model = PackagePlanDetails
        fields = ['id', 'name', 'usage_limit', 'plan_type', 'price', 'days', 'created_at', 'updated_at']
        kwargs = {
            'id': {'read_only': True},
            'name': {'required': True},
            'usage_limit': {'required': True},
            'plan_type': {'required': True},
            'price': {'required': True},
            'days': {'required': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }

class PackagePlanDetailUpdateSerializer(PackagePlanDetailSerializer):
    id = serializers.UUIDField()
     
    def validate_plan_type(self, value):
        if value in [PlanType.FREE_PACKAGE, PlanType.FREE_UNREGISTERED_PACKAGE, PlanType.PREMIER_TRIAL_PACKAGE]:
            package = PackagePlanDetails.objects.filter(plan_type=value).exclude(id=self.instance.id)
            if package.exists():
                raise serializers.ValidationError('This Package plan type already exists')   
        return value 
    
    def validate_name(self, value):
        value = value.lower().strip()
        plan_type = self.initial_data.get('plan_type')
        package = PackagePlanDetails.objects.filter(name=value.lower(), plan_type=plan_type).exclude(id=self.instance.id)
        if package.exists():
            raise serializers.ValidationError('Package plan with this name and package type already exists')
        return value
    
    def validate_days(self, value):
        plan_type = self.instance.plan_type
        if 'plan_type' in self.initial_data:
            plan_type = self.initial_data.get('plan_type')
        
        if plan_type == PlanType.NON_EXPIRING_LIMITED_USAGE:
            return 0
            # raise serializers.ValidationError('Days cannot be set for non expiring package plans')
        
        if value <= 0:
            raise serializers.ValidationError('Days must be greater than 0')
        return value
    
    def validate_usage_limit(self, value):
        plan_type = self.initial_data.get('plan_type')
        
        if plan_type == PlanType.UNLIMITED_USAGE:
            return 0
            # raise serializers.ValidationError('Usage limit cannot be set for unlimited package plans')
        
        if value <= 0:
            raise serializers.ValidationError('Usage limit must be greater than 0')
        return value
    
    def validate_price(self, value):
        plan_type = self.initial_data.get('plan_type')

        if plan_type in [PlanType.FREE_PACKAGE, PlanType.FREE_UNREGISTERED_PACKAGE, PlanType.PREMIER_TRIAL_PACKAGE]:
            return 0
            # raise serializers.ValidationError('Price cannot be set for this package plan')
        
        if value <= 0:
            raise serializers.ValidationError('Package price must be greater than 0')
        return value
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.usage_limit = validated_data.get('usage_limit', instance.usage_limit)
        instance.days = validated_data.get('days', instance.days)
        instance.plan_type = validated_data.get('plan_type', instance.plan_type)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance

    class Meta:
        model = PackagePlanDetails
        fields = ['id', 'name', 'usage_limit', 'plan_type', 'price', 'days', 'created_at', 'updated_at']
        extra_kwargs = {
            'id': {'required': True}, 
            'name': {'required': False, 'allow_blank': True, 'allow_null': True},
            'usage_limit': {'required': False, 'allow_null': True},
            'plan_type': {'required': False, 'allow_null': True},
            'price': {'required': False, 'allow_null': True},
            'days': {'required': False, 'allow_null': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }
        