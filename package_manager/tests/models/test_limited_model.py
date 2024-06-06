import pytest
from package_manager.models import LimitedUsageSubscriptionPlans
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from datetime import timedelta
from django.utils import timezone

@pytest.mark.django_db
class TestLimitedUsageSubscriptionPlans:

    def test_limited_usage_subscription_plans_creation(self, users, package_plans, transactions):
        subscription_plan = LimitedUsageSubscriptionPlans.objects.create(
            user=users[0],
            package_detail=package_plans[3],  # Using the limited usage package plan
            transaction=transactions[0],
            usage_count=500,
            usage_limit=1000,
            expire_date=timezone.now() + timedelta(days=30)
        )

        # Assertions to verify the correctness of the created instance
        assert subscription_plan.user == users[0]
        assert subscription_plan.package_detail == package_plans[3]
        assert subscription_plan.transaction == transactions[0]
        assert subscription_plan.usage_count == 500
        assert subscription_plan.usage_limit == 1000

    def test_limited_usage_subscription_plans_creation_without_user(self, package_plans, transactions):
        with pytest.raises(IntegrityError):
            LimitedUsageSubscriptionPlans.objects.create(
                package_detail=package_plans[3],
                transaction=transactions[0],
                usage_count=500,
                usage_limit=1000,
                expire_date=timezone.now() + timedelta(days=30)
            )

    def test_limited_usage_subscription_plans_creation_without_package_plan(self, users, transactions):
        with pytest.raises(IntegrityError):
            LimitedUsageSubscriptionPlans.objects.create(
                user=users[0],
                transaction=transactions[0],
                usage_count=500,
                usage_limit=1000,
                expire_date=timezone.now() + timedelta(days=30)
            )

    def test_limited_usage_subscription_plans_creation_without_transaction(self, users, package_plans):
        with pytest.raises(IntegrityError):
            LimitedUsageSubscriptionPlans.objects.create(
                user=users[0],
                package_detail=package_plans[3],
                usage_count=500,
                usage_limit=1000,
                expire_date=timezone.now() + timedelta(days=30)
            )

    def test_limited_usage_subscription_plans_creation_with_invalid_usage_count(self, users, package_plans, transactions):
        with pytest.raises(ValidationError):
            subscription_plan = LimitedUsageSubscriptionPlans(
                user=users[0],
                package_detail=package_plans[3],
                transaction=transactions[0],
                usage_count=-100,  # Invalid usage count
                usage_limit=1000,
                expire_date=timezone.now() + timedelta(days=30)
            )
            subscription_plan.full_clean()  # This triggers model validation

    def test_limited_usage_subscription_plans_creation_with_invalid_usage_limit(self, users, package_plans, transactions):
        with pytest.raises(ValidationError):
            subscription_plan = LimitedUsageSubscriptionPlans(
                user=users[0],
                package_detail=package_plans[3],
                transaction=transactions[0],
                usage_count=500,
                usage_limit=-100,  # Invalid usage limit
                expire_date=timezone.now() + timedelta(days=30)
            )
            subscription_plan.full_clean()  # This triggers model validation

    def test_limited_usage_subscription_plans_creation_with_past_expire_date(self, users, package_plans, transactions):
        passed_expire_date = timezone.now() - timedelta(days=package_plans[3].days)
        with pytest.raises(ValidationError):
            subscription_plan = LimitedUsageSubscriptionPlans(
                user=users[0],
                package_detail=package_plans[3],
                transaction=transactions[0],
                usage_count=500,
                usage_limit=1000,
                expire_date=passed_expire_date
            )
            subscription_plan.full_clean()
