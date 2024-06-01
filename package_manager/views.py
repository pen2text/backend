from rest_framework import status, generics
from rest_framework.response import Response
from package_manager.serializers import PackagePlanDetailSerializer, PackagePlanDetailUpdateSerializer
from package_manager.models import PackagePlanDetails
from utils.format_errors import validation_error
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class PackagePlanDetailCreateView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = PackagePlanDetails.objects.all()
    serializer_class = PackagePlanDetailSerializer

    def create(self, request, *args, **kwargs):
        if request.user.role != 'admin':
            response_data = {
                "status": "FAILED",
                "message": "You are not authorized to create plan",
            }
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            response_data = {
                "status": "FAILED",
                "message": "validation error",
                "errors": validation_error(serializer.errors),
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        response_data = {
            "status": "OK",
            "message": "Package plan created successfully",
            "data": serializer.validated_data,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

class PackagePlanDetailListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = PackagePlanDetails.objects.all()
    serializer_class = PackagePlanDetailSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = {
            "status": "OK",
            "message": "Plans fetched successfully",
            "data": serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)

class PackagePlanDetailRetrieveView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = PackagePlanDetails.objects.all()
    serializer_class = PackagePlanDetailSerializer
    lookup_field = 'id'
    
    def retrieve(self, request, *args, **kwargs):
        try:
            package_id = kwargs.get('id')
            instance = self.queryset.get(id=package_id)
            serializer = self.get_serializer(instance)
            response_data = {
                "status": "OK",
                "message": "Package fetched successfully",
                "data": serializer.data,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except PackagePlanDetails.DoesNotExist:
            response_data = {
                "status": "FAILED",
                "message": "Package not found",
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
     
class PackagePlanDetailDeleteView(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = PackagePlanDetails.objects.all()
    serializer_class = PackagePlanDetailSerializer
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        if request.user.role != 'admin':
            response_data = {
                "status": "FAILED",
                "message": "You are not authorized to delete plan",
            }
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)
        
        try:
            package_id = kwargs.get('id')
            instance = self.queryset.get(id=package_id)
            instance.delete()
            response_data = {
                "status": "OK",
                "message": "Package deleted successfully",
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except PackagePlanDetails.DoesNotExist:
            response_data = {
                "status": "FAILED",
                "message": "Package not found",
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

class PackagePlanDetailUpdateView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = PackagePlanDetails.objects.all()
    serializer_class = PackagePlanDetailUpdateSerializer

    def update(self, request, *args, **kwargs):
        if request.user.role != 'admin':
            response_data = {
                "status": "FAILED",
                "message": "You are not authorized to update plan",
            }
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)
        
        try:
            package_id = request.data.get('id')
            instance = self.queryset.get(id=package_id)
        except PackagePlanDetails.DoesNotExist:
            response_data = {
                "status": "FAILED",
                "message": "Package Plan not found",
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if not serializer.is_valid():
            response_data = {
                "status": "FAILED",
                "message": "validation error",
                "errors": validation_error(serializer.errors),
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_update(serializer)
        response_data = {
            "status": "OK",
            "message": "Plan updated successfully",
            "data": serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)