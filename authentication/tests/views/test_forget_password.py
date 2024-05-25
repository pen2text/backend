# from unittest.mock import patch
# import pytest
# from django.urls import reverse
# from rest_framework import status

# @pytest.fixture
# def mock_send_reset_password_email():
#     with patch('authentication.views.send_reset_password_email') as mock:
#         yield mock
        
# @pytest.mark.django_db
# class TestForgotPasswordView:

#     def test_forgot_password_success(self, mock_send_reset_password_email, api_client, users):
#         user = users[1]  
#         mock_send_reset_password_email.return_value = True
#         url = reverse('forgot-password', args=[user.email])
#         response = api_client.get(url)

#         assert response.status_code == status.HTTP_200_OK
#         assert response.data['status'] == 'OK'
#         assert response.data['message'] == 'Password reset email has been sent'
#         mock_send_reset_password_email.assert_called_once_with(user)

#     def test_forgot_password_user_not_exist(self, mock_send_reset_password_email, api_client):
#         url = reverse('forgot-password', args=['nonexistent@example.com'])
#         response = api_client.get(url)

#         assert response.status_code == status.HTTP_400_BAD_REQUEST
#         assert response.data['status'] == 'FAILED'
#         assert response.data['message'] == 'User with this email does not exist'
#         mock_send_reset_password_email.assert_not_called()

#     def test_forgot_password_no_email_provided(self, mock_send_reset_password_email, api_client):
#         url = reverse('forgot-password', args=[' '])
#         response = api_client.get(url)

#         assert response.status_code == status.HTTP_400_BAD_REQUEST
#         assert response.data['message'] == 'Email is required'
#         mock_send_reset_password_email.assert_not_called()

#     def test_forgot_password_email_send_fail(self, mock_send_reset_password_email, api_client, users):
#         user = users[1] 
#         mock_send_reset_password_email.return_value = False
#         url = reverse('forgot-password', args=[user.email])
#         response = api_client.get(url)

#         assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
#         assert response.data['message'] == 'An error occurred while sending the email. Please try again later.'
#         mock_send_reset_password_email.assert_called_once_with(user)
