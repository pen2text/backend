from datetime import timedelta
from django.utils import timezone
from django.db.models import Count, Sum, Q, F
from chapa_gateway.models import ChapaStatus, ChapaTransactions
from package_manager.models import LimitedUsageSubscriptionPlans, PackagePlanDetails, PlanType, UnlimitedUsageSubscriptionPlans, UserAccessRecords
from user_management.models import UserActivities, Users
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from user_management.serializers import UserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication  
from django.db.models.functions import ExtractMonth



class PaginatedUserListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        current_user = request.user
        if current_user.role != 'admin':
            response_data = {
                'status': 'FAILED',
                'message': 'You are not authorized to view users',
            }
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)
        
        page_size = int(request.query_params.get('page_size', 10))
        page_number = int(request.query_params.get('page', 1))
        
        start_index = max(page_number - 1, 0) * page_size
        users = Users.objects.exclude(id=current_user.id)
        
        paginated_users = users[start_index:start_index + page_size]
        serializer = UserSerializer(paginated_users, many=True)
        response_data = {
            'status': 'OK',
            'message': 'Users retrieved successfully',
            'data': serializer.data,
            'total_count': users.count(),
            'page_size': page_size,
            'page_number': page_number,
        }
        return Response(response_data, status=status.HTTP_200_OK)

class SubscriptionPlanByPlanTypeListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        current_user = request.user
        if current_user.role != 'admin':
            response_data = {
                'status': 'FAILED',
                'message': 'You are not authorized to view subscription plans',
            }
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)
        
        days = int(request.query_params.get('days', 30))
    
        days_ago = timezone.now() - timedelta(days=30)
        
        # Count of users who have accessed the system in the last [days] days for each plan type
        regular_user_count = UserAccessRecords.objects.filter(package_plan__plan_type=PlanType.FREE_PACKAGE, last_date_use__gte= days_ago).count()
        guest_user_count = UserAccessRecords.objects.filter(package_plan__plan_type=PlanType.FREE_UNREGISTERED_PACKAGE, last_date_use__gte= days_ago).count()
        premium_user_count = UserAccessRecords.objects.filter(package_plan__plan_type=PlanType.PREMIER_TRIAL_PACKAGE, last_date_use__gte= days_ago).count()
        
        unlimited_usage_count = UnlimitedUsageSubscriptionPlans.objects.filter(created_at__gte=days_ago).count()
        
        limited_usage_count = LimitedUsageSubscriptionPlans.objects.filter(package_detail__plan_type=PlanType.LIMITED_USAGE,created_at__gte=days_ago).count()
        custom_limited_count = LimitedUsageSubscriptionPlans.objects.filter(package_detail__plan_type=PlanType.CUSTOM_LIMITED_USAGE,created_at__gte=days_ago).count()
        non_expiring_limited_count = LimitedUsageSubscriptionPlans.objects.filter(package_detail__plan_type=PlanType.NON_EXPIRING_LIMITED_USAGE,created_at__gte=days_ago).count()
        
        response_data = {
            'status': 'SUCCESS',
            'message': 'Subscription plans data retrieved successfully',
            'data': {
                'regular_user_count': regular_user_count,
                'guest_user_count': guest_user_count,
                'unlimited_usage_count': unlimited_usage_count,
                'limited_usage_count': limited_usage_count,
                'custom_limited_count': custom_limited_count,
                'non_expiring_limited_count': non_expiring_limited_count,
                'premium_user_count': premium_user_count,
            }
        }
        
        return Response(response_data, status=status.HTTP_200_OK)

class UserActivityCountView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        current_user = request.user
        if current_user.role != 'admin':
            response_data = {
                'status': 'FAILED',
                'message': 'You are not authorized to view user activity',
            }
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)
        
        days = int(request.query_params.get('days', 30))
        days_ago = timezone.now() - timedelta(days=30)
        
        # Count of users who have accessed the system in the last [days] days
        visitor_count = UserActivities.objects.filter(activity_type='web-visitor', created_at__gte= days_ago).count()
        user_register_count = UserActivities.objects.filter(activity_type='user-register', created_at__gte= days_ago).count()
        convert_user_count = UserActivities.objects.filter(activity_type='convert-user', created_at__gte= days_ago).count()
        convert_other_system_count = UserActivities.objects.filter(activity_type='convert-other-system', created_at__gte= days_ago).count()
        
        response_data = {
            'status': 'OK',
            'message': 'User activity data retrieved successfully',
            'data': {
                'visitor_count': visitor_count,
                'user_register_count': user_register_count,
                'convert_user_count': convert_user_count,
                'convert_other_system_count': convert_other_system_count,
            }
        }
        
        return Response(response_data, status=status.HTTP_200_OK)       

