# from package_manager.models import PlanType
# import pytest
# from rest_framework import status
# from django.urls import reverse


# @pytest.fixture
# def url():
#     return reverse('package-plan-list')

# @pytest.mark.django_db
# class TestPackagePlanDetailList:
    
#     @pytest.fixture(autouse=True)
#     def setup(self, api_client, users, mock_token, package_plans, url):
#         self.api_client = api_client
#         self.users = users
#         self.mock_token = mock_token
#         self.package_plans = package_plans
#         self.url = url

#     def test_package_plan_detail_list(self):
#         user = self.users[0]
#         token = self.mock_token(user)
#         self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
#         response = self.api_client.get(self.url)
        
#         assert response.status_code == status.HTTP_200_OK
#         assert response.data['status'] == 'OK'
#         assert response.data['message'] == 'Plans fetched successfully'
#         assert len(response.data['data']) == len(self.package_plans)

#         for plan in response.data['data']:
#             assert 'name' in plan
#             assert 'plan_type' in plan
#             assert 'usage_limit' in plan
#             assert 'price' in plan
#             assert 'days' in plan
#             assert plan['plan_type'] in PlanType.values

#     def test_package_plan_detail_list_unauthorized(self):
#         response = self.api_client.get(self.url)
        
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED
#         assert 'detail' in response.data
#         assert response.data['detail'] == 'Authentication credentials were not provided.'

#     def test_package_plan_detail_list_non_admin(self):
#         non_admin_user = self.users[1]
#         token = self.mock_token(non_admin_user)
#         self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
#         response = self.api_client.get(self.url)
        
#         assert response.status_code == status.HTTP_200_OK
