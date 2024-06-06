import pytest
from django.urls import reverse
from rest_framework import status

@pytest.fixture
def url():
    return reverse('user-update')

@pytest.mark.django_db
class TestUserUpdateView:

    @pytest.fixture(autouse=True)
    def setup(self, api_client, mock_token, users, url):
        self.api_client = api_client
        self.mock_token = mock_token
        self.users = users
        self.url = url

    def test_update_success(self):
        user = self.users[0]
        token = self.mock_token(user)
        self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        data = {'first_name': 'New Name'}

        response = self.api_client.patch(self.url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'OK'
        assert response.data['message'] == 'User information updated successfully'
        assert response.data['data']['first_name'] == 'New Name'
        
    def test_update_with_invalid_data(self):
        user = self.users[0]
        token = self.mock_token(user)
        self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        data = {'date_of_birth': 'invalid_date'}
        response = self.api_client.patch(self.url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        response_data = response.json()
        assert response_data['status'] == 'FAILED'
        assert response_data['message'] == 'Validation failed'
        assert 'date_of_birth' in response_data['errors']

    def test_update_password_success(self):
        user = self.users[0]
        token = self.mock_token(user)
        self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        data = {
            'password': 'NewPassword123!',
            'old_password': 'JaneDoe123!'
        }
        response = self.api_client.patch(self.url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data['status'] == 'OK'
        assert response_data['message'] == 'User information updated successfully'
        user.refresh_from_db()
        assert user.check_password('NewPassword123!')

    def test_update_password_without_old_password_failed(self):
        user = self.users[0]
        token = self.mock_token(user)
        self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        data = {
            'password': 'NewPassword123!',
        }
        response = self.api_client.patch(self.url, data, format='json')
        print("response", response.data)


        assert response.status_code == status.HTTP_400_BAD_REQUEST
        response_data = response.json()
        assert response_data['status'] == 'FAILED'
        assert response_data['message'] == 'Validation failed'
        assert 'old_password' in response_data['errors']

    def test_update_password_with_incorrect_old_password_failed(self):
        user = self.users[0]
        token = self.mock_token(user)
        self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        data = {
            'password': 'NewPassword123!',
            'old_password': 'IncorrectOldPassword'
        }
        response = self.api_client.patch(self.url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        response_data = response.json()
        assert response_data['status'] == 'FAILED'
        assert response_data['message'] == 'Validation failed'
        assert 'old_password' in response_data['errors']
