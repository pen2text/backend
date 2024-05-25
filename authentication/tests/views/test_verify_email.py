# import pytest
# from django.urls import reverse
# from rest_framework import status
# from utils.jwt_token_utils import generate_jwt_token


# @pytest.mark.django_db
# class TestVerifyEmailView:

#     def test_verify_email_success(self, api_client, users, mock_jwt_token):
#         user = users[2] 
#         token = mock_jwt_token(user, 'email_verification')
        
#         url = reverse('verify-email', args=[token])
#         response = api_client.get(url)

#         assert response.status_code == status.HTTP_200_OK
#         user.refresh_from_db()
#         assert user.is_verified
#         assert response.data['message'] == 'Email verified successfully.'

#     def test_verify_email_invalid_token(self, api_client):
#         url = reverse('verify-email', args=['invalid-token'])

#         response = api_client.get(url)

#         assert response.status_code == status.HTTP_400_BAD_REQUEST
#         assert response.data['message'] == "Token get expired or invalid token, please request a new one."
