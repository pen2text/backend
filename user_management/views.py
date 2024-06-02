from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RoleSerializer, UserSerializer, UserUpdateSerializer
from user_management.models import Users, UserActivities
from utils.email_utils import send_verification_email
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from utils.format_errors import validation_error
from django.db.models import Q


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            response_data = {
                "status": "FAILED",
                "message": "Forbidden: You are already logged in",
            }
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            response_data = {
                'status': 'FAILED',
                'message': 'Validation failed',
                'errors': validation_error(serializer.errors)
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        user = serializer.save()
        
        response_data = {
            "status": "OK",
            "message": "User registered successfully",
            "data": {
                "id": user.id,
                **serializer.data,
            }
        }
        
        #Log user registration activity
        data = {
            "user_id": user.id,
            "ip_address": request.META.get('REMOTE_ADDR'),
            "type": "user_registration"
        }
        UserActivities.objects.create(**data)
        
        #send verification email
        send_verification_email(user)
        
        return Response(response_data, status=status.HTTP_201_CREATED)

class UserListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Users.objects.all()
    serializer_class = UserSerializer
    def list(self, request, *args, **kwargs):
        user = request.user
        if user.role == 'user':
            response_data = {
                "status": "FAILED",
                "message": "Forbidden: You do not have permission to access this resource",
            }
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(self.get_queryset(), many=True)
        response_data = {
            "status": "OK",
            "message": "Users retrieved successfully",
            "data": serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)

class UserRetrieveByIdView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = Users.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        user_id = request.user.id
        
        try:
            user = self.queryset.get(id=user_id)  
        except Users.DoesNotExist:
            return Response({
                "status": "FAILED",
                "message": "User not found with the provided ID",
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(user)  
        return Response({
            "status": "OK",
            "message": "User data retrieved successfully",
            "data": serializer.data,
        }, status=status.HTTP_200_OK)
        
class UserRetrieveByEmailView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'email'

    def retrieve(self, request, *args, **kwargs):
        user_email = self.kwargs.get('email')
        user = request.user
        if user.role == 'user' and user.email != user_email:
            response_data = {
                "status": "FAILED",
                "message": "Forbidden: You do not have permission to access this resource",
            }
            return Response(response_data, status=status.HTTP_403_FORBIDDEN) 
        try:
            user = self.queryset.get(email=user_email)  
        except Users.DoesNotExist:
            response_data = {
                "status": "FAILED",
                "message": "User not found with the provided email",
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(user)
        response_data = {
            "status": "OK",
            "message": "User retrieved successfully",
            "data": serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)

class UserDeleteView(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        user_id = self.kwargs.get('id')
        user = request.user
        if user.role == 'user' and user.id != user_id:
            response_data = {
                "status": "FAILED",
                "message": "Forbidden: You do not have permission to access this resource",
            }
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)
        try:
            user = self.queryset.get(id=user_id)  
        except Users.DoesNotExist:
            response_data = {
                "status": "FAILED",
                "message": "User not found with the provided ID",
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        self.perform_destroy(user)
        response_data = {
            "status": "OK",
            "message": "User deleted successfully",
        }
        return Response(response_data, status=status.HTTP_200_OK)

class CheckEmailExistsView(generics.GenericAPIView):
    serializer_class = UserSerializer
    lookup_field = 'email'
    
    def get(self, request, *args, **kwargs):
        user_email = self.kwargs.get('email')    
        if not user_email or user_email.isspace():
            response_data = {
                "status": "FAILED",
                "message": "Email is required",
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user_email = Users.objects.get(email=user_email)
        except Users.DoesNotExist:
            response_data = {
                "status": "OK",
                "message": "Email does not exists",
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        response_data = {
            "status": "OK",
            "message": "Email exists",
        }
        return Response(response_data, status=status.HTTP_200_OK)
   
class UserUpdateView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = Users.objects.all()
    serializer_class = UserUpdateSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        user_id = request.user.id
         
        try:
            user = self.queryset.get(id=user_id)
        except Users.DoesNotExist:
            response_data = {
                'status': 'FAILED', 
                'message': "User not found with the provided ID",
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(user, data=request.data, partial=partial)
        if not serializer.is_valid():
            response_data = {
                'status': 'FAILED',
                'message': 'Validation failed',
                'errors': validation_error(serializer.errors)
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        self.perform_update(serializer)
        response_data = {
            "status": "OK",
            "message": "User information updated successfully",
            "data": serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
class UpdateRoleView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    serializer_class = RoleSerializer

    def patch(self, request, format=None):
        if request.user.role != 'admin':
            response_data = {
                "status": "FAILED",
                "message": "Forbidden: You do not have permission to update user roles",
            }
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)
        
        try:
            user_id = request.data.get('id')
            user = Users.objects.get(id=user_id)
        except Users.DoesNotExist:
            response_data = {
                "status": "FAILED", 
                "message": "User does not exist", 
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(user, data=request.data, partial=True, context={'request': request})
        
        if not serializer.is_valid():
            response_data = {
                "status": "FAILED",
                "message": "Validation failed",
                "errors": validation_error(serializer.errors)
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        
        user_data = UserSerializer(user).data 

        response_data = {
            "status": "OK", 
            "message": "Role updated successfully", 
            "data": user_data,
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
class UserSearchByNameView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = Users.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        user = request.user
        if user.role == 'user':
            response_data = {
                "status": "FAILED",
                "message": "Forbidden: You do not have permission to access this resource",
            }
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)
        
        search_term = self.kwargs.get('name').strip() or ''

        # search for users by first or last name containing the search term
        users = self.queryset.filter(Q(first_name__icontains=search_term) | Q(last_name__icontains=search_term))
        
        serializer = self.get_serializer(users, many=True)
        response_data = {
            "status": "OK",
            "message": "Users retrieved successfully",
            "data": serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)