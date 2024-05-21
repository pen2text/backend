# from unittest.mock import patch
# import pytest
# from django.urls import reverse
# from rest_framework import status


# @pytest.fixture
# def mock_send_verification_email():
#     with patch('authentication.views.send_verification_email') as mock:
#         yield mock
        
# @pytest.mark.django_db
# class TestLoginView:

#     def test_successful_login(self, api_client, users):
#         user = users[1]

#         url = reverse('token-obtain-pair')
#         data = {
#             'email': user.email,
#             'password': 'JohnSmith123!',
#         }
        
#         response = api_client.post(url, data, format='json')

#         assert response.status_code == status.HTTP_200_OK
#         assert response.data['status'] == 'OK'
#         assert response.data['message'] == 'User logged in successfully.'
#         assert 'access_token' in response.data['data']
#         assert 'refresh_token' in response.data['data']

#     def test_login_with_unverified_email(self, api_client, users, mock_send_verification_email):
#         user = users[2]

#         url = reverse('token-obtain-pair')
#         data = {
#             'email': user.email,
#             'password': 'AliceJohnson123!',
#         }
        
#         response = api_client.post(url, data, format='json')

#         assert response.status_code == status.HTTP_400_BAD_REQUEST
#         assert response.data['status'] == 'FAILED'
#         assert response.data['message'] == 'Please verify your email address, email has been sent.'
        
#         mock_send_verification_email.assert_called_once_with(user)

#     def test_login_with_wrong_credentials(self, api_client, users):
#         user = users[1]  

#         url = reverse('token-obtain-pair')
#         data = {
#             'email': user.email,
#             'password': 'WrongPassword123!',
#         }
        
#         response = api_client.post(url, data, format='json')

#         assert response.status_code == status.HTTP_400_BAD_REQUEST
#         assert response.data['status'] == 'FAILED'
#         assert response.data['message'] == 'Wrong email or password'

#     def test_login_with_validation_error(self, api_client):
#         url = reverse('token-obtain-pair')
#         data = {
#             'email': 'invalid-email',
#             'password': '',
#         }
        
#         response = api_client.post(url, data, format='json')

#         assert response.status_code == status.HTTP_400_BAD_REQUEST
#         assert response.data['status'] == 'FAILED'
#         assert response.data['message'] == 'Validation error'
#         assert 'errors' in response.data
#         assert 'email' in response.data['errors']
        
#     def test_logged_in_user_tries_to_login(self, api_client, users, mock_token):
#         user = users[0]  
#         token = mock_token(user)
        
#         api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
#         url = reverse('token-obtain-pair')
#         data = {
#             'email': user.email,
#             'password': 'JaneDoe123!',
#         }
        
#         response = api_client.post(url, data, format='json')

#         assert response.status_code == status.HTTP_403_FORBIDDEN
#         assert response.data['status'] == 'FAILED'
#         assert response.data['message'] == 'Forbidden: You are already logged in'
