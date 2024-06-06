import pytest
from django.urls import reverse
from rest_framework import status
from user_management.models import Users

@pytest.mark.django_db
class TestUserDeleteView:

    def test_admin_deletes_user(self, api_client, mock_token, users):
        admin_user = users[0]  # Admin user
        target_user = users[1]  # Non-admin user
        token = mock_token(admin_user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        url = reverse('user-delete', kwargs={'id': target_user.id})
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'OK'
        assert response.data['message'] == 'User deleted successfully'

        # Check if the user has been deleted from the database
        with pytest.raises(Users.DoesNotExist):
            Users.objects.get(id=target_user.id)

    def test_user_forbidden_to_delete_user(self, api_client, mock_token, users):
        user = users[1]  # Regular user
        target_user = users[0]  # Admin user
        token = mock_token(user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        url = reverse('user-delete', kwargs={'id': target_user.id})
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data['status'] == 'FAILED'
        assert response.data['message'] == 'Forbidden: You do not have permission to access this resource'

    def test_user_deletes_own_account(self, api_client, mock_token, users):
        user = users[1]  # Regular user
        token = mock_token(user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        url = reverse('user-delete', kwargs={'id': user.id})
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'OK'
        assert response.data['message'] == 'User deleted successfully'

        # Check if the user has been deleted from the database
        with pytest.raises(Users.DoesNotExist):
            Users.objects.get(id=user.id)

    def test_non_existent_user_delete(self, api_client, mock_token, users):
        admin_user = users[0]  # Admin user
        token = mock_token(admin_user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        non_existent_user_id = '999e4567-e89b-12d3-a456-426614174099'
        url = reverse('user-delete', kwargs={'id': non_existent_user_id})
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['status'] == 'FAILED'
        assert response.data['message'] == 'User not found with the provided ID'

    def test_unauthorized_user_cannot_delete_user(self, api_client, users):
        target_user = users[2]  
        api_client.credentials(HTTP_AUTHORIZATION='')

        url = reverse('user-delete', kwargs={'id': target_user.id})
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data['detail'] == 'Authentication credentials were not provided.'