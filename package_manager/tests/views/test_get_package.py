import uuid
import pytest
from rest_framework import status
from django.urls import reverse


@pytest.fixture
def url(package_plans):
    return reverse('package-plan-retrieve', args=[package_plans[0].id])

@pytest.mark.django_db
class TestPackagePlanDetailRetrieve:
    
    @pytest.fixture(autouse=True)
    def setup(self, api_client, users, mock_token, package_plans, url):
        self.api_client = api_client
        self.users = users
        self.mock_token = mock_token
        self.package_plans = package_plans
        self.url = url

    def test_package_plan_detail_retrieve(self):
        user = self.users[0]
        token = self.mock_token(user)
        self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        response = self.api_client.get(self.url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'OK'
        assert response.data['message'] == 'Package fetched successfully'
        data = response.data['data']
        plan = self.package_plans[0]
        assert data['name'] == plan.name
        assert data['plan_type'] == plan.plan_type
        assert data['usage_limit'] == plan.usage_limit
        assert data['price'] == plan.price
        assert data['days'] == plan.days

    def test_package_plan_detail_retrieve_unauthorized(self):
        response = self.api_client.get(self.url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert 'detail' in response.data
        assert response.data['detail'] == 'Authentication credentials were not provided.'

    def test_package_plan_detail_retrieve_non_existent(self):
        user = self.users[0]
        token = self.mock_token(user)
        self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        non_existent_uuid = uuid.uuid4()
        non_existent_url = reverse('package-plan-retrieve', args=[non_existent_uuid])
        
        response = self.api_client.get(non_existent_url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['status'] == 'FAILED'
        assert response.data['message'] == 'Package not found'