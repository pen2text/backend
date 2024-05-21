# import pytest
# from django.urls import reverse
# from rest_framework import status
# from utils.jwt_token_utils import generate_jwt_token


# @pytest.mark.django_db
# class TestVerifyEmailView:

#     def test_verify_email_success(self, api_client, users):
#         user = users[2] 
#         payload = {
#             'email': user.email,
#             'id': str(user.id),
#             'token_type': 'email_verification'
#         } 
#         token = generate_jwt_token(payload)
        
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
#         assert response.data['message'] == "Invalid token or token get expired"
