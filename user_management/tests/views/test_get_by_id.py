# import pytest
# from django.urls import reverse
# from rest_framework import status

# @pytest.mark.django_db
# class TestUserRetrieveByIdView:

#     def test_user_retrieves_own_data(self, api_client, mock_token, users):
#         user = users[1]
#         token = mock_token(user)
#         api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

#         url = reverse('user-retrieve')
#         response = api_client.get(url)

#         assert response.status_code == status.HTTP_200_OK
#         assert response.data['status'] == 'OK'
#         assert response.data['message'] == 'User data retrieved successfully'

#     def test_unauthorized_user_retrieves_users_data(self, api_client, mock_token, users):
#         api_client.credentials(HTTP_AUTHORIZATION='')

#         url = reverse('user-retrieve')
#         response = api_client.get(url)

#         assert response.status_code == status.HTTP_401_UNAUTHORIZED
#         assert response.data['detail'] == 'Authentication credentials were not provided.'
