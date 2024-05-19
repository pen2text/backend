# import pytest
# from django.urls import reverse
# from rest_framework import status

# @pytest.mark.django_db
# class TestCheckEmailExistsView:

#     def test_check_existing_email(self, api_client, users):
#         existing_email = users[0].email  
#         url = reverse('check-email-exists', kwargs={'email': existing_email})
#         response = api_client.get(url)

#         assert response.status_code == status.HTTP_200_OK
#         assert response.data['status'] == 'OK'
#         assert response.data['message'] == 'Email exists'

#     def test_check_non_existing_email(self, api_client):
#         non_existing_email = 'nonexistent@example.com'
#         url = reverse('check-email-exists', kwargs={'email': non_existing_email})
#         response = api_client.get(url)

#         assert response.status_code == status.HTTP_404_NOT_FOUND
#         assert response.data['status'] == 'OK'
#         assert response.data['message'] == 'Email does not exists'

#     def test_check_with_out_email(self, api_client):
#         url = reverse('check-email-exists', kwargs={'email': ' '})
#         response = api_client.get(url)

#         assert response.status_code == status.HTTP_400_BAD_REQUEST
#         assert response.data['status'] == 'FAILED'
#         assert response.data['message'] == 'Email is required'

#     def test_check_invalid_email(self, api_client):
#         invalid_email = 'invalid_email'
#         url = reverse('check-email-exists', kwargs={'email': invalid_email})
#         response = api_client.get(url)

#         assert response.status_code == status.HTTP_404_NOT_FOUND
#         assert response.data['status'] == 'OK'
#         assert response.data['message'] == 'Email does not exists'
