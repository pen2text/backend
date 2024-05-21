# from unittest.mock import patch
# import pytest
# from rest_framework import status
# from django.urls import reverse


# @pytest.fixture
# def mock_send_verification_email():
#     with patch('user_management.views.send_verification_email') as mock:
#         yield mock

# @pytest.mark.django_db
# class TestUserRegistrationView:
    
#     def test_logged_in_user_registration_forbidden(self, api_client, mock_token, users):
#         logged_in_user = users[0] 
#         token = mock_token(logged_in_user)
#         api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

#         url = reverse('user-register')
#         data = {
#             'first_name': 'New',
#             'last_name': 'User',
#             'gender': 'female',
#             'date_of_birth': '1995-05-20',
#             'email': 'new.user@example.com',
#             'password': 'NewUser123!',
#         }
        
#         response = api_client.post(url, data, format='json')

#         assert response.status_code == status.HTTP_403_FORBIDDEN
#         assert response.data['status'] == 'FAILED'
#         assert response.data['message'] == 'Forbidden: You are already logged in'

#     def test_anonymous_user_registration(self, api_client, mock_send_verification_email):
#         url = reverse('user-register')
#         data = {
#             'first_name': 'New',
#             'last_name': 'User',
#             'gender': 'female',
#             'date_of_birth': '1995-05-20',
#             'email': 'new.user@example.com',
#             'password': 'NewUser123!',
#         }
        
#         response = api_client.post(url, data, format='json')

#         assert response.status_code == status.HTTP_201_CREATED
#         assert response.data['status'] == 'OK'
#         assert response.data['message'] == 'User registered successfully'
#         assert 'id' in response.data['data']

#         mock_send_verification_email.assert_called_once()

#     def test_anonymous_user_registration_validation_error(self, api_client):
#         url = reverse('user-register')
#         data = {
#             'first_name': '',
#             'last_name': 'User',
#             'gender': 'female',
#             'date_of_birth': '1995-05-20',
#             'email': 'invalid-email',
#             'password': 'short',
#         }
        
#         response = api_client.post(url, data, format='json')

#         assert response.status_code == status.HTTP_400_BAD_REQUEST
#         assert response.data['status'] == 'FAILED'
#         assert response.data['message'] == 'Validation failed'
#         assert 'errors' in response.data
#         assert 'first_name' in response.data['errors']