# import pytest
# from rest_framework import status
# from django.urls import reverse
# from package_manager.models import PackagePlanDetails, PlanType

# @pytest.fixture
# def create_url():
#     return reverse('package-plan-create')

# @pytest.mark.django_db
# class TestPackagePlanDetailCreate:
    
#     @pytest.fixture(autouse=True)
#     def setup(self, api_client, users, mock_token, create_url, package_plans):
#         self.api_client = api_client
#         self.users = users
#         self.mock_token = mock_token
#         self.create_url = create_url
#         self.package_plans = package_plans

#     def test_package_plan_create_unauthorized(self):
#         data = {
#             "name": "premium",
#             "plan_type": PlanType.CUSTOM_LIMITED_USAGE,
#             "usage_limit": 100,
#             "price": 9.99,
#             "days": 30
#         }
        
#         response = self.api_client.post(self.create_url, data, format='json')
        
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED
#         assert 'detail' in response.data
#         assert response.data['detail'] == 'Authentication credentials were not provided.'

#     def test_package_plan_create_non_admin(self):
#         non_admin_user = self.users[1]  # Non-admin user
#         token = self.mock_token(non_admin_user)
#         self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
#         data = {
#             "name": "premium",
#             "plan_type": PlanType.CUSTOM_LIMITED_USAGE,
#             "usage_limit": 100,
#             "price": 9.99,
#             "days": 30
#         }
        
#         response = self.api_client.post(self.create_url, data, format='json')
        
#         assert response.status_code == status.HTTP_403_FORBIDDEN
#         assert response.data['status'] == 'FAILED'
#         assert response.data['message'] == 'You are not authorized to create plan'

#     def test_package_plan_create_invalid_data(self):
#         user = self.users[0]  # Admin user
#         token = self.mock_token(user)
#         self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
#         data = {
#             "name": "",  # Invalid name
#             "plan_type": PlanType.CUSTOM_LIMITED_USAGE,
#             "usage_limit": -1,  # Invalid usage limit
#             "price": -5,  # Invalid price
#             "days": 0  # Invalid days
#         }
        
#         response = self.api_client.post(self.create_url, data, format='json')
        
#         assert response.status_code == status.HTTP_400_BAD_REQUEST
#         assert response.data['status'] == 'FAILED'
#         assert response.data['message'] == 'validation error'
#         assert 'errors' in response.data
#         assert 'name' in response.data['errors']
#         assert 'usage_limit' in response.data['errors']
#         assert 'price' in response.data['errors']
#         assert 'days' in response.data['errors']

#     @pytest.mark.parametrize("plan_type, usage_limit, price, days", [
#         # (PlanType.FREE_PACKAGE, 10, 0, 1),
#         # (PlanType.FREE_UNREGISTERED_PACKAGE, 5, 0, 7),
#         # (PlanType.PREMIER_TRIAL_PACKAGE, 20, 0, 30),
#         (PlanType.NON_EXPIRING_LIMITED_USAGE, 50, 29.99, 0),
#         (PlanType.UNLIMITED_USAGE, 0, 49.99, 30),
#         (PlanType.LIMITED_USAGE, 100, 19.99, 30),
#         (PlanType.CUSTOM_LIMITED_USAGE, 200, 59.99, 60),
#     ])
#     def test_package_plan_create_various_plan_types(self, plan_type, usage_limit, price, days):
#         user = self.users[0]  # Admin user
#         token = self.mock_token(user)
#         self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
#         name = plan_type[:20]
#         data = {
#             "name": name,
#             "plan_type": plan_type,
#             "usage_limit": usage_limit,
#             "price": price,
#             "days": days
#         }
        
#         response = self.api_client.post(self.create_url, data, format='json')
                
#         assert response.status_code == status.HTTP_201_CREATED
#         assert response.data['status'] == 'OK'
#         assert response.data['message'] == 'Package plan created successfully'
        
#         assert 'data' in response.data
#         assert response.data['data']['name'] == data['name']
#         assert response.data['data']['plan_type'] == data['plan_type']
#         assert response.data['data']['usage_limit'] == data['usage_limit']
#         assert response.data['data']['price'] == data['price']
#         assert response.data['data']['days'] == data['days']

