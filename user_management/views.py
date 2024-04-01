from rest_framework import generics, status
from rest_framework.exceptions import NotFound, APIException
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, UserUpdateSerializer
from user_management.models import User
from utils.email_utils import send_email
from utils.jwt_token_utils import generate_jwt_token, verify_token
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class BadRequest(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Bad Request'
    default_code = 'bad_request'

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            response_data = {
                "status": "success",
                "code": status.HTTP_201_CREATED,
                "message": "User created",
                "data": {
                    **serializer.data, 
                    "id": user.id,
                    },
                "errors": []
            }
            
            payload = {
                'email': user.email,
                'id': user.id,
                'token_type': 'email_verification'
            }
            jwt_token = generate_jwt_token(payload)

            # Retrieve content, subject, and receiver_email
            verification_url = f'http://localhost:8000/api/users/verify-email/{jwt_token}'
            content = "Content for email verification. " + verification_url 
            subject = "Email Verification"
            receiver_email = user.email
            
            # Send the email
            if send_email(content, subject, receiver_email):
                print("Email sent successfully!")
            else:
                print("Failed to send email.")
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            response_data = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Validation failed",
                "data": {},
                "errors": serializer.errors
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

class UserListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = UserSerializer
    def list(self, request, *args, **kwargs):
        user = request.user
        if user.role == 'user':
            response_data = {
                "status": "error",
                "code": status.HTTP_403_FORBIDDEN,
                "message": "Forbidden",
                "data": {},
                "errors": ["You do not have permission to access this resource"]
            }
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)
        
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = {
            "status": "success",
            "code": status.HTTP_200_OK,
            "message": "Users retrieved successfully",
            "data": serializer.data,
            "errors": []
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
                "status": "error",
                "code": status.HTTP_403_FORBIDDEN,
                "message": "Forbidden",
                "errors": ["You do not have permission to access this resource"]
            }
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)
        
         
        try:
            user = self.queryset.get(id=user_id)  
        except User.DoesNotExist:
            return Response({
                "status": "error",
                "code": status.HTTP_404_NOT_FOUND,
                "message": "User not found",
                "data": {},
                "errors": ["User not found with the provided ID"]
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(user)  
        return Response({
            "status": "success",
            "code": status.HTTP_200_OK,
            "message": "User retrieved successfully",
            "data": serializer.data,
            "errors": []
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
                "status": "error",
                "code": status.HTTP_403_FORBIDDEN,
                "message": "Forbidden",
                "data": {},
                "errors": ["You do not have permission to access this resource"]
            }
            return Response(response_data, status=status.HTTP_403_FORBIDDEN) 
        try:
            user = self.queryset.get(email=user_email)  
        except User.DoesNotExist:
            response_data = {
                "status": "error",
                "code": status.HTTP_404_NOT_FOUND,
                "message": "User not found",
                "data": {},
                "errors": ["User not found with the provided email"]
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(user)
        response_data = {
            "status": "success",
            "code": status.HTTP_200_OK,
            "message": "User retrieved successfully",
            "data": serializer.data,
            "errors": []
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
                "status": "error",
                "code": status.HTTP_403_FORBIDDEN,
                "message": "Forbidden",
                "data": {},
                "errors": ["You do not have permission to access this resource"]
            }
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)
        try:
            user = self.queryset.get(id=user_id)  
        except User.DoesNotExist:
            response_data = {
                "status": "error",
                "code": status.HTTP_404_NOT_FOUND,
                "message": "User not found",
                "data": {},
                "errors": ["User not found with the provided ID"]
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        self.perform_destroy(user)
        response_data = {
            "status": "success",
            "code": status.HTTP_200_OK,
            "message": "User deleted successfully",
            "data": {},
            "errors": []
        }
        return Response(response_data, status=status.HTTP_200_OK)

class CheckEmailExistsView(generics.GenericAPIView):
    serializer_class = UserSerializer
    lookup_field = 'email'
    def get(self, request, *args, **kwargs):
        user_email = self.kwargs.get('email')    
        if not user_email:
            return Response({'status': 'error', 'message': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
    
        user_exists = User.objects.filter(email=user_email).exists()
        response_data = {
            "status": "success",
            "code": status.HTTP_200_OK,
            "message": "Email existence checked successfully",
            "data": {"email_exists": user_exists},
            "errors": []
        }
        if not user_exists:
            response_data['message'] = "Email does not exist"
            response_data['status'] = "error"
            response_data['code'] = status.HTTP_404_NOT_FOUND
        
        return Response(response_data, status=response_data['code'])

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
                'status': 'error', 
                "status": status.HTTP_404_NOT_FOUND,
                'message': str(e),
                'errors': [str(e)],
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except BadRequest as e:
            response_data = {
                'status': 'error', 
                "status": status.HTTP_400_BAD_REQUEST,
                'message': str(e),
                'errors': [str(e)],
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        if user.role != 'user' or user.id != serializer.validated_data['id']:
            response_data = {
                "status": "error",
                "code": status.HTTP_403_FORBIDDEN,
                "message": "Forbidden",
                "data": {},
                "errors": ["You do not have permission to update this user's information"]
            }
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)
        
        self.perform_update(serializer)
        
        response_data = {
            "status": "success",
            "code": status.HTTP_200_OK,
            "message": "User updated successfully",
            "data": serializer.data,
            "errors": []
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def get_object(self):
        user_id = self.request.data.get('id')
        
        if user_id is None:
            raise BadRequest("ID not provided in the request data.")
        
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound("User not found.")

class VerifyEmailView(generics.GenericAPIView):
    serializer_class = UserSerializer
    def get(self, request, token):
        
        try:
            user = verify_token(token, 'email_verification')
            user.is_verified = True
            user.save()
            response_data = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Email verified successfully.",
                "data": {},
                "errors": []
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except ValueError as e:
            response_data = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": str(e),
                "data": {},
                "errors": [str(e)]
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

class UpdateRoleView(APIView):
    def patch(self, request, format=None):
        role = request.data.get('role', None)
        user_id = request.data.get('id', None)
        print(role, user_id)
        if not role or not user_id:
            response_data = {
                "status": "error", 
                "code": status.HTTP_400_BAD_REQUEST, 
                "message": "Both role and user_id must be provided", 
                "errors": ["Both role and user_id must be provided"]
            }
            return Response(response_data, status = status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            response_data = {
                "status": "error", 
                "code": status.HTTP_404_NOT_FOUND, 
                "message": "User does not exist", 
                "errors": ["User does not exist"]
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        
        user.role = role 
        user.save()
        serializer = UserSerializer(user)
        response_data = {
            "status": "success", 
            "code": status.HTTP_200_OK, 
            "message": "Role updated successfully", 
            "data": serializer.data, 
        }
        return Response(response_data, status=status.HTTP_200_OK)