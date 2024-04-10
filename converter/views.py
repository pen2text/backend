from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from .serializers import ConverterSerializer
from utils.format_errors import validation_error

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
        
        # for index, image in serializer.validated_data:
        #     #process image call ml model
            
        #     response_data['data'].append({
        #         'index': index,
        #         'text-content': 'This is a sample text content',
        #         'state': 'OK',
        #     })
        
            
        return Response(response_data, status=status.HTTP_200_OK)

class ConvertUsingRemoteAPIView(generics.GenericAPIView):
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
        
        # for index, image in serializer.validated_data:
        #     #process image call ml model
            
        #     response_data['data'].append({
        #         'index': index,
        #         'text-content': 'This is a sample text content',
        #         'state': 'OK',
        #     })
        
            
        return Response(response_data, status=status.HTTP_200_OK)