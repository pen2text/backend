from django.db import models
from user_management.models import User
import uuid

class SubscriptionPlanDetails(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    amount = models.IntegerField()

class UnlimitedSubscriptionPlans(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan_details = models.ForeignKey(SubscriptionPlanDetails, on_delete=models.CASCADE)
    expire_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

class LimitedSubscriptionPlans(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan_details = models.ForeignKey(SubscriptionPlanDetails, on_delete=models.CASCADE)
    access_limit = models.IntegerField(default=0)
    usage_count = models.IntegerField(default=0)
    expire_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class UserAccessRecords(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    ip_address = models.CharField(max_length=50)
    access_limit = models.IntegerField(default=0)
    usage_count = models.IntegerField(default=0)
    expire_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
