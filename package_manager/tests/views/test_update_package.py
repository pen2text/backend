import pytest
from rest_framework import status
from django.urls import reverse
from package_manager.models import PlanType

@pytest.fixture
def update_url():
    return reverse('package-plan-update')

@pytest.mark.django_db
class TestPackagePlanDetailUpdate:
    
    @pytest.fixture(autouse=True)
    def setup(self, api_client, users, mock_token, update_url, package_plans):
        self.api_client = api_client
        self.users = users
        self.mock_token = mock_token
        self.update_url = update_url
        self.package_plans = package_plans

    def test_package_plan_update_unauthorized(self):
        package_plan = self.package_plans[0]
        data = {
            "id": package_plan.id,
            "name": "updated_plan",
            "usage_limit": 150,
            "price": 14.99,
            "days": 40
        }
        
        response = self.api_client.put(self.update_url, data, format='json')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert 'detail' in response.data
        assert response.data['detail'] == 'Authentication credentials were not provided.'

    def test_package_plan_update_non_admin(self):
        non_admin_user = self.users[1]  # Non-admin user
        token = self.mock_token(non_admin_user)
        self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        package_plan = self.package_plans[0]
        data = {
            "id": package_plan.id,
            "name": "updated_plan",
            "usage_limit": 150,
            "price": 14.99,
            "days": 40
        }
        
        response = self.api_client.put(self.update_url, data, format='json')
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data['status'] == 'FAILED'
        assert response.data['message'] == 'You are not authorized to update plan'

    def test_package_plan_update_success(self):
        admin_user = self.users[0]  # Admin user
        token = self.mock_token(admin_user)
        self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        package_plan = self.package_plans[0]
        data = {
            "id": package_plan.id,
            "name": "updated_plan",
            "usage_limit": 150,
            "price": 14.99,
            "days": 40
        }
        
        response = self.api_client.put(self.update_url, data, format='json')
        print(response.data)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'OK'
        assert response.data['message'] == 'Plan updated successfully'
        
        assert 'data' in response.data
        assert response.data['data']['name'] == data['name']
        assert response.data['data']['usage_limit'] == data['usage_limit']
        assert response.data['data']['price'] == data['price']
        assert response.data['data']['days'] == data['days']

    def test_package_plan_update_not_found(self):
        admin_user = self.users[0]  # Admin user
        token = self.mock_token(admin_user)
        self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        non_existent_id = 999
        data = {
            "id": non_existent_id,
            "name": "updated_plan",
            "usage_limit": 150,
            "price": 14.99,
            "days": 40
        }
        
        response = self.api_client.put(self.update_url, data, format='json')
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['status'] == 'FAILED'
        assert response.data['message'] == 'Package Plan not found'

    def test_package_plan_update_invalid_data(self):
        admin_user = self.users[0]  # Admin user
        token = self.mock_token(admin_user)
        self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        package_plan = self.package_plans[0] # Free package plan
        data = {
            "id": package_plan.id,
            "name": "",  # Invalid name
            "usage_limit": -10,  # Invalid usage limit
            "price": -1,  # Invalid price
            "days": 0  # Invalid days
        }
        
        response = self.api_client.put(self.update_url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['status'] == 'FAILED'
        assert response.data['message'] == 'validation error'
        assert 'errors' in response.data
        assert 'usage_limit' in response.data['errors']
        assert 'price' in response.data['errors']
        assert 'days' in response.data['errors']

    def test_package_plan_update_duplicate_package(self):
        admin_user = self.users[0]  # Admin user
        token = self.mock_token(admin_user)
        self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        package_plan = self.package_plans[0]
        data = {
            "id": package_plan.id,
            "name": "limited_usage",
            "plan_type": PlanType.LIMITED_USAGE,
            "usage_limit": 0,
            "price": 14.99,
            "days": 30
        }
        
        response = self.api_client.put(self.update_url, data, format='json')
        print(response.data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['status'] == 'FAILED'
        assert response.data['message'] == 'validation error'
        assert response.data['errors']['name'] == 'Package plan with this name and package type already exists'
        
'''
invalid -> name, usage_limit, price, days, plan_type
'''