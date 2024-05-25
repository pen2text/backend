# import pytest
# from django.urls import reverse
# from rest_framework import status
# from unittest.mock import patch


# @pytest.mark.django_db
# class TestResetPasswordView:

#     def test_reset_password_success(self, api_client, users, mock_jwt_token):
    
#         user = users[0]
#         token = mock_jwt_token(user, 'password_reset')
        
#         url = reverse('reset-password')
#         data = {
#             'token': token,
#             'password': 'NewPassword123!'
#         }
#         response = api_client.put(url, data, format='json')

#         assert response.status_code == status.HTTP_200_OK
#         assert response.data['message'] == 'Password updated successfully'
#         user.refresh_from_db()
#         assert user.check_password('NewPassword123!')

#     def test_reset_password_validation_error(self, api_client, users, mock_jwt_token):
#         token = mock_jwt_token(users[0], 'password_reset')
#         url = reverse('reset-password')
#         data = {
#             'token': token,
#         }
#         response = api_client.put(url, data, format='json')

#         assert response.status_code == status.HTTP_400_BAD_REQUEST
#         assert response.data['message'] == 'Validation error'
#         assert 'errors' in response.data
#         assert 'password' in response.data['errors']
#         assert  'token' not in response.data['errors']

#     def test_reset_password_invalid_token(self, api_client, users, mock_jwt_token):
#         url = reverse('reset-password')
#         token = mock_jwt_token(users[0], 'invalid_token')
        
#         data = {
#             'token': token,
#             'password': 'NewPassword123!'
#         }
#         response = api_client.put(url, data, format='json')

#         assert response.status_code == status.HTTP_400_BAD_REQUEST
#         assert response.data['message'] == 'Validation error'

#     def test_reset_password_invalid_password(self, api_client, users, mock_jwt_token):
#         token = mock_jwt_token(users[0], 'password_reset')
#         url = reverse('reset-password')
#         data = {
#             'token': token,
#             'password': 'invalid_password'
#         }
#         response = api_client.put(url, data, format='json')

#         assert response.status_code == status.HTTP_400_BAD_REQUEST
#         assert response.data['message'] == 'Validation error'
#         assert 'errors' in response.data
#         assert 'password' in response.data['errors']
#         assert  'token' not in response.data['errors']