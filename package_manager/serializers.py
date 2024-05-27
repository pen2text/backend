from rest_framework import serializers
from package_manager import models


class PackagePlanDetailSerializer(serializers.ModelSerializer):
    
    def validate(self, data):
        pass
        
    class Meta:
        model = models.PackagePlanDetails
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
    

    
