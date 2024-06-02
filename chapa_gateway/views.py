from rest_framework import status, generics
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from utils.chapa_utils import Chapa, create_premier_plan
from utils.check_access_utils import is_user_has_active_package
from .models import ChapaStatus, ChapaTransactions
from .serializers import ChapaPaymentInitializationSerializer
from utils.format_errors import validation_error
from package_manager.models import PackagePlanDetails, PlanType, TempSubscriptionPlans
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class ChapaTransactionInitiateView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    serializer_class = ChapaPaymentInitializationSerializer
    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            response_data = {
                'status': 'FAILED',
                'message': 'Validation Error',
                'data': validation_error(serializer.errors)
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        if is_user_has_active_package(request.user):
            response_data = {
                'status': 'FAILED',
                'message': "You hadn't finished using the previous package, kindly finish using it before purchasing another package"
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            
        package_instance = PackagePlanDetails.objects.get(id= serializer.validated_data['id'])
        
        # calculate package fee
        package_fee = 20
        
        # create transaction       
        new_transaction = ChapaTransactions.objects.create(
            amount= package_fee,
            currency='ETB',
            phone_number= "0912345678",
            email = user.email,
            first_name = user.first_name,
            last_name = user.last_name,
            payment_title = 'Payment',
            description = 'Payment Description'
        )
        
        response = Chapa.initialize_transaction(new_transaction)
        
        if not response:
            response_data = {
                'status': 'FAILED',
                'message': 'Failed to initialize transaction'
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        if response['status'] == 'success':
            new_transaction .status = ChapaStatus.PENDING
            new_transaction .checkout_url = response['data']['checkout_url']
            new_transaction .save()
                
        if response['status'] == 'failed':
            new_transaction .delete()
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
                
        usage_limit = package_instance.usage_limit
        if package_instance.plan_type in [PlanType.CUSTOM_LIMITED_USAGE, PlanType.NON_EXPIRING_LIMITED_USAGE]:
            usage_limit = serializer.validated_data['usage_limit']
            
        TempSubscriptionPlans.objects.create(
            user= user,
            transaction= new_transaction ,
            package_detail= package_instance,
            usage_limit=  usage_limit
        )
        
        response_data = {
            'status': 'OK',
            'message': 'Transaction initialized successfully',
            'data': {
                'checkout_url': response['data']['checkout_url']
            }
        }
        return Response(response_data, status=status.HTTP_200_OK)

# @csrf_exempt       
class ChapaTransactionVerifyView(generics.RetrieveAPIView):
    serializer_class = ChapaPaymentInitializationSerializer
    queryset = ChapaTransactions
    
    def get(self, request, *args, **kwargs):
        tx_ref = kwargs.get('pk')
        try:
            instance = self.queryset.objects.get(id=tx_ref)
            temp_subscription = TempSubscriptionPlans.objects.filter(transaction_id=tx_ref).first()
        except ChapaTransactions.DoesNotExist or TempSubscriptionPlans.DoesNotExist:
            response_data = {
                'status': 'FAILED',
                'message': 'Invalid Transaction'
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        if instance.status == 'success':
            response_data = {
                'status': 'OK',
                'message': 'Transaction already verified'
            }
            return Response(response_data, status=status.HTTP_200_OK)
           
        response = Chapa.verify_payment(tx_ref.__str__())
        if response['status'] == 'FAILED':
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        result = create_premier_plan(temp_subscription, instance)
        if result == False:
            response_data = {
                'status': 'FAILED',
                'message': 'Failed to verify transaction'
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)      
        
        return Response(response, status=status.HTTP_200_OK)

@csrf_exempt
class ChapaWebhookView(generics.CreateAPIView):
    queryset = ChapaTransactions
    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            transaction_instance = self.queryset.objects.get(id=data.get('reference'))
            transaction_instance.status = data.get('status')
            transaction_instance.response_dump = data
            transaction_instance.save()
            return Response(data, status=status.HTTP_200_OK)
        except ChapaTransactions.DoesNotExist:
            return Response(
                {
                    'error': "Invalid Transaction"
                },
                status=status.HTTP_400_BAD_REQUEST
            )