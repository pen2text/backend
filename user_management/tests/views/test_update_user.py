import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.hashers import check_password



@pytest.mark.django_db
class TestUserUpdateView:

    def test_update_own_information(self, api_client, mock_token, users):
        user = users[0]
        token = mock_token(user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        url = reverse('user-update')
        data = {'id': user.id, 'first_name': 'New Name'}

        response = api_client.patch(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data['status'] == 'OK'
        assert response_data['message'] == 'User information updated successfully'
        assert response_data['data']['first_name'] == 'New Name'
        
    def test_update_other_user_information(self, api_client, mock_token, users):
        user = users[1]
        token = mock_token(user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        other_user = users[0]
        url = reverse('user-update')
        data = {'id': other_user.id, 'first_name': 'New Name'}
        response = api_client.patch(url, data, format='json')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_with_invalid_data(self, api_client, mock_token, users):
        user = users[0]
        token = mock_token(user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        url = reverse('user-update')
        data = {'id': user.id, 'date_of_birth': 'invalid_email'}
        response = api_client.put(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['status'] == 'FAILED'
        assert response.data['message'] == 'Validation failed'
        assert 'date_of_birth' in response.data['errors']

    def test_update_password(self, api_client, mock_token, users):
        user = users[0]
        token = mock_token(user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        url = reverse('user-update')
        data = {
            'id': user.id,
            'password': 'NewPassword123!',
            'old_password': 'JaneDoe123!'
        }
        response = api_client.patch(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        # user.refresh_from_db()
        # assert check_password('JaneDoe123!', user.password)  # Assert old password
        # assert check_password('NewPassword123!', user.password)  # Assert new password

    def test_update_password_without_old_password(self, api_client, mock_token, users):
        user = users[0]
        token = mock_token(user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        url = reverse('user-update')
        data = {
            'id': user.id,
            'password': 'NewPassword123!',
        }
        response = api_client.patch(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['status'] == 'FAILED'
        assert response.data['message'] == 'Validation failed'
        assert 'password' in response.data['errors']

    def test_update_password_with_incorrect_old_password(self, api_client, mock_token, users):
        user = users[0]
        token = mock_token(user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        url = reverse('user-update')
        data = {
            'id': user.id,
            'password': 'NewPassword123!',
            'old_password': 'IncorrectOldPassword'
        }
        response = api_client.patch(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['status'] == 'FAILED'
        assert response.data['message'] == 'Validation failed'
        assert 'old_password' in response.data['errors']

