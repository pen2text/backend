from rest_framework import generics, status
from rest_framework.response import Response
from exception.badRequest import BadRequest
from .models import ConversionHistory
from .serializers import ConversionHistorySerializer, ConversionHistoryUpdateSerializer

class ConversionHistoryListView(generics.ListAPIView):
    queryset = ConversionHistory.objects.all()
    serializer_class = ConversionHistorySerializer
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = {
            'status': 'OK',
            'message': 'Conversion History List',
            'data': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
        
class ConversionHistoryCreateView(generics.CreateAPIView):
    queryset = ConversionHistory.objects.all()
    serializer_class = ConversionHistorySerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            response_data = {
                'status': 'FAILED',
                'message': 'Validation Error',
                'data': serializer.errors
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        response_data = {
            'status': 'OK',
            'message': 'Conversion History Created',
            'data': serializer.data
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

class ConversionHistoryRetrieveByIdView(generics.RetrieveAPIView):
    queryset = ConversionHistory.objects.all()
    serializer_class = ConversionHistorySerializer
    lookup_field = 'id'
    
    def get(self, request, *args, **kwargs):
        conversion_id = kwargs.get('id')
        try:
            conversion = self.queryset.get(id=conversion_id)
        except ConversionHistory.DoesNotExist:
            response_data = {
                'status': 'FAILED',
                'message': 'Conversion History Not Found',
                'error': {'Conversion History Not Found'}
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(conversion)
        response_data = {
            'status': 'OK',
            'message': 'Conversion History Detail',
            'data': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)

class ConversionHistoryDeleteView(generics.DestroyAPIView):
    queryset = ConversionHistory.objects.all()
    serializer_class = ConversionHistorySerializer
    lookup_field = 'id'
    
    def delete(self, request, *args, **kwargs):
        conversion_id = kwargs.get('id')
        try:
            conversion = self.queryset.get(id=conversion_id)
        except ConversionHistory.DoesNotExist:
            response_data = {
                'status': 'FAILED',
                'message': 'Conversion History Not Found',
                'error': {'Conversion History Not Found'}
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        
        conversion.delete()
        response_data = {
            'status': 'OK',
            'message': 'Conversion History Deleted'
        }
        return Response(response_data, status=status.HTTP_200_OK)

class ConversionHistoryUpdateView(generics.UpdateAPIView):
    queryset = ConversionHistory.objects.all()
    serializer_class = ConversionHistoryUpdateSerializer
    
    def put(self, request, *args, **kwargs):
        
        conversion_id = request.data.get('id')
        if not conversion_id:
            response_data = {
                'status': 'FAILED',
                'message': 'Conversion ID is required',
                'error': {'Conversion ID is required'}
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            isinstance = self.queryset.get(id=conversion_id)
        except ConversionHistory.DoesNotExist:
            response_data = {
                'status': 'FAILED',
                'message': 'Conversion History Not Found',
                'error': {'Conversion History Not Found'}
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(isinstance, data=request.data, partial=True)
        if not serializer.is_valid():
            response_data = {
                'status': 'FAILED',
                'message': 'Validation Error',
                'data': serializer.errors
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_update(serializer)
        response_data = {
            'status': 'OK',
            'message': 'Conversion History Updated',
            'data': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)

