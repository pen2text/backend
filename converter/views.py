from conversion_management.models import ConversionHistories
from package_manager.models import PlanType
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from user_management.models import UserActivities
from utils.upload_to_cloudinary import convert_image_to_text, upload_image
from .serializers import ConverterSerializer, ImageUploadSerializer
from utils.format_errors import validation_error
from utils.check_access_utils import check_access, is_user_has_active_package
from rest_framework.parsers import MultiPartParser, FormParser



class ConvertUsingRemoteAPIView(generics.GenericAPIView):
    serializer_class = ConverterSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
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
        
        result = check_access(request.user, request.META.get('REMOTE_ADDR'))

        # for index, image in serializer.validated_data:
        #     #process image call ml model
            
        #     response_data['data'].append({
        #         'index': index,
        #         'text-content': 'This is a sample text content',
        #         'state': 'OK',
        #     })
        
        #Log server image conversion activity
        # data = {
        #     "user_id": user.id,
        #     "ip_address": request.META.get('REMOTE_ADDR'),
        #     "type": "server_conversion"
        # }
        # UserActivities.objects.create(**data)
        
        return Response(response_data, status=status.HTTP_200_OK)
    
class ConverterView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    
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
        
        
        is_premier_user = False
        if request.user.is_authenticated:
            is_premier_user = is_user_has_active_package(request.user)
        
        
        # don't allow batch upload for free users
        if not is_premier_user and len(files) > 1:
            response_data = {
                'status': 'FAILED',
                'message': 'Batch upload is not allowed for free users'
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        # check whether the user has reached the limit of the package plan
        # user_package = check_access(request.user, request.META.get('REMOTE_ADDR'))
        user_package = check_access(request)
        
        if user_package[0] == False:
            response_data = {
                'status': 'FAILED',
                'message': 'You have reached the limit of your package plan',
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST) 
        
        if user_package[1] != PlanType.UNLIMITED_USAGE and len(files) > user_package[2]:
            response_data = {
                'status': 'FAILED',
                'message': "You don't have enough package plan to convert all the images",
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
           
        try:
            response_data = {
                'status': 'OK',
                'message': 'Images processed successfully',
                'data': []
            }
            
            # convert the images to text 
            conversion_histories = []
            for file in files:

                # process image
                processed_text_content = convert_image_to_text(file)
                response_data['data'].append({
                    'text-content': processed_text_content,
                    'succuss': 'OK',
                })
                
                if is_premier_user:
                    processed_image_url = upload_image(file)
                    
                    # Create ConversionHistories instance
                    conversion_history = ConversionHistories(
                        user= request.user,
                        text_content= processed_text_content,
                        image_url= processed_image_url
                    )
                    conversion_histories.append(conversion_history)
            if is_premier_user:
                ConversionHistories.objects.bulk_create(conversion_histories)
            
            # update user package usage count
            if user_package[1] != PlanType.UNLIMITED_USAGE:
                user_package[3].usage_count += len(files)
                user_package[3].save()
                     
#         #Log user image conversion activity
#         # data = {
#         #     "user_id": user.id,
#         #     "ip_address": request.META.get('REMOTE_ADDR'),
#         #     "type": "user_conversion"
#         # }
#         # UserActivities.objects.create(**data)

            return Response(response_data, status=status.HTTP_200_OK)
        except:
            response_data = {
                'status': 'FAILED',
                'message': 'An error occurred while processing the image',
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)