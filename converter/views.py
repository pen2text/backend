from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from user_management.models import UserActivities
from .serializers import ConverterSerializer
from utils.format_errors import validation_error
from utils.check_access_utils import check_access

class ConverterView(generics.GenericAPIView):
    serializer_class = ConverterSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if(not serializer.is_valid()):
            response_data = {
                'status': 'FAILED',
                'message': 'Invalid data',
                'errors': validation_error(serializer.errors)
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        response_data = {
            'status': 'OK',
            'message': 'Image processed',
            'data': []
        }
        
           
        result = check_access(request.user, request.META.get('REMOTE_ADDR'))
        print(result)
        
        # for index, image in serializer.validated_data:
        #     #process image call ml model
            
        #     response_data['data'].append({
        #         'index': index,
        #         'text-content': 'This is a sample text content',
        #         'state': 'OK',
        #     })
        
        #Log user image conversion activity
        # data = {
        #     "user_id": user.id,
        #     "ip_address": request.META.get('REMOTE_ADDR'),
        #     "type": "user_conversion"
        # }
        # UserActivities.objects.create(**data)
          
        return Response(response_data, status=status.HTTP_200_OK)

class ConvertUsingRemoteAPIView(generics.GenericAPIView):
    serializer_class = ConverterSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            response_data = {
                'status': 'FAILED',
                'message': 'Invalid data',
                'errors': validation_error(serializer.errors)
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        response_data = {
            'status': 'OK',
            'message': 'Image processed',
            'data': []
        }
        
        result = check_access(request.user, request.META.get('REMOTE_ADDR'))

        # for index, image in serializer.validated_data:
        #     #process image call ml model
            
        #     response_data['data'].append({
        #         'index': index,
        #         'text-content': 'This is a sample text content',
        #         'state': 'OK',
        #     })
        
        #Log server image conversion activity
        # data = {
        #     "user_id": user.id,
        #     "ip_address": request.META.get('REMOTE_ADDR'),
        #     "type": "server_conversion"
        # }
        # UserActivities.objects.create(**data)
        
        return Response(response_data, status=status.HTTP_200_OK)