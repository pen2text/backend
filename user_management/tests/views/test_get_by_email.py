import pytest
from django.urls import reverse
from rest_framework import status

@pytest.mark.django_db
class TestUserRetrieveByEmailView:
    def test_admin_retrieves_user_data(self, api_client, mock_token, users):
        admin_user = users[0]
        target_user = users[1]  # Non-admin user
        token = mock_token(admin_user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        url = reverse('user-retrieve-by-email', kwargs={'email': target_user.email})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['data']['email'] == target_user.email

    def test_user_retrieves_own_data(self, api_client, mock_token, users):
        user = users[1]  # Regular user
        token = mock_token(user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        url = reverse('user-retrieve-by-email', kwargs={'email': user.email})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['data']['email'] == user.email

    def test_user_retrieves_other_user_data(self, api_client, mock_token, users):
        user = users[1]  # Regular user
        token = mock_token(user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        other_user_email = users[0].email  # Admin user
        url = reverse('user-retrieve-by-email', kwargs={'email': other_user_email})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data['message'] == "Forbidden: You do not have permission to access this resource"

    def test_admin_retrieves_non_existent_user_data(self, api_client, mock_token, users):
        admin_user = users[0]  # Admin user
        token = mock_token(admin_user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        non_existent_user_email = 'nonexistent@example.com'
        url = reverse('user-retrieve-by-email', kwargs={'email': non_existent_user_email})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['message'] == "User not found with the provided email"

    def test_unauthorized_user_retrieves_users_data(self, api_client, mock_token, users):
        api_client.credentials(HTTP_AUTHORIZATION='')

        url = reverse('user-list')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data['detail'] == 'Authentication credentials were not provided.'