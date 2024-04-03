from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from user_management.models import User
from utils.email_utils import send_email
from utils.jwt_token_utils import generate_jwt_token, verify_token
from authentication.serializers import ResetPasswordSerializer, CustomTokenObtainPairSerializer



class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors['data'], status=serializer.errors['data']['code'])
        
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class ForgotPasswordView(APIView):
    queryset = User.objects.all()
    lookup_field = 'email'
    def get(self, request, *args, **kwargs):
        user_email = self.kwargs.get('email')
        if not user_email:
            response_data = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Email is required",
                "data": {},
                "errors": ["Email is required"]
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = self.queryset.get(email = user_email)
        except User.DoesNotExist:
            response_data = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "User with this email does not exist",
                "data": {},
                "errors": ["User with this email does not exist"]
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        payload = {
            'email': user.email,
            'id': str(user.id),
            'token_type': 'forgot_password'
        }
        token = generate_jwt_token(payload)
        
        # Construct the password reset link
        password_reset_link = f'http://front.com/reset-password/?token={token}'

        # Send the password reset email using your utility function
        content = "Content for password reset. " + password_reset_link 
        subject = "Password reset instructions"
        receiver_email = user_email
        
        response_data = {
            "status": "success",
            "code": status.HTTP_200_OK,
            "message": "Password reset email sent",
            "data": {},
            "errors": []
        }
        
        if not send_email(content, subject, receiver_email):
            response_data["status"] = "error"
            response_data["code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            response_data["message"] = "An error occurred while sending the email"
            response_data["errors"] = ["An error occurred while sending the email"]
        
        return Response(response_data, status=response_data["code"])

class ResetPasswordView(APIView):
    serializer_class = ResetPasswordSerializer
    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        
        if not serializer.is_valid():
            response_data = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Validation error",
                "errors": serializer.errors
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        token = serializer.validated_data.get('token')
        password = serializer.validated_data.get('password')

        try:
            user = verify_token(token, 'forgot_password')
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            response_data = {
                    "status": "error",
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Invalid token",
                    "errors": ["Invalid token"]
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(password)
        user.save()
        response_data = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Password updated successfully",
        }
        return Response(response_data, status=status.HTTP_200_OK)