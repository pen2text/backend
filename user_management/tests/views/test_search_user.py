# import pytest
# from django.urls import reverse
# from rest_framework import status

# @pytest.fixture
# def search_url():
#     def url(name):
#         return reverse('user-search', kwargs={'name': name})
#     return url

# @pytest.mark.django_db
# class TestUserSearchByNameView:

#     @pytest.fixture(autouse=True)
#     def setup(self, search_url, api_client, mock_token, users):
#         self.search_url = search_url
#         self.api_client = api_client
#         self.mock_token = mock_token
#         self.users = users

#     def test_search_users_by_name(self):
#         user = self.users[0]
#         token = self.mock_token(user)
#         self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
#         url = self.search_url("doe")
#         response = self.api_client.get(url, format='json')

#         assert response.status_code == status.HTTP_200_OK
#         response_data = response.json()
#         assert response_data['status'] == 'OK'
#         assert response_data['message'] == 'Users retrieved successfully'
#         assert len(response_data['data']) == 1  

#     def test_search_users_with_empty_name(self):
#         user = self.users[0] # admin user
#         token = self.mock_token(user)
#         self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

#         url = self.search_url(' ')
#         response = self.api_client.get(url, format='json')

#         assert response.status_code == status.HTTP_200_OK
#         response_data = response.json()
#         assert response_data['status'] == 'OK'
#         assert response_data['message'] == 'Users retrieved successfully'
#         assert len(response_data['data']) == len(self.users)  # All users should be retrieved

#     def test_search_users_as_regular_user(self):
#         user = self.users[1] # regular user
#         token = self.mock_token(user)
#         self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

#         url = self.search_url('doe')
#         response = self.api_client.get(url, format='json')

#         assert response.status_code == status.HTTP_403_FORBIDDEN
#         response_data = response.json()
#         assert response_data['status'] == 'FAILED'
#         assert response_data['message'] == 'Forbidden: You do not have permission to access this resource'

#     def test_search_without_authentication(self):
#         url = self.search_url('doe')
#         response = self.api_client.get(url, format='json')

#         assert response.status_code == status.HTTP_401_UNAUTHORIZED
#         assert response.data['detail'] == 'Authentication credentials were not provided.'