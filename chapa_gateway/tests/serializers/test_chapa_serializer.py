from django.test import TestCase
from uuid import uuid4

from chapa_gateway.serializers import ChapaPaymentInitializationSerializer
from package_manager.models import PackagePlanDetails, PlanType

class ChapaPaymentInitializationSerializerTest(TestCase):

    def setUp(self):
        self.package1 = PackagePlanDetails.objects.create(id=uuid4(), plan_type=PlanType.CUSTOM_LIMITED_USAGE)
        self.package2 = PackagePlanDetails.objects.create(id=uuid4(), plan_type=PlanType.NON_EXPIRING_LIMITED_USAGE)
        self.package3 = PackagePlanDetails.objects.create(id=uuid4(), plan_type=PlanType.UNLIMITED_USAGE)

    def test_valid_data(self):
        valid_data = {'id': self.package1.id, 'usage_limit': 5}
        serializer = ChapaPaymentInitializationSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())

        valid_data = {'id': self.package2.id, 'usage_limit': 10}
        serializer = ChapaPaymentInitializationSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())

        valid_data = {'id': self.package3.id}
        serializer = ChapaPaymentInitializationSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())

    def test_missing_usage_limit(self):
        invalid_data = {'id': self.package1.id}
        serializer = ChapaPaymentInitializationSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('usage_limit', serializer.errors)

        invalid_data = {'id': self.package2.id}
        serializer = ChapaPaymentInitializationSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('usage_limit', serializer.errors)

    def test_invalid_usage_limit(self):
        invalid_data = {'id': self.package1.id, 'usage_limit': 0}
        serializer = ChapaPaymentInitializationSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('usage_limit', serializer.errors)

        invalid_data = {'id': self.package1.id, 'usage_limit': -1}
        serializer = ChapaPaymentInitializationSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('usage_limit', serializer.errors)
