import requests 
from datetime import timedelta
from django.db import transaction
from django.utils import timezone
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from chapa_gateway import models
from package_manager.models import LimitedUsageSubscriptionPlans, PlanType, TempSubscriptionPlans, UnlimitedUsageSubscriptionPlans

try:
    BASE_URL = settings.CHAPA_BASE_URL
    SECRET_KEY = settings.CHAPA_SECRET_KEY
    CALLBACK_URL = settings.CHAPA_CALLBACK_URL
except AttributeError as e:
    raise ImproperlyConfigured(f"One or more chapa config missing {e}, please check in your settings file")


class Chapa:
    @classmethod
    def get_headers(cls) -> dict:
        return {
            'Content-type': 'application/json',
            'Authorization': f'Bearer {SECRET_KEY}'
        }

    @classmethod
    def initialize_transaction(cls, transaction) -> dict:
        # data['return_url']: 'https://www.google.com/',
        payment_data = {
            'amount': transaction.amount,
            'currency': transaction.currency,
            'email': transaction.email,
            'first_name': transaction.first_name,
            'last_name': transaction.last_name,
            'tx_ref': transaction.id.__str__(),
            'callback_url': CALLBACK_URL + transaction.id.__str__(),
            'customization': {
                'title': transaction.payment_title,
                'description': transaction.description
            },
        }
        
        transaction_url = BASE_URL + "initialize"
        response = requests.post(transaction_url, json=payment_data, headers=cls.get_headers())
        return response.json()
    
    @classmethod
    def verify_payment(cls, tx_ref) -> dict:
        verify_url = BASE_URL + "verify/" + tx_ref
        response = requests.get(verify_url, headers=cls.get_headers())
        
        data = response.json()

        if data and data['status'] == 'success' and data['data']['status'] == 'success':
            response_data = {
                'status': 'OK',
                'message': 'Transaction verified successfully'
            }
            return response_data
        
        response_data = {
            'status': 'FAILED',
            'message': 'Failed to verify transaction'
        }
        return response_data
        
        
def create_premier_plan(temp_subscription: TempSubscriptionPlans, chapa_transaction: models.ChapaTransactions):
    try:
        with transaction.atomic():
            
            expire_date = timezone.now() + timedelta(days=temp_subscription.package_detail.days)
            user = temp_subscription.user
            
            if temp_subscription.package_detail.plan_type == PlanType.NON_EXPIRING_LIMITED_USAGE:
                expire_date = None

            if temp_subscription.package_detail.plan_type in (PlanType.LIMITED_USAGE, PlanType.CUSTOM_LIMITED_USAGE, PlanType.NON_EXPIRING_LIMITED_USAGE):
                LimitedUsageSubscriptionPlans.objects.create(
                    user=user,
                    transaction=chapa_transaction,
                    package_detail=temp_subscription.package_detail,
                    usage_limit=temp_subscription.usage_limit,
                    expire_date=expire_date
                )
            else:
                UnlimitedUsageSubscriptionPlans.objects.create(
                    user=user,
                    transaction=chapa_transaction,
                    package_plan=temp_subscription.package_detail,
                    expire_date=expire_date
                )   
            
            # delete temp subscription    
            temp_subscription.delete()
            
            chapa_transaction.status = models.ChapaStatus.SUCCESS
            chapa_transaction.save()
            
        return True
    except Exception as e:
        # logger.error(f"Error creating premier plan: {e}")        
        chapa_transaction.status = models.ChapaStatus.FAILED
        chapa_transaction.save()
        return False

