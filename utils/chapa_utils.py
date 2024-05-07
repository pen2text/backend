import requests 
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from chapa_gateway import models
from package_manager.models import LimitedUsageSubscriptionPlans, PlanType, TempSubscriptionPlans, UnlimitedUsageSubscriptionPlans

try:
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
    def initialize_transaction(cls, transaction: models.ChapaTransaction) -> dict:
        
        data = {
            'amount': transaction.amount,
            'currency': transaction.currency,
            'email': transaction.email,
            'first_name': transaction.first_name,
            'last_name': transaction.last_name,
            'tx_ref': transaction.id.__str__(),
            'callback_url': CALLBACK_URL,
            # 'return_url': 'https://www.google.com/',
            'phone_number': transaction.phone_number,
            'customization': {
                'title': transaction.payment_title,
                'description': transaction.description
            },
        }
        
        transaction_url = "https://api.chapa.co/v1/transaction/initialize"
        response = requests.post(transaction_url, json=data, headers=cls.get_headers())

        data = response.json()
        if data and data.get('status') == 'success':
            transaction.status = models.ChapaStatus.PENDING
            transaction.checkout_url = data.get('data').get('checkout_url')
            transaction.save()

        return data
    
    @classmethod
    def verify_payment(cls, transaction: models.ChapaTransaction) -> dict:
        verify_url = "https://api.chapa.co/v1/transaction/verify/" + transaction.id.__str__()
        # payload = ''
        response = requests.get(verify_url, headers=cls.get_headers(),)
        data = response.json()
        if data and data.get('status') == 'success' and data.get('data').get('status') == 'success':
            transaction.status = data.get('status')
            transaction.save()
            
            temp_subscription = TempSubscriptionPlans.objects.get(transaction_id=transaction.id)
            create_premier_plan(temp_subscription, transaction)
            
        return data
        
        
def create_premier_plan(temp_subscription: TempSubscriptionPlans, chapa_transaction: models.ChapaTransaction):
    
    expire_date = timezone.now() + timedelta(days=temp_subscription.package_detail.days)
    user = temp_subscription.user

    if temp_subscription.package_detail.plan_type == PlanType.LIMITED_USAGE:
        LimitedUsageSubscriptionPlans.objects.create(
            user= user,
            transaction= chapa_transaction,
            package_detail= temp_subscription.package_detail,
            usage_limit= temp_subscription.usage_limit,
            expire_date= expire_date
        )
    elif temp_subscription.package_detail.plan_type == PlanType.UNLIMITED_USAGE:
        UnlimitedUsageSubscriptionPlans.objects.create(
            user= user,
            transaction= chapa_transaction,
            package_plan= temp_subscription.package_detail,
            expire_date= expire_date
        )
    elif temp_subscription.package_detail.plan_type == PlanType.NON_EXPIRING:
        UnlimitedUsageSubscriptionPlans.objects.create(
            user= user,
            transaction= chapa_transaction,
            package_plan= temp_subscription.package_detail
        )  