import uuid
import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestPackagePlanFeeCalculateView:
    
    @pytest.fixture(autouse=True)
    def setup(self, api_client, package_plans):
        self.api_client = api_client
        self.package_plans = package_plans
        self.url = reverse('package-plan-fee-calculate')

    def test_calculate_fee_not_found_package(self):
        non_existent_package_id = uuid.UUID(int=0)
        
        response = self.api_client.post(self.url, {'id': non_existent_package_id})
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['message'] == 'Package Plan not found'

    def test_calculate_fee_free_package(self):
        package = self.package_plans[0]
        response = self.api_client.post(self.url, {'id': package.id})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['message'] == 'This package is free'

    def test_calculate_fee_fixed_fee_package(self):
        package = self.package_plans[3]
        response = self.api_client.post(self.url, {'id': package.id})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['message'] == 'This package has fixed fee'
        assert 'fee' in response.data['data']

    def test_calculate_fee_custom_fee_package(self):
        package = self.package_plans[5]
        
        response = self.api_client.post(self.url, {'id': package.id, 'usage_limit': 100})
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'OK'
        assert response.data['message'] == 'Package fee calculated successfully'
        assert 'fee' in response.data['data']

    @pytest.mark.parametrize("usage_limit", [(0), ()])   
    def test_calculate_fee_custom_fee_package_with_invalid_usage_limit(self, usage_limit):
        package = self.package_plans[5]
        
        response = self.api_client.post(self.url, {'id': package.id, "usage_limit": usage_limit})
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['status'] == 'FAILED'
        assert response.data['message'] == 'Validation failed'
        assert 'usage_limit' in response.data['errors']
        
