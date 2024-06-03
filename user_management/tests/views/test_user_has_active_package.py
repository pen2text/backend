# import pytest
# from django.urls import reverse
# from rest_framework import status


# @pytest.mark.django_db
# class TestUserHasActivePremierPackageView:

#     @pytest.fixture(autouse=True)
#     def setup(self, api_client, users, mock_token, unlimited_usage_subscription_plans):
#         self.api_client = api_client
#         self.users = users
#         self.mock_token = mock_token
#         self.unlimited_usage_subscription_plans = unlimited_usage_subscription_plans
#         self.url = reverse('user-has-active-premier-package')
    
#     def test_user_has_active_premier_package(self):
#         user = self.users[0]
        
#         token = self.mock_token(user)
#         self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
#         response = self.api_client.get(self.url)
        
#         assert response.status_code == status.HTTP_200_OK
#         assert response.data['status'] == 'OK'
#         assert response.data['message'] == 'User active premier package status fetched successfully'
#         assert response.data['data']['is_premier'] is True

#     def test_user_has_no_active_premier_package(self):
#         user = self.users[1]  
        
#         token = self.mock_token(user)
#         self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
#         response = self.api_client.get(self.url)
        
#         assert response.status_code == status.HTTP_200_OK
#         assert response.data['status'] == 'OK'
#         assert response.data['message'] == 'User active premier package status fetched successfully'
#         assert response.data['data']['is_premier'] is False

#     def test_user_has_no_active_premier_package_without_authentication(self):
#         response = self.api_client.get(self.url)

#         assert response.status_code == status.HTTP_401_UNAUTHORIZED
#         assert response.data['detail'] == 'Authentication credentials were not provided.'
