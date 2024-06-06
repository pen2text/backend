import pytest
from django.urls import reverse
from rest_framework import status

@pytest.mark.django_db
class TestUserRetrieveByIdView:
    
    @pytest.fixture(autouse=True)
    def setup(self, users, mock_token, api_client, package_plans):
        self.url = reverse('user-retrieve')
        self.users = users
        self.mock_token = mock_token
        self.api_client = api_client
        self.package_plans = package_plans

    def test_user_retrieves_own_data(self):
        user = self.users[0]
        token = self.mock_token(user)
        self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        response = self.api_client.get(self.url)        

        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'OK'
        assert response.data['message'] == 'User data retrieved successfully'

    def test_unauthorized_user_retrieves_users_data(self):
        self.api_client.credentials(HTTP_AUTHORIZATION='')

        response = self.api_client.get(self.url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data['detail'] == 'Authentication credentials were not provided.'
