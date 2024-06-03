# import pytest
# from django.urls import reverse
# from rest_framework import status

# @pytest.mark.django_db
# def test_token_verify_valid(api_client, users, mock_token):
#     user = users[0]  
#     token = mock_token(user)
    
#     api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(token))
#     url = reverse('token-verify')
#     response = api_client.get(url)
    
#     assert response.status_code == status.HTTP_200_OK
#     assert response.data['status'] == 'OK'
#     assert response.data['message'] == 'Token is valid'

# @pytest.mark.django_db
# def test_token_verify_invalid(api_client):
#     api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + 'invalidtoken')
#     url = reverse('token-verify')
#     response = api_client.get(url)
    
#     assert response.status_code == status.HTTP_401_UNAUTHORIZED
#     assert 'detail' in response.data
