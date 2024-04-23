from rest_framework import generics, status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, UserUpdateSerializer
from user_management.models import User
from utils.email_utils import send_verification_email
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from exception.badRequest import BadRequest
from utils.format_errors import validation_error

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
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
            "message": "User created successfully",
            "data": {
                "id": user.id,
                **serializer.data,
            }
        }
        
        #send verification email
        send_verification_email(user)
        
        return Response(response_data, status=status.HTTP_201_CREATED)

class UserListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = UserSerializer
    def list(self, request, *args, **kwargs):
        user = request.user
        if user.role == 'user':
            response_data = {
                "status": "FAILED",
                "message": "Forbidden: You do not have permission to access this resource",
            }
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)
        
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = {
            "status": "OK",
            "message": "Users retrieved successfully",
            "data": serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)

class UserRetrieveByIdView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        user_id = self.kwargs.get('id') 
        if user.role == 'user' and user.id != user_id:
            response_data = {
                "status": "FAILED",
                "message": "Forbidden: You do not have permission to access this resource",
            }
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)
        
        try:
            user = self.queryset.get(id=user_id)  
        except User.DoesNotExist:
            return Response({
                "status": "FAILED",
                "message": "User not found with the provided ID",
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(user)  
        return Response({
            "status": "OK",
            "message": "User retrieved successfully",
            "data": serializer.data,
        }, status=status.HTTP_200_OK)
        
class UserRetrieveByEmailView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = User.objects.all()
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
        except User.DoesNotExist:
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
    
    queryset = User.objects.all()
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
        except User.DoesNotExist:
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
        if not user_email:
            return Response({'status': 'FAILED', 'message': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
    
        user_exists = User.objects.filter(email=user_email).exists()
        response_data = {
            "status": "OK",
            "message": "Email existence checked successfully",               
        }
        
        code = status.HTTP_200_OK
        if not user_exists:
            response_data['status'] = "FAILED"
            response_data['message'] = "Email does not exist"
            code = status.HTTP_404_NOT_FOUND
        
        return Response(response_data, status=code)

class UpdateRoleView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def patch(self, request, format=None):
        role = request.data.get('role', None)
        user_id = request.data.get('id', None)
        
        if not role or not user_id:
            response_data = {
                "status": "FAILED", 
                "message": "Both role and user_id must be provided", 
            }
            return Response(response_data, status = status.HTTP_400_BAD_REQUEST)
        
        user = request.user
        if user.role != 'admin':
            response_data = {
                "status": "FAILED",
                "message": "Forbidden: You do not have permission to update user roles",
            }
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            response_data = {
                "status": "FAILED", 
                "message": "User does not exist", 
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        
        user.role = role 
        user.save()
        serializer = UserSerializer(user)
        response_data = {
            "status": "OK", 
            "message": "Role updated successfully", 
            "data": serializer.validated_data, 
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
class UserUpdateView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)

        try:
            instance = self.get_object()
        except NotFound as e:
            response_data = {
                'status': 'FAILED', 
                'message': str(e),
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except BadRequest as e:
            response_data = {
                'status': 'FAILED', 
                'message': str(e),
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            response_data = {
                'status': 'FAILED',
                'message': 'Validation failed',
                'errors': validation_error(e.detail)
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        if user.role != 'user' or user.id != serializer.validated_data['id']:
            response_data = {
                "status": "FAILED",
                "message": "Forbidden: You do not have permission to update this user's information",
            }
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)

        # If password is not provided or empty, retain the existing password
        if 'password' in request.data and not request.data['password']: 
            serializer.validated_data.pop('password')

        serializer.validated_data['gender'] = serializer.validated_data['gender'].lower()
        self.perform_update(serializer)
        
        response_data = {
            "status": "OK",
            "message": "User updated successfully",
            "data": serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def get_object(self):
        user_id = self.request.data.get('id')
        
        if user_id is None:
            raise BadRequest("ID not provided in the request data.")
        
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound("User doesn't found!")