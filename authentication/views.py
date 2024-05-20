from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from user_management.models import Users
from utils.email_utils import send_reset_password_email
from utils.jwt_token_utils import verify_token
from utils.format_errors import validation_error
from authentication.serializers import ResetPasswordSerializer, CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        
        if not serializer.is_valid():
            response_data = {
                "status": "FAILED",
                "message": "Validation error",
                "errors": validation_error(serializer.errors)
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class ForgotPasswordView(APIView):
    queryset = Users.objects.all()
    lookup_field = 'email'
    
    def get(self, request, *args, **kwargs):
        user_email = self.kwargs.get('email')
        if not user_email:
            response_data = {
                "status": "FAILED",
                "message": "Email is required",
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = self.queryset.get(email = user_email)
        except Users.DoesNotExist:
            response_data = {
                "status": "FAILED",
                "message": "User with this email does not exist",
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        if not send_reset_password_email(user):
            response_data["status"] = "FAILED"
            response_data["message"] = "An error occurred while sending the email. Please try again later."
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        response_data = {
            "status": "OK",
            "message": "Password reset email has been sent",
        }
        return Response(response_data, status=status.HTTP_200_OK)

class ResetPasswordView(APIView):
    serializer_class = ResetPasswordSerializer
    
    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        
        if not serializer.is_valid():
            response_data = {
                "status": "OK",
                "message": "Validation error",
                "errors": validation_error(serializer.errors)
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        token = serializer.validated_data.get('token')
        password = serializer.validated_data.get('password')

        try:
            user = verify_token(token, 'password_reset')
        except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
            response_data = {
                "status": "FAILED",
                "message": "Invalid token or expired token. Please request a new one.",
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(password)
        user.save()
        response_data = {
                "status": "OK",
                "message": "Password updated successfully",
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
class VerifyEmailView(APIView):
    def get(self, request, token):
        try:
            user = verify_token(token, 'email_verification')
            user.is_verified = True
            user.save()
            response_data = {
                "status": "OK",
                "message": "Email verified successfully.",
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except ValueError as e:
            response_data = {
                "status": "FAILED",
                "message": str(e),
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)