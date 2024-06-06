import pytest
from rest_framework import status
from django.urls import reverse
from unittest.mock import patch
# from package_manager.models import RemoteAPITokenManagers
# from package_manager.serializers import RemoteAPITokenManagerSerializer
# from rest_framework.exceptions import ValidationError

@pytest.fixture
def create_url():
    return reverse('remote-api-token-create')

@pytest.mark.django_db
class TestRemoteAPITokenManagerCreateView:
    
    @pytest.fixture(autouse=True)
    def setup(self, api_client, users, mock_token, remote_api_tokens):
        self.api_client = api_client
        self.users = users
        self.mock_token = mock_token
        self.remote_api_tokens = remote_api_tokens

    def test_remote_api_token_manager_create_unauthorized(self, create_url):
        response = self.api_client.post(create_url, {})
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert 'detail' in response.data
        assert response.data['detail'] == 'Authentication credentials were not provided.'

    def test_remote_api_token_manager_create_success(self, create_url):
        user = self.users[1]
        token = self.mock_token(user)
        self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        data = {'name': 'New Token'}
        # with patch('package_manager.views.generate_jwt_token', return_value='newly_generated_token'):
        response = self.api_client.post(create_url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['status'] == 'OK'
        assert response.data['message'] == 'Remote API Token Created'
        
        assert 'data' in response.data
        assert response.data['data']['name'] == 'New Token'
        # assert response.data['data']['token'] == 'newly_generated_token'

    def test_remote_api_token_manager_create_validation_error(self, create_url):
        user = self.users[1]
        token = self.mock_token(user)
        self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        data = {}  # Invalid data
        response = self.api_client.post(create_url, data)
        print(response.data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['status'] == 'FAILED'
        assert response.data['message'] == 'Validation Error'
        assert 'name' in response.data['errors']

    def test_remote_api_token_manager_create_limit_exceeded(self, create_url, settings):
        user = self.users[0]
        token = self.mock_token(user)
        self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
                
        data = {'name': 'New Token'}
        response = self.api_client.post(create_url, data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['status'] == 'FAILED'
        assert response.data['message'] == 'API Token Limit Exceeded'

