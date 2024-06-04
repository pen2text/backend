from rest_framework import generics, status
from rest_framework.response import Response
from utils.check_access_utils import is_user_has_active_package
from .models import ConversionHistories
from .serializers import ConversionHistorySerializer, ConversionHistoryUpdateSerializer
from utils.format_errors import validation_error
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class ConversionHistoryListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = ConversionHistories.objects.all()
    serializer_class = ConversionHistorySerializer
    
    def get(self, request, *args, **kwargs):
        
        user = request.user        
        queryset = self.get_queryset().filter(user=user).order_by('-created_at')
        serializer = self.get_serializer(queryset, many=True)
        response_data = {
            'status': 'OK',
            'message': 'Conversion History List',
            'data': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
        
class ConversionHistoryRetrieveByIdView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = ConversionHistories.objects.all()
    serializer_class = ConversionHistorySerializer
    lookup_field = 'id'
    
    def get(self, request, *args, **kwargs):
        user = request.user
        conversion_id = kwargs.get('id')
        
        try:
            conversion = self.queryset.get(id=conversion_id, user=user)
        except ConversionHistories.DoesNotExist:
            response_data = {
                'status': 'FAILED',
                'message': 'Conversion History Not Found',
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
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = ConversionHistories.objects.all()
    serializer_class = ConversionHistorySerializer
    lookup_field = 'id'
    
    def delete(self, request, *args, **kwargs):
        user = request.user
        conversion_id = kwargs.get('id')
        
        try:
            conversion = self.queryset.get(id=conversion_id, user=user)
        except ConversionHistories.DoesNotExist:
            response_data = {
                'status': 'FAILED',
                'message': 'Conversion History Not Found',
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        
        conversion.delete()
        response_data = {
            'status': 'OK',
            'message': 'Conversion History Deleted'
        }
        return Response(response_data, status=status.HTTP_200_OK)

class ConversionHistoryUpdateView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = ConversionHistories.objects.all()
    serializer_class = ConversionHistoryUpdateSerializer
    
    def put(self, request, *args, **kwargs):
        user = request.user
        
        # check whether the user has premier access
        is_premier = is_user_has_active_package(user)
        if not is_premier:
            response_data = {
                'status': 'FAILED',
                'message': 'Free User Cannot Update Conversion History'
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
          
        try:
            conversion_id = request.data.get('id')
            isinstance = self.queryset.get(id=conversion_id, user=user)
        except ConversionHistories.DoesNotExist:
            response_data = {
                'status': 'FAILED',
                'message': 'Conversion History Not Found',
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(isinstance, data=request.data, partial=True)
        if not serializer.is_valid():
            response_data = {
                'status': 'FAILED',
                'message': 'Validation Error',
                'errors': validation_error(serializer.errors)
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_update(serializer)
        response_data = {
            'status': 'OK',
            'message': 'Conversion History Updated',
            'data': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)



# class ConversionHistoryCreateView(generics.CreateAPIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]
    
#     queryset = ConversionHistories.objects.all()
#     serializer_class = ConversionHistorySerializer
    
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if not serializer.is_valid():
#             response_data = {
#                 'status': 'FAILED',
#                 'message': 'Validation Error',
#                 'errors': validation_error(serializer.errors)
#             }
#             return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
#         serializer.validated_data['user'] = request.user
        
#         serializer.save()
#         response_data = {
#             'status': 'OK',
#             'message': 'Conversion History Created',
#             'data': serializer.data
#         }
#         return Response(response_data, status=status.HTTP_201_CREATED)
