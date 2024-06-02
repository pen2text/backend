# import uuid
# import pytest
# from rest_framework import status
# from django.urls import reverse
# from unittest.mock import patch


# @pytest.fixture
# def initiate_url():
#     return reverse('chapa-initiate')

# @pytest.mark.django_db
# class TestChapaTransactionInitiateView:
    
#     @pytest.fixture(autouse=True)
#     def setup(self, api_client, users, mock_token, package_plans, initiate_url):
#         self.api_client = api_client
#         self.initiate_url = initiate_url
#         self.users = users
#         self.mock_token = mock_token
#         self.package_plans = package_plans

#     def test_chapa_transaction_initiate_unauthorized(self, initiate_url):
#         response = self.api_client.post(initiate_url, {})
        
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED
#         assert 'detail' in response.data
#         assert response.data['detail'] == 'Authentication credentials were not provided.'

#     def test_chapa_transaction_initiate_validation_error(self, initiate_url):
#         user = self.users[0]
#         token = self.mock_token(user)
#         self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
#         data = {}  # Invalid data
#         response = self.api_client.post(initiate_url, data)
        
#         assert response.status_code == status.HTTP_400_BAD_REQUEST
#         assert response.data['status'] == 'FAILED'
#         assert response.data['message'] == 'Validation Error'
#         assert 'data' in response.data

#     def test_chapa_transaction_initiate_active_package(self, initiate_url):
#         user = self.users[0]
#         token = self.mock_token(user)
#         self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
#         data = {'id': self.package_plans[3].id, 'usage_limit': 10}
#         with patch('chapa_gateway.views.is_user_has_active_package', return_value=True):
#             response = self.api_client.post(initiate_url, data)
        
#         assert response.status_code == status.HTTP_400_BAD_REQUEST
#         assert response.data['status'] == 'FAILED'
#         assert response.data['message'] == "You hadn't finished using the previous package, kindly finish using it before purchasing another package"

#     def test_chapa_transaction_initiate_success(self, initiate_url):
#         user = self.users[0]
#         token = self.mock_token(user)
#         self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        
#         data = {'id': self.package_plans[3].id, 'usage_limit': 5}
#         with patch('chapa_gateway.views.is_user_has_active_package', return_value=False), \
#              patch('chapa_gateway.views.Chapa.initialize_transaction', 
#                    return_value={
#                        'status': 'OK', 
#                        'message': 'Transaction initialized successfully',
#                        'data': {'checkout_url': 'http://checkout.url'}
#                     }
#                 ):
            
#             response = self.api_client.post(initiate_url, data)
        
#         assert response.status_code == status.HTTP_200_OK
#         assert response.data['status'] == 'OK'
#         assert response.data['message'] == 'Transaction initialized successfully'
#         assert 'data' in response.data
#         assert 'checkout_url' in response.data['data']
#         assert response.data['data']['checkout_url'] == 'http://checkout.url'

#     def test_chapa_transaction_initiate_failure(self, initiate_url):
#         user = self.users[0]
#         token = self.mock_token(user)
#         self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
#         package = self.package_plans[3]
        
#         data = {'id': package.id, 'usage_limit': 5}
#         with patch('chapa_gateway.views.is_user_has_active_package', return_value=False), \
#              patch('chapa_gateway.views.Chapa.initialize_transaction', 
#                    return_value={
#                        'status': 'FAILED', 
#                         'message': 'Failed to initialize transaction'
#                     }
#                 ):
            
#             response = self.api_client.post(initiate_url, data)
        
#         assert response.status_code == status.HTTP_400_BAD_REQUEST
#         assert response.data['status'] == 'FAILED'
#         assert response.data['message'] == 'Failed to initialize transaction'

#     def test_chapa_transaction_initiate_invalid_package_id(self):
#         user = self.users[0]
#         token = self.mock_token(user)
#         self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
#         package_id = '00000000-0000-0000-0000-000000000000'
#         data = {'id': package_id, 'usage_limit':3}
        
#         response = self.api_client.post(self.initiate_url, data)
        
#         assert response.status_code == status.HTTP_400_BAD_REQUEST
#         assert response.data['status'] == 'FAILED'
#         assert response.data['message'] == 'Validation Error'

# # different package plans for testing
