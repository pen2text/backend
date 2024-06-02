import pytest
from rest_framework import status
from django.urls import reverse
from unittest.mock import patch
from chapa_gateway.models import ChapaTransactions
from package_manager.models import TempSubscriptionPlans


@pytest.fixture
def verify_url():
    def _verify_url(pk):
        return reverse('chapa-verify', args=[pk])
    return _verify_url

@pytest.fixture
def transactions(users):
    transaction1 = ChapaTransactions.objects.create(
        amount=20,
        currency='ETB',
        email=users[0].email,
        first_name=users[0].first_name,
        last_name=users[0].last_name,
        payment_title='Payment',
        description='Payment Description',
        status= 'success'
    )

    transaction2 = ChapaTransactions.objects.create(
        amount=20,
        currency='ETB',
        email=users[1].email,
        first_name=users[1].first_name,
        last_name=users[1].last_name,
        payment_title='Payment',
        description='Payment Description',
        status= 'pending'
    )
    
    return [transaction1, transaction2]

@pytest.fixture
def temp_subscription(transactions, users, package_plans):
    temp1 = TempSubscriptionPlans.objects.create(
        user=users[1],
        transaction=transactions[1],
        package_detail=package_plans[3],
        usage_limit=10
    )
    return temp1

@pytest.mark.django_db
class TestChapaTransactionVerifyView:
    
    @pytest.fixture(autouse=True)
    def setup(self, api_client, verify_url, transactions, temp_subscription):
        self.api_client = api_client
        self.verify_url = verify_url
        self.transactions = transactions
        self.temp_subscription = temp_subscription

    def test_chapa_transaction_verify_not_found(self):
        non_existent_uuid = '00000000-0000-0000-0000-000000000000'
        url = self.verify_url(non_existent_uuid)
        response = self.api_client.get(url)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['status'] == 'FAILED'
        assert response.data['message'] == 'Invalid Transaction'

    def test_chapa_transaction_verify_already_verified(self):
        
        transaction_id = self.transactions[0].id
        url = self.verify_url(transaction_id)
        response = self.api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'OK'
        assert response.data['message'] == 'Transaction already verified'

    def test_chapa_transaction_verify_failure(self):
        transaction_id = self.transactions[1].id 
        url = self.verify_url(transaction_id)
        
        with patch('chapa_gateway.views.Chapa.verify_payment', return_value={'status': 'FAILED', 'message': 'Failed to verify payment transaction',}):
            response = self.api_client.get(url)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['status'] == 'FAILED'
        assert response.data['message'] == 'Failed to verify payment transaction'

    def test_chapa_transaction_verify_success(self):
        transaction_id = self.transactions[1].id
        
        url = self.verify_url(transaction_id)
        with patch('chapa_gateway.views.Chapa.verify_payment',
                   return_value={
                       'status': 'OK', 
                       'message': 'Transaction verified successfully',
                       'data': {}
                    }), \
             patch('chapa_gateway.views.create_premier_plan', return_value=True):
            response = self.api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'OK'
        assert response.data['message'] == 'Transaction verified successfully'
        
