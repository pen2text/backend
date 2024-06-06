import pytest
from package_manager.models import TempSubscriptionPlans
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta

@pytest.mark.django_db
class TestTempSubscriptionPlans:

    def test_temp_subscription_plans_creation(self, users, package_plans, transactions):
        subscription_plan = TempSubscriptionPlans.objects.create(
            user=users[0],
            transaction=transactions[0],
            package_detail=package_plans[0],
            usage_limit=500,  
        )

        assert subscription_plan.user == users[0]
        assert subscription_plan.transaction == transactions[0]
        assert subscription_plan.package_detail == package_plans[0]
        assert subscription_plan.usage_limit == 500

    def test_temp_subscription_plans_creation_without_user(self, package_plans, transactions):
        with pytest.raises(IntegrityError):
            TempSubscriptionPlans.objects.create(
                transaction=transactions[0],
                package_detail=package_plans[0], 
                usage_limit=500,
            )

    def test_temp_subscription_plans_creation_without_transaction(self, users, package_plans):
        with pytest.raises(IntegrityError):
            TempSubscriptionPlans.objects.create(
                user=users[0],
                package_detail=package_plans[0], 
                usage_limit=500, 
            )

    def test_temp_subscription_plans_creation_without_package_detail(self, users, transactions):
        with pytest.raises(IntegrityError):
            TempSubscriptionPlans.objects.create(
                user=users[0],
                transaction=transactions[0],
                usage_limit=500, 
            )

    def test_temp_subscription_plans_creation_with_invalid_usage_limit(self, users, package_plans, transactions):
        with pytest.raises(ValidationError):
            subscription_plan = TempSubscriptionPlans(
                user=users[0],
                transaction=transactions[0],
                package_detail=package_plans[0],  
                usage_limit=-100, 
            )
            subscription_plan.full_clean() 
