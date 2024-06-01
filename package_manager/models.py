from django.db import models
from user_management.models import Users
from chapa_gateway.models import ChapaTransactions
import uuid

class PlanType(models.TextChoices):
    UNLIMITED_USAGE = 'unlimited_usage', 'UNLIMITED_USAGE'
    LIMITED_USAGE = 'limited_usage', 'LIMITED_USAGE'
    NON_EXPIRING_LIMITED_USAGE = 'non_expiring_limited_usage', 'NON_EXPIRING_LIMITED_USAGE'
    CUSTOM_LIMITED_USAGE = 'custom_limited_usage', 'CUSTOM_LIMITED_USAGE'
    FREE_PACKAGE = 'free_package', 'FREE_PACKAGE'
    FREE_UNREGISTERED_PACKAGE = 'free_unregistered_package', 'FREE_UNREGISTERED_PACKAGE'
    PREMIER_TRIAL_PACKAGE = 'premier_trial_package', 'PREMIER_TRIAL_PACKAGE'

class PackagePlanDetails(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20)
    plan_type = models.CharField(max_length=30, choices=PlanType.choices)
    usage_limit = models.IntegerField(default=0)
    price = models.FloatField(default=0.0)
    days = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'package_plan_details'
    
class UserAccessRecords(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
    ip_address = models.CharField(max_length=50)
    usage_count = models.IntegerField(default=0)
    package_plan = models.ForeignKey(PackagePlanDetails, on_delete=models.CASCADE)
    last_date_use = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_access_records'

class UnlimitedUsageSubscriptionPlans(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    package_plan = models.ForeignKey(PackagePlanDetails, on_delete=models.CASCADE)
    transaction = models.OneToOneField(ChapaTransactions, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # expire_date = models.DateTimeField()
    
    class Meta:
        db_table = 'unlimited_usage_subscription_plans'

class LimitedUsageSubscriptionPlans(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    package_detail = models.ForeignKey(PackagePlanDetails, on_delete=models.CASCADE)
    transaction = models.OneToOneField(ChapaTransactions, on_delete=models.CASCADE)
    usage_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    usage_limit = models.IntegerField(default=0)
    # expire_date = models.DateTimeField(null=True)
    
    class Meta:
        db_table = 'limited_usage_subscription_plans'

class TempSubscriptionPlans(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    transaction = models.OneToOneField(ChapaTransactions, on_delete=models.CASCADE)
    package_detail = models.ForeignKey(PackagePlanDetails, on_delete=models.CASCADE)
    usage_limit = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'temp_subscription_plans'