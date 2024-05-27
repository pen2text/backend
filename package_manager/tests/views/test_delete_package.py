# import uuid
# import pytest
# from rest_framework import status
# from django.urls import reverse
# from package_manager.models import PackagePlanDetails

# @pytest.fixture
# def url(package_plans):
#     return reverse('package-plan-delete', args=[package_plans[0].id])

# @pytest.mark.django_db
# class TestPackagePlanDetailDelete:
    
#     @pytest.fixture(autouse=True)
#     def setup(self, api_client, users, mock_token, package_plans, url):
#         self.api_client = api_client
#         self.users = users
#         self.mock_token = mock_token
#         self.package_plans = package_plans
#         self.url = url

#     def test_package_plan_detail_delete(self):
#         user = self.users[0]  # Admin user
#         token = self.mock_token(user)
#         self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
#         response = self.api_client.delete(self.url)
        
#         assert response.status_code == status.HTTP_200_OK
#         assert response.data['status'] == 'OK'
#         assert response.data['message'] == 'Package deleted successfully'
#         assert not PackagePlanDetails.objects.filter(id=self.package_plans[0].id).exists()

#     def test_package_plan_detail_delete_unauthorized(self):
#         response = self.api_client.delete(self.url)
        
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED
#         assert 'detail' in response.data
#         assert response.data['detail'] == 'Authentication credentials were not provided.'

#     def test_package_plan_detail_delete_non_admin(self):
#         non_admin_user = self.users[1]  # Non-admin user
#         token = self.mock_token(non_admin_user)
#         self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
#         response = self.api_client.delete(self.url)
        
#         assert response.status_code == status.HTTP_403_FORBIDDEN
#         assert response.data['status'] == 'FAILED'
#         assert response.data['message'] == 'You are not authorized to delete plan'

#     def test_package_plan_detail_delete_non_existent(self):
#         user = self.users[0]  # Admin user
#         token = self.mock_token(user)
#         self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
#         non_existent_uuid = uuid.uuid4()
#         non_existent_url = reverse('package-plan-delete', args=[non_existent_uuid])
        
#         response = self.api_client.delete(non_existent_url)
        
#         assert response.status_code == status.HTTP_404_NOT_FOUND
#         assert response.data['status'] == 'FAILED'
#         assert response.data['message'] == 'Package not found'