#     @pytest.mark.parametrize("plan_type", [
#         (PlanType.FREE_PACKAGE), 
#         (PlanType.FREE_UNREGISTERED_PACKAGE), 
#         (PlanType.PREMIER_TRIAL_PACKAGE)
#     ])   
#     def test_free_package_plans_create_duplicate_failed(self, plan_type):
#         user = self.users[0]  # Admin user
#         token = self.mock_token(user)
#         self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
#         name = plan_type[:20]
#         data = {
#             "name": name,
#             "plan_type": plan_type,
#             "usage_limit": 10,
#             "price": 0,
#             "days": 1
#         }
        
#         response = self.api_client.post(self.create_url, data, format='json')
        
#         assert response.status_code == status.HTTP_400_BAD_REQUEST
#         assert response.data['status'] == 'FAILED'
#         assert 'errors' in response.data
#         assert 'plan_type' in response.data['errors']
#         assert response.data['errors']['plan_type'] == 'This Package plan type already exists'
        

#     def test_package_plan_create_invalid_price(self):
#         user = self.users[0]  # Admin user
#         token = self.mock_token(user)
#         self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
#         data = {
#             "name": 'custom',
#             "plan_type": PlanType.CUSTOM_LIMITED_USAGE,
#             "usage_limit": 10,
#             "price": 0,
#             "days": 1
#         }
        
#         response = self.api_client.post(self.create_url, data, format='json')
        
#         assert response.status_code == status.HTTP_400_BAD_REQUEST
#         assert response.data['status'] == 'FAILED'
#         assert 'errors' in response.data
#         assert 'price' in response.data['errors']
#         assert response.data['errors']['price'] == 'Package price must be greater than 0'
        
#     def test_package_plan_create_invalid_days(self):
#         user = self.users[0]  # Admin user
#         token = self.mock_token(user)
#         self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
#         data = {
#             "name": 'custom',
#             "plan_type": PlanType.CUSTOM_LIMITED_USAGE,
#             "usage_limit": 10,
#             "price": 10,
#             "days": 0
#         }
        
#         response = self.api_client.post(self.create_url, data, format='json')
        
#         assert response.status_code == status.HTTP_400_BAD_REQUEST
#         assert response.data['status'] == 'FAILED'
#         assert 'errors' in response.data
#         assert 'days' in response.data['errors']
#         assert response.data['errors']['days'] == 'Days must be greater than 0'
        
#     def test_package_plan_create_invalid_usage_limit(self):
#         user = self.users[0]  # Admin user
#         token = self.mock_token(user)
#         self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
#         data = {
#             "name": 'custom',
#             "plan_type": PlanType.CUSTOM_LIMITED_USAGE,
#             "usage_limit": 0,
#             "price": 10,
#             "days": 1
#         }
        
#         response = self.api_client.post(self.create_url, data, format='json')
        
#         assert response.status_code == status.HTTP_400_BAD_REQUEST
#         assert response.data['status'] == 'FAILED'
#         assert 'errors' in response.data
#         assert 'usage_limit' in response.data['errors']
#         assert response.data['errors']['usage_limit'] == 'Usage limit must be greater than 0'

#     @pytest.mark.parametrize("name, plan_type", [
#         ("free", PlanType.FREE_PACKAGE), 
#         ("free_unregistered", PlanType.FREE_UNREGISTERED_PACKAGE), 
#         ("premier_trial", PlanType.PREMIER_TRIAL_PACKAGE)
#     ])   
#     def test_package_plans_create_duplicate_failed(self, name, plan_type):
#         user = self.users[0]  # Admin user
#         token = self.mock_token(user)
#         self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
#         data = {
#             "name": name,
#             "plan_type": plan_type,
#             "usage_limit": 10,
#             "price": 0,
#             "days": 1
#         }
        
#         response = self.api_client.post(self.create_url, data, format='json')
        
#         assert response.status_code == status.HTTP_400_BAD_REQUEST
#         assert response.data['status'] == 'FAILED'
#         assert 'errors' in response.data
#         assert 'name' in response.data['errors']
#         assert response.data['errors']['name'] == 'Package plan with this name and package type already exists'       
