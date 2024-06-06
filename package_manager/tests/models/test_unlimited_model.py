import pytest
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from package_manager.models import UnlimitedUsageSubscriptionPlans
from datetime import datetime, timedelta
from django.utils import timezone


@pytest.mark.django_db
class TestUnlimitedUsageSubscriptionPlans:

    def test_unlimited_usage_subscription_plans_creation(self, users, package_plans, transactions):
        expire_date = timezone.now() + timedelta(days=30)
        subscription_plan = UnlimitedUsageSubscriptionPlans.objects.create(
            user=users[0],
            package_plan=package_plans[3],  
            transaction=transactions[0],  
            expire_date=expire_date
        )

        assert subscription_plan.user == users[0]
        assert subscription_plan.package_plan == package_plans[3]
        assert subscription_plan.transaction == transactions[0]
        assert subscription_plan.expire_date == expire_date

    def test_unlimited_usage_subscription_plans_creation_without_user(self, package_plans, transactions):
        with pytest.raises(IntegrityError):
            UnlimitedUsageSubscriptionPlans.objects.create(
                package_plan=package_plans[3],
                transaction=transactions[0],
                expire_date=datetime.now() + timedelta(days=30)
            )

    def test_unlimited_usage_subscription_plans_creation_without_package_plan(self, users, transactions):
        with pytest.raises(IntegrityError):
            UnlimitedUsageSubscriptionPlans.objects.create(
                user=users[0],
                transaction=transactions[0],
                expire_date=datetime.now() + timedelta(days=30)
            )

    def test_unlimited_usage_subscription_plans_creation_without_transaction(self, users, package_plans):
        with pytest.raises(IntegrityError):
            UnlimitedUsageSubscriptionPlans.objects.create(
                user=users[0],
                package_plan=package_plans[3],
                expire_date=datetime.now() + timedelta(days=30)
            )

    def test_unlimited_usage_subscription_plans_creation_with_past_expire_date(self, users, package_plans, transactions):
        
        past_expire_date = timezone.now() - timedelta(days=30)
        
        with pytest.raises(ValidationError):
            subscription_plan = UnlimitedUsageSubscriptionPlans(
                user=users[0],
                package_plan=package_plans[3],
                transaction=transactions[0],
                expire_date=past_expire_date
            )
            subscription_plan.full_clean()
