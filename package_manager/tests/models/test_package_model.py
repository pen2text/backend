import pytest
from django.core.exceptions import ValidationError
from django.db.utils import DataError
from package_manager.models import PackagePlanDetails, PlanType

@pytest.mark.django_db
class TestPackagePlanDetails:

    @pytest.fixture
    def package_plan(self, db):
        return PackagePlanDetails.objects.create(
            name='Basic Plan',
            plan_type=PlanType.UNLIMITED_USAGE,
            usage_limit=1000,
            price=29.99,
            days=30
        )

    def test_package_plan_details_creation(self, package_plan):
        # Assertions to verify the correctness of the created instance
        assert package_plan.name == 'Basic Plan'
        assert package_plan.plan_type == PlanType.UNLIMITED_USAGE
        assert package_plan.usage_limit == 1000
        assert package_plan.price == 29.99
        assert package_plan.days == 30

    def test_package_plan_details_creation_without_name(self):
        invalid_plan = PackagePlanDetails(
            plan_type=PlanType.UNLIMITED_USAGE,
            usage_limit=1000,
            price=29.99,
            days=30
        )
        with pytest.raises(ValidationError):
            invalid_plan.full_clean() 

    def test_package_plan_details_creation_with_long_name(self):
        with pytest.raises(DataError):
            PackagePlanDetails.objects.create(
                name='a' * 21,  # Name longer than the allowed length
                plan_type=PlanType.UNLIMITED_USAGE,
                usage_limit=1000,
                price=29.99,
                days=30
            )

    def test_package_plan_details_creation_with_invalid_plan_type(self):
        with pytest.raises(ValidationError):
            invalid_plan = PackagePlanDetails(
                name='Invalid Plan',
                plan_type='invalid_type',  # Invalid plan type
                usage_limit=1000,
                price=29.99,
                days=30
            )
            invalid_plan.full_clean()  # This triggers model validation

    def test_package_plan_details_creation_with_negative_usage_limit(self):
        with pytest.raises(ValidationError):
            invalid_plan = PackagePlanDetails(
                name='Negative Usage Limit Plan',
                plan_type=PlanType.UNLIMITED_USAGE,
                usage_limit=-100,  # Negative usage limit
                price=29.99,
                days=30
            )
            invalid_plan.full_clean()  # This triggers model validation

    def test_package_plan_details_creation_with_negative_price(self):
        with pytest.raises(ValidationError):
            invalid_plan = PackagePlanDetails(
                name='Negative Price Plan',
                plan_type=PlanType.UNLIMITED_USAGE,
                usage_limit=1000,
                price=-29.99,  # Negative price
                days=30
            )
            invalid_plan.full_clean()  # This triggers model validation

    def test_package_plan_details_creation_with_negative_days(self):
        with pytest.raises(ValidationError):
            invalid_plan = PackagePlanDetails(
                name='Negative Days Plan',
                plan_type=PlanType.UNLIMITED_USAGE,
                usage_limit=1000,
                price=29.99,
                days=-30  # Negative number of days
            )
            invalid_plan.full_clean()  # This triggers model validation
