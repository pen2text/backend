from rest_framework import status, generics
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from utils.chapa_utils import Chapa
from .models import ChapaTransactions
from .serializers import ChapaTransactionSerializer
from utils.format_errors import validation_error
from package_manager.models import PackagePlanDetails, TempSubscriptionPlans
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class ChapaTransactionInitiateView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    serializer_class = ChapaTransactionSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            response_data = {
                'status': 'FAILED',
                'message': 'Validation Error',
                'data': validation_error(serializer.errors)
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        package = serializer.validated_data.pop('package')
        instance = serializer.save()
        response = Chapa.initialize_transaction(instance)
                
        if response.get('status') == 'failed':
            instance.delete()
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        package_instance = PackagePlanDetails.objects.get(id=package['id'])
         
        TempSubscriptionPlans.objects.create(
            user= request.user,
            transaction= instance,
            package_detail= package_instance,
            usage_limit=  package_instance.usage_limit if package_instance.usage_limit > 0 else package['usage_limit']
        )
        return Response(response, status=status.HTTP_200_OK)
        
@csrf_exempt       
class ChaPaTransactionVerifyView(generics.RetrieveAPIView):
    serializer_class = ChapaTransactionSerializer
    queryset = ChapaTransactions
    
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        response = Chapa.verify_payment(instance)
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