from rest_framework import status, generics
from rest_framework.response import Response
from .models import RemoteAPITokenManagers
from .serializers import RemoteAPITokenManagerSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from utils.format_errors import validation_error
from utils.jwt_token_utils import generate_jwt_token


class RemoteAPITokenManagerCreateView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    serializer_class = RemoteAPITokenManagerSerializer
    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            response_data = {
                'status': 'FAILED',
                'message': 'Validation Error',
                'data': validation_error(serializer.errors)
            }
        
        payload = {
            'token_type': 'remote-access-key',
            'id': str(user.id),
            'email': user.email,
        }
        serializer.validated_data['token'] = generate_jwt_token(payload, 10)
        serializer.validated_data['user'] = user
        serializer.save()
        response_data = {
            'status': 'OK',
            'message': 'Remote API Token Created',
            'data': serializer.data
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

class RemoteAPITokenManagerListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = RemoteAPITokenManagers.objects.all()
    serializer_class = RemoteAPITokenManagerSerializer
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        # serializer.data.pop('token')
        response_data = {
            'status': 'OK',
            'message': 'Remote API Token List',
            'data': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
class RemoteAPITokenManagerDeleteView(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = RemoteAPITokenManagers.objects.all()
    serializer_class = RemoteAPITokenManagerSerializer
    lookup_field = 'id'
    def delete(self, request, *args, **kwargs):
        user = request.user
        token_id = kwargs.get('id')
        try:
            token = self.queryset.get(id=token_id, user=user)
        except RemoteAPITokenManagers.DoesNotExist:
            response_data = {
                'status': 'FAILED',
                'message': 'Remote API Token Not Found',
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        token.delete()
        response_data = {
            'status': 'OK',
            'message': 'Remote API Token Deleted',
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
