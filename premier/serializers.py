from rest_framework import serializers
import models  

class SubscriptionPlanDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SubscriptionPlanDetails
        fields = ['id', 'name', 'amount']
        kwargs = {
            'id': {'read_only': True}, 
            'name': {'required': True},
            'amount': {'required': True}
        }

class UnlimitedSubscriptionPlansSerializer(serializers.ModelSerializer):
    plan = serializers.UUIDField()
    
    class Meta:
        model = models.UnlimitedSubscriptionPlans
        fields = ['id', 'user', 'plan_details', 'expire_date', 'created_at']
        

class LimitedSubscriptionPlansSerializer(serializers.ModelSerializer):
    plan = serializers.UUIDField()
    
    class Meta:
        model = models.LimitedSubscriptionPlans
        fields = ['id', 'user', 'plan_details', 'access_limit', 'usage_count', 'expire_date', 'created_at']
        kwargs = {
            'plan_details': {'required': True},            
        }

class UserAccessRecordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserAccessRecords
        fields = ['id', 'user', 'ip_address', 'access_limit', 'usage_count', 'expire_date', 'created_at']
