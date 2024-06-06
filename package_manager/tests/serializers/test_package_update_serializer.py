import pytest
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from package_manager.serializers import PackagePlanDetailUpdateSerializer
from package_manager.models import PackagePlanDetails, PlanType

@pytest.mark.django_db
class TestPackagePlanDetailUpdateSerializer:
    factory = APIRequestFactory()
    request = factory.get('/fake-url/')
    serializer_context = {'request': Request(request)}

    def test_serialize_valid_data(self, package_plans):
        plan = package_plans[0]
        serializer = PackagePlanDetailUpdateSerializer(instance=plan, context=self.serializer_context)
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
        serializer = PackagePlanDetailUpdateSerializer(instance=plan, context=self.serializer_context)
        data = serializer.data

        assert 'id' in data
        assert 'created_at' in data
        assert 'updated_at' in data

    def test_validate_existing_plan_type(self, package_plans):
        existing_plan_type = package_plans[0].plan_type
        data = {
            'id': str(package_plans[1].id),
            'name': 'new_plan',
            'usage_limit': 10,
            'plan_type': existing_plan_type,
            'price': 10.00,
            'days': 10
        }
        serializer = PackagePlanDetailUpdateSerializer(instance=package_plans[1], data=data, context=self.serializer_context)
        assert not serializer.is_valid()
        assert 'plan_type' in serializer.errors

    def test_validate_unique_name_per_type(self, package_plans):
        existing_plan = package_plans[0]
        data = {
            'id': str(package_plans[1].id),
            'name': existing_plan.name,
            'usage_limit': 10,
            'plan_type': existing_plan.plan_type,
            'price': 10.00,
            'days': 10
        }
        serializer = PackagePlanDetailUpdateSerializer(instance=package_plans[1], data=data, context=self.serializer_context)
        assert not serializer.is_valid()
        assert 'name' in serializer.errors

    def test_validate_usage_limit_unlimited(self, package_plans):
        data = {
            'id': str(package_plans[4].id),
            'name': 'unlimited_usage_plan',
            'usage_limit': 10,
            'plan_type': PlanType.UNLIMITED_USAGE,
            'price': 20.00,
            'days': 30
        }
        serializer = PackagePlanDetailUpdateSerializer(instance=package_plans[4], data=data, context=self.serializer_context)
        assert serializer.is_valid()
        assert serializer.validated_data['usage_limit'] == 0
      
    def test_update_plan(self, package_plans):
        plan = package_plans[0]
        updated_data = {
            'id': str(plan.id),
            'name': 'updated_plan',
            'usage_limit': 50,
            'plan_type': PlanType.LIMITED_USAGE,
            'price': 25.00,
            'days': 60
        }
        serializer = PackagePlanDetailUpdateSerializer(instance=plan, data=updated_data, context=self.serializer_context)
        assert serializer.is_valid()
        updated_instance = serializer.save()

        assert updated_instance.name == updated_data['name']
        assert updated_instance.usage_limit == updated_data['usage_limit']
        assert updated_instance.plan_type == updated_data['plan_type']
        assert updated_instance.price == updated_data['price']
        assert updated_instance.days == updated_data['days']

    def test_validate_days_non_expiring(self, package_plans):
        plan = package_plans[3]
        
        data = {
            'id': str(plan.id),
            'days': 10,
            'plan_type': PlanType.NON_EXPIRING_LIMITED_USAGE
        }
        serializer = PackagePlanDetailUpdateSerializer(instance=plan, data=data, context=self.serializer_context)
        assert serializer.is_valid()
        assert serializer.validated_data['days'] == 0

    def test_serialize_invalid_data(self, package_plans):
        plan = package_plans[0]
        invalid_data = {
            'id': str(plan.id),
            'usage_limit': -1,
            'plan_type': PlanType.LIMITED_USAGE,
            'price': -5,
            'days': -10
        }
        serializer = PackagePlanDetailUpdateSerializer(instance=plan, data=invalid_data, context=self.serializer_context)
        assert not serializer.is_valid()

        errors = serializer.errors
        assert 'usage_limit' in errors
        assert 'price' in errors
        assert 'days' in errors
