# import uuid
# import pytest
# from django.urls import reverse
# from rest_framework import status

# @pytest.mark.django_db
# class TestUpdateRoleView:
#     def test_update_role_by_admin(self, api_client, mock_token, users):
#         admin_user = users[0]
#         regular_user = users[1]
        
#         token = mock_token(admin_user)
#         api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')


#         update_data = {
#             'id': regular_user.id, 
#             'role': 'admin'
#         }

#         url = reverse('update-role')
#         response = api_client.patch(url, update_data)

#         assert response.status_code == status.HTTP_200_OK
#         assert response.data['status'] == 'OK'
#         assert response.data['message'] == 'Role updated successfully'
#         assert response.data['data']['role'] == 'admin'

#     def test_update_role_by_non_admin(self, api_client, mock_token, users):
#         regular_user = users[1]
#         admin_user = users[0]
        
#         token = mock_token(regular_user)
#         api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

#         update_data = {
#             'id': admin_user.id,  
#             'role': 'user'
#         }

#         url = reverse('update-role')
#         response = api_client.patch(url, update_data)

#         assert response.status_code == status.HTTP_403_FORBIDDEN
#         assert response.data['status'] == 'FAILED'
#         assert response.data['message'] == "Forbidden: You do not have permission to update user roles"

#     def test_update_role_nonexistent_user(self, api_client, mock_token, users):
#         admin_user = users[0] 
#         token = mock_token(admin_user)
#         api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

#         non_existent_user_id = uuid.uuid4()
#         update_data = {
#             'id': non_existent_user_id,  
#             'role': 'user'
#         }

#         url = reverse('update-role')
#         response = api_client.patch(url, update_data)

#         assert response.status_code == status.HTTP_404_NOT_FOUND
#         assert response.data['status'] == 'FAILED'
#         assert response.data['message'] == 'User does not exist'
        
#     def test_user_cannot_update_own_role(self, api_client, users, mock_token):
#         url = reverse('update-role')

#         admin_user = users[0]

#         regular_user_token = mock_token(admin_user)
#         api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(regular_user_token))

#         update_data = {
#             'id': str(admin_user.id),
#             'role': 'admin'
#         }

#         response = api_client.patch(url, update_data, format='json')

#         assert response.status_code == status.HTTP_400_BAD_REQUEST
#         assert response.data['status'] == 'FAILED'
#         assert response.data['message'] == 'Validation failed'
#         assert 'errors' in response.data
#         assert 'id' in response.data['errors']
        
#     def test_update_role_invalid_role(self, api_client, users, mock_token):
#         url = reverse('update-role')

#         admin_user = users[0]

#         regular_user_token = mock_token(admin_user)
#         api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(regular_user_token))

#         update_data = {
#             'id': str(users[1].id),
#             'role': 'invalid-role'
#         }

#         response = api_client.patch(url, update_data, format='json')

#         assert response.status_code == status.HTTP_400_BAD_REQUEST
#         assert response.data['status'] == 'FAILED'
#         assert response.data['message'] == 'Validation failed'
#         assert 'errors' in response.data
#         assert 'role' in response.data['errors']