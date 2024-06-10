import pytest
from django.urls import reverse
from rest_framework import status

@pytest.mark.django_db
class TestUserListView:

    def test_admin_retrieves_users_list(self, api_client, mock_token, users):
        admin_user = users[0]  # Admin user
        token = mock_token(admin_user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        url = reverse('user-list')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'OK'
        assert response.data['message'] == 'Users retrieved successfully'
        assert len(response.data['data']) == len(users)

    def test_user_forbidden_to_retrieve_users_list(self, api_client, mock_token, users):
        user = users[1]  # Regular user
        token = mock_token(user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        url = reverse('user-list')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data['status'] == 'FAILED'
        assert response.data['message'] == 'Forbidden: You do not have permission to access this resource'

    def test_unauthorized_user_retrieves_users_list(self, api_client, mock_token, users):
        api_client.credentials(HTTP_AUTHORIZATION='')

        url = reverse('user-list')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data['detail'] == 'Authentication credentials were not provided.'