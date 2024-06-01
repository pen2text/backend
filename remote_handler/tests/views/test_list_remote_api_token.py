# import pytest
# from rest_framework import status
# from django.urls import reverse


# @pytest.fixture
# def list_url():
#     return reverse('remote-api-token-list')

# @pytest.mark.django_db
# class TestRemoteAPITokenManagerListView:
    
#     @pytest.fixture(autouse=True)
#     def setup(self, api_client, users, mock_token, list_url, remote_api_tokens):
#         self.api_client = api_client
#         self.users = users
#         self.mock_token = mock_token
#         self.list_url = list_url
#         self.remote_api_tokens = remote_api_tokens

#     def test_remote_api_token_manager_list_unauthorized(self):
#         response = self.api_client.get(self.list_url)
        
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED
#         assert 'detail' in response.data
#         assert response.data['detail'] == 'Authentication credentials were not provided.'

#     def test_remote_api_token_manager_list_authorized(self):
#         user = self.users[0]
#         token = self.mock_token(user)
#         self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
#         response = self.api_client.get(self.list_url)
        
#         assert response.status_code == status.HTTP_200_OK
#         assert response.data['status'] == 'OK'
#         assert response.data['message'] == 'Remote API Token List'
#         assert len(response.data['data']) == 3
#         assert 'data' in response.data
        
#         for token_data in response.data['data']:
#             assert 'token' not in token_data  
#             assert 'name' in token_data

