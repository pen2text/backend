import pytest
from datetime import datetime
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from user_management.models import Users
from package_manager.models import PackagePlanDetails, PlanType
from package_manager.models import UserAccessRecords 


@pytest.mark.django_db
class TestUserAccessRecords:

    @pytest.fixture
    def user(self, db):
        user = Users.objects.create(
            first_name='John',
            last_name='Doe',
            gender='male',
            date_of_birth=datetime(1990, 1, 1),
            email='john.doe@example.com',
            is_verified=True,
            role='user'
        )
        user.set_password('password123')
        user.save()
        return user

    @pytest.fixture
    def package_plan(self, db):
        return PackagePlanDetails.objects.create(
            name='Basic Plan',
            plan_type=PlanType.UNLIMITED_USAGE,
            usage_limit=1000,
            price=29.99,
            days=30
        )

    def test_user_access_records_creation(self, user, package_plan):
        access_record = UserAccessRecords.objects.create(
            user=user,
            ip_address='192.168.1.1',
            usage_count=10,
            package_plan=package_plan
        )

        # Assertions to verify the correctness of the created instance
        assert access_record.user == user
        assert access_record.ip_address == '192.168.1.1'
        assert access_record.usage_count == 10
        assert access_record.package_plan == package_plan

    def test_user_access_records_creation_without_user(self, package_plan):
        access_record = UserAccessRecords.objects.create(
            ip_address='192.168.1.1',
            usage_count=10,
            package_plan=package_plan
        )

        # Assertions to verify the correctness of the created instance
        assert access_record.user is None
        assert access_record.ip_address == '192.168.1.1'
        assert access_record.usage_count == 10
        assert access_record.package_plan == package_plan

    def test_user_access_records_creation_without_package_plan(self, user):
        with pytest.raises(IntegrityError):
            UserAccessRecords.objects.create(
                user=user,
                ip_address='192.168.1.1',
                usage_count=10
            )

    def test_user_access_records_creation_with_long_ip_address(self, user, package_plan):
        with pytest.raises(ValidationError):
            access_record = UserAccessRecords(
                user=user,
                ip_address='a' * 51,  # IP address longer than the allowed length
                usage_count=10,
                package_plan=package_plan
            )
            access_record.full_clean()  # This triggers model validation

    def test_user_access_records_creation_with_negative_usage_count(self, user, package_plan):
        with pytest.raises(ValidationError):
            access_record = UserAccessRecords(
                user=user,
                ip_address='192.168.1.1',
                usage_count=-1,  # Negative usage count
                package_plan=package_plan
            )
            access_record.full_clean() 
