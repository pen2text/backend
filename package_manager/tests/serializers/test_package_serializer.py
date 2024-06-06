import pytest
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from package_manager.serializers import PackagePlanDetailSerializer
from package_manager.models import PlanType

@pytest.mark.django_db
class TestPackagePlanDetailSerializer:
    factory = APIRequestFactory()
    request = factory.get('/fake-url/')
    serializer_context = {'request': Request(request)}

    def test_serialize_valid_data(self, package_plans):
        plan = package_plans[0]
        serializer = PackagePlanDetailSerializer(instance=plan, context=self.serializer_context)
        data = serializer.data

        assert str(data['id']) == str(plan.id)
        assert data['name'] == plan.name
        assert data['usage_limit'] == plan.usage_limit
        assert data['plan_type'] == plan.plan_type
        assert data['price'] == plan.price
        assert data['days'] == plan.days
        assert 'created_at' in data
        assert 'updated_at' in data

    def test_serialize_read_only_fields(self, package_plans):
        plan = package_plans[0]
        serializer = PackagePlanDetailSerializer(instance=plan, context=self.serializer_context)
        data = serializer.data

        assert 'id' in data
        assert 'created_at' in data
        assert 'updated_at' in data

    def test_serialize_invalid_data(self):
        invalid_data = {
            'name': '',
            'usage_limit': -1,
            'plan_type': PlanType.LIMITED_USAGE,
            'price': -5,
            'days': -10
        }
        serializer = PackagePlanDetailSerializer(data=invalid_data, context=self.serializer_context)
        assert not serializer.is_valid()

        errors = serializer.errors
        assert 'name' in errors
        assert 'usage_limit' in errors
        assert 'price' in errors
        assert 'days' in errors

    def test_validate_existing_plan_type(self, package_plans):
        existing_plan_type = package_plans[0].plan_type
        data = {
            'name': 'new_plan',
            'usage_limit': 10,
            'plan_type': existing_plan_type,
            'price': 10.00,
            'days': 10
        }
        serializer = PackagePlanDetailSerializer(data=data, context=self.serializer_context)
        assert not serializer.is_valid()
        assert 'plan_type' in serializer.errors

    def test_validate_unique_name_per_type(self, package_plans):
        existing_plan = package_plans[0]
        data = {
            'name': existing_plan.name,
            'usage_limit': 10,
            'plan_type': existing_plan.plan_type,
            'price': 10.00,
            'days': 10
        }
        serializer = PackagePlanDetailSerializer(data=data, context=self.serializer_context)
        assert not serializer.is_valid()
        assert 'name' in serializer.errors

    def test_validate_usage_limit_unlimited(self):
        data = {
            'name': 'unlimited_usage_plan',
            'usage_limit': 10,
            'plan_type': PlanType.UNLIMITED_USAGE,
            'price': 20.00,
            'days': 30
        }
        serializer = PackagePlanDetailSerializer(data=data, context=self.serializer_context)
        assert serializer.is_valid()
        assert serializer.validated_data['usage_limit'] == 0

    def test_validate_days_non_expiring(self):
        data = {
            'name': 'non_expiring_plan',
            'usage_limit': 10,
            'plan_type': PlanType.NON_EXPIRING_LIMITED_USAGE,
            'price': 20.00,
            'days': 10
        }
        serializer = PackagePlanDetailSerializer(data=data, context=self.serializer_context)
        assert serializer.is_valid()
        assert serializer.validated_data['days'] == 0