class ConvertCountEachMonthView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        current_user = request.user
        if current_user.role != 'admin':
            response_data = {
                'status': 'FAILED',
                'message': 'You are not authorized to view user activity',
            }
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)
        
        months_count = int(request.query_params.get('months', 12))
        
        start_date = timezone.now() - timedelta(days=months_count * 30)
        
        # count of conversion for each month
        converted_users = (
            UserActivities.objects.filter(
                created_at__gte=start_date,
                activity_type__in=['convert-user', 'convert-other-system']
            )
            .annotate(month=ExtractMonth('created_at'))
            .values('month')
            .annotate(convert_count=Count('id'))
            .order_by('month')
        )
        response_data = {
            'status': 'OK',
            'message': 'User conversion count for each month retrieved successfully',
            'data': list(converted_users)
        }
        return Response(response_data, status=status.HTTP_200_OK)
               
class DashboardDataView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        current_user = request.user
        if current_user.role != 'admin':
            response_data = {
                'status': 'FAILED',
                'message': 'You are not authorized to view user activity',
            }
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)
        
        days = 30
        days_ago = timezone.now() - timedelta(days=days)
        
        # total revenue for the last 30 days
        total_revenue = ChapaTransactions.objects.filter(status=ChapaStatus.SUCCESS).aggregate(total_revenue=Sum('amount'))['total_revenue']
        monthly_revenue = ChapaTransactions.objects.filter(created_at__gte=days_ago, status=ChapaStatus.SUCCESS).aggregate(total_revenue=Sum('amount'))['total_revenue']
        
        # subscription for the last 30 days
        total_subscription = UnlimitedUsageSubscriptionPlans.objects.filter().count()
        monthly_subscription = UnlimitedUsageSubscriptionPlans.objects.filter(created_at__gte=days_ago).count()
        
        total_subscription += LimitedUsageSubscriptionPlans.objects.filter().count()
        monthly_subscription += LimitedUsageSubscriptionPlans.objects.filter(created_at__gte=days_ago).count()
        
        # user count for the last 30 days
        total_user_count = Users.objects.count()
        monthly_user_count = Users.objects.filter(created_at__gte=days_ago).count()
        
        # premium user count for the last 30 days
        premium_users_count = Users.objects.filter(
                Q(unlimitedusagesubscriptionplans__isnull=False) | 
                Q(limitedusagesubscriptionplans__isnull=False)
            ).distinct().count()
        
        new_premium_users_count = Users.objects.filter(
                Q(unlimitedusagesubscriptionplans__created_at__gte=days_ago) | 
                Q(limitedusagesubscriptionplans__created_at__gte=days_ago)
            ).distinct().count()
        
        
        # regular user and premium user count
        regular_user_count = Users.objects.filter(
            Q(unlimitedusagesubscriptionplans__isnull=True) & 
            Q(limitedusagesubscriptionplans__isnull=True)
        ).count()
        
        # most subscribed packages for the last 30 days
        most_package_count = 5
        
        limited_usage_packages = (
            LimitedUsageSubscriptionPlans.objects.filter(created_at__gte=days_ago)
            .values(package_name=F('package_detail__name'))
            .annotate(total_revenue=Sum('transaction__amount'))
        )
        
        unlimited_usage_packages = (
            UnlimitedUsageSubscriptionPlans.objects.filter(created_at__gte=days_ago)
            .values(package_name=F('package_plan__name'))
            .annotate(total_revenue=Sum('transaction__amount'))
        )
        
        # Combine and sort
        combined_packages = (
            limited_usage_packages.union(unlimited_usage_packages)
            .order_by('-total_revenue')[:most_package_count]
        )
        
        
        
        response_data = {
            'status': 'OK',
            'message': 'Dashboard data retrieved successfully',
            'data': {
                'revenue': {
                    'total_revenue': total_revenue,
                    'monthly_revenue': monthly_revenue,
                },
                'subscription': {
                    'total_subscription': total_subscription,
                    'monthly_subscription': monthly_subscription,
                },
                'user_count': {
                    'total_user_count': total_user_count,
                    'monthly_user_count': monthly_user_count,
                },
                'premium_user_count': {
                    'premium_users_count': premium_users_count,
                    'new_premium_users_count': new_premium_users_count,
                },
                'users': {
                    'regular_user_count': regular_user_count,
                    'premium_user_count': premium_users_count,
                },
                'most_subscribed_packages': combined_packages,
            }
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
class PaginatedPackagePlanDetailsListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        current_user = request.user
        if current_user.role != 'admin':
            response_data = {
                'status': 'FAILED',
                'message': 'You are not authorized to view users',
            }
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)
        
        page_size = int(request.query_params.get('page_size', 10))
        page_number = int(request.query_params.get('page', 1))
        
        start_index = max(page_number - 1, 0) * page_size
        packages = PackagePlanDetails.objects.all()
        
        paginated_users = packages[start_index:start_index + page_size]
        serializer = UserSerializer(paginated_users, many=True)
        response_data = {
            'status': 'OK',
            'message': 'Packages retrieved successfully',
            'data': serializer.data,
            'total_count': packages.count(),
            'page_size': page_size,
            'page_number': page_number,
        }
        return Response(response_data, status=status.HTTP_200_OK)  
        