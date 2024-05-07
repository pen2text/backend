from rest_framework import status, generics
from rest_framework.response import Response
from package_manager.serializers import PackagePlanDetailSerializer, PackagePlanDetailUpdateSerializer
from package_manager.models import PackagePlanDetails
from utils.format_errors import validation_error


class PackagePlanDetailCreateView(generics.CreateAPIView):
    queryset = PackagePlanDetails.objects.all()
    serializer_class = PackagePlanDetailSerializer

    def create(self, request, *args, **kwargs):
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
            "message": "Plan created successfully",
            "data": serializer.data,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

class PackagePlanDetailListView(generics.ListAPIView):
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
                "message": "Plan fetched successfully",
                "data": serializer.data,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except PackagePlanDetails.DoesNotExist:
            response_data = {
                "status": "FAILED",
                "message": "Plan not found",
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
     
class PackagePlanDetailDeleteView(generics.DestroyAPIView):
    queryset = PackagePlanDetails.objects.all()
    serializer_class = PackagePlanDetailSerializer
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        try:
            package_id = kwargs.get('id')
            instance = self.queryset.get(id=package_id)
            instance.delete()
            response_data = {
                "status": "OK",
                "message": "Plan deleted successfully",
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except PackagePlanDetails.DoesNotExist:
            response_data = {
                "status": "FAILED",
                "message": "Plan not found",
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

class PackagePlanDetailUpdateView(generics.UpdateAPIView):
    queryset = PackagePlanDetails.objects.all()
    serializer_class = PackagePlanDetailUpdateSerializer

    def update(self, request, *args, **kwargs):
        try:
            package_id = request.data.get('id')
            instance = self.queryset.get(id=package_id)
            serializer = self.get_serializer(instance, data=request.data)
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
                "message": "Plan updated successfully",
                "data": serializer.data,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except PackagePlanDetails.DoesNotExist:
            response_data = {
                "status": "FAILED",
                "message": "Plan not found",
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)