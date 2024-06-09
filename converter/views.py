from conversion_management.models import ConversionHistories
from package_manager.models import PlanType
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from user_management.models import UserActivities
from utils.jwt_token_utils import PrivateKeyAuthentication
from utils.upload_to_cloudinary import convert_image_to_text, upload_image
from .serializers import ImageUploadSerializer
from utils.format_errors import validation_error
from utils.check_access_utils import check_access, user_package_plan_status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from django.db import transaction


    
class ConverterView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    # serializer_class = ImageUploadSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = ImageUploadSerializer(data=request.data)
               
        if not serializer.is_valid():
            response_data = {
                'status': 'FAILED',
                'message': 'Validation failed',
                'errors': validation_error(serializer.errors)
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        files = serializer.validated_data.get('images')
        
        # get user's package plan
        user_package = check_access(request)

        # check if user is a premier user
        is_premier_user = False
        if user_package['status'] and user_package['plan_type'] not in [PlanType.FREE_PACKAGE, PlanType.FREE_UNREGISTERED_PACKAGE, PlanType.PREMIER_TRIAL_PACKAGE]:
            is_premier_user = True
        
        
        # don't allow batch upload for free users
        if not is_premier_user and len(files) > 1:
            response_data = {
                'status': 'FAILED',
                'message': 'Batch upload is not allowed for free users'
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        
        # check if user has reached the limit of their package plan
        if user_package['status'] == False:
            response_data = {
                'status': 'FAILED',
                'message': 'You have reached the limit of your package plan',
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST) 
        
        # check if user has enough package plan to convert all the images
        remaining_usage = user_package['usage_limit'] - user_package['usage_count']
        if user_package['plan_type'] != PlanType.UNLIMITED_USAGE and len(files) > remaining_usage:
            response_data = {
                'status': 'FAILED',
                'message': "You don't have enough package plan to convert all the images",
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        # process the images one by one  
        try:
            with transaction.atomic(): 

                response_data = {
                    'status': 'OK',
                    'message': 'Images processed successfully',
                    'data': []
                }
                
                for file in files:

                    # process image using model and get text content
                    processed_text_content = convert_image_to_text(file)
                    result = {
                        'text-content': processed_text_content,
                        'success': 'OK',
                    }
                    
                    if is_premier_user:
                        processed_image_url = upload_image(file)
                        
                        # Create ConversionHistories instance
                        conversion_history = ConversionHistories.objects.create(
                            user= request.user,
                            text_content= processed_text_content,
                            image_url= processed_image_url
                        )
                        result['image_url'] = processed_image_url
                        result['conversion_id'] = conversion_history.id
                    
                    response_data['data'].append(result)  
                
                # update user package usage count
                if user_package['plan_type'] != PlanType.UNLIMITED_USAGE:
                    user_package["package"].usage_count += len(files)
                    user_package["package"].save()
                        
                # Log user image conversion activity
                data = {
                    "user": request.user,
                    "ip_address": request.META.get('REMOTE_ADDR'),
                    "type": "convert-user"
                }
                UserActivities.objects.create(**data)

                return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            transaction.set_rollback(True)

            response_data = {
                'status': 'FAILED',
                'message': 'An error occurred while processing the image',
                'errors': {
                    "server_error": str(e)
                }
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ConvertUsingRemoteAPIView(generics.GenericAPIView):
    authentication_classes = [PrivateKeyAuthentication]
    permission_classes = [IsAuthenticated]
    
    parser_classes = (MultiPartParser, FormParser)
    # serializer_class = ImageUploadSerializer
    def post(self, request, *args, **kwargs):
        serializer = ImageUploadSerializer(data=request.data)
               
        if not serializer.is_valid():
            response_data = {
                'status': 'FAILED',
                'message': 'Validation failed',
                'errors': validation_error(serializer.errors)
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        files = serializer.validated_data.get('images')
        
        # get user's package plan
        user_package = user_package_plan_status(request.user)

        # check if user has a premier feature access
        if not user_package['status'] or user_package['plan_type'] == PlanType.FREE_PACKAGE:
            response_data = {
                'status': 'FAILED',
                'message': 'You are not allowed to use this feature',
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            
        
        # check if user has reached the limit of their package plan
        if user_package['status'] == False:
            response_data = {
                'status': 'FAILED',
                'message': 'You have reached the limit of your package plan',
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST) 
        
        # check if user has enough package plan to convert all the images
        remaining_usage = user_package['usage_limit'] - user_package['usage_count']
        if user_package['plan_type'] != PlanType.UNLIMITED_USAGE and len(files) > remaining_usage:
            response_data = {
                'status': 'FAILED',
                'message': "You don't have enough package plan to convert all the images",
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        # process the images one by one  
        try:
            response_data = {
                'status': 'OK',
                'message': 'Images processed successfully',
                'data': []
            }
            
            # process image
            for file in files:
                processed_text_content = convert_image_to_text(file)
                response_data['data'].append({
                    'text-content': processed_text_content,
                    'succuss': 'OK',
                })
                
            
            # update user package usage count
            if user_package['plan_type'] != PlanType.UNLIMITED_USAGE:
                user_package["package"].usage_count += len(files)
                user_package["package"].save()
                     
            # Log user image conversion activity
            data = {
                "user": request.user,
                "ip_address": request.META.get('REMOTE_ADDR'),
                "type": "convert-other-system"
            }
            UserActivities.objects.create(**data)

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            response_data = {
                'status': 'FAILED',
                'message': 'An error occurred while processing the image',
                'errors': {
                    "server_error": str(e)
                }
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
