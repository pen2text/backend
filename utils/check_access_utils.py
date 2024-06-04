from datetime import timedelta
from package_manager.models import LimitedUsageSubscriptionPlans, PackagePlanDetails, PlanType, UnlimitedUsageSubscriptionPlans, UserAccessRecords
from user_management.models import Users
from django.utils import timezone




def check_free_unregistered_access(ip_address) -> bool:
    
    user_record = UserAccessRecords.objects.filter(ip_address=ip_address, user=None).first()
    package_plan = PackagePlanDetails.objects.get(plan_type=PlanType.FREE_UNREGISTERED_PACKAGE)
    if not user_record: 
        user_record = UserAccessRecords.objects.create(ip_address=ip_address, package_plan=package_plan)  
        response_data = {
            "status": True,
            "plan_type": PlanType.FREE_UNREGISTERED_PACKAGE,
            "usage_limit": package_plan.usage_limit,
            "usage_count": 0,
            "expire_date": None,
            "name": package_plan.name,
            "package": user_record,
        }
        return response_data
    
    # Get the current date
    today = timezone.now()
    
    # Get the start date of the current week and set time to 00:00
    start_of_week = today - timedelta(days=today.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)

    # Get the end date of the current week and set time to 23:59
    end_of_week = start_of_week + timedelta(days=6)
    end_of_week = end_of_week.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    if user_record.last_date_use <= end_of_week and user_record.usage_count >= package_plan.usage_limit:
        response_data = {
            "status": False,
            "plan_type": PlanType.FREE_UNREGISTERED_PACKAGE,
        }
        return response_data
    
    if user_record.last_date_use <= start_of_week:
        user_record.usage_count = 0
        user_record.save()
    
    response_data = {
        "status": True,
        "plan_type": PlanType.FREE_UNREGISTERED_PACKAGE,
        "usage_limit": package_plan.usage_limit,
        "usage_count": user_record.usage_count,
        "expire_date": end_of_week,
        "name": package_plan.name,
        "package": user_record,
    }
        
    return response_data

def check_free_access(user: Users) -> bool:
 
    user_record = UserAccessRecords.objects.filter(user=user).first()
    package_plan = PackagePlanDetails.objects.get(plan_type=PlanType.FREE_PACKAGE)
    if not user_record: 
        user_record = UserAccessRecords.objects.create(ip_address=None, user=user, package_plan=package_plan)
        
    # Get the current date
    today = timezone.now()
    
    # previous day
    yesterday = today - timedelta(days=package_plan.days)
    yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)

    # Get the end date of the current week and set time to 23:59
    new_day = yesterday + timedelta(days=package_plan.days)
    new_day = new_day.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    if user_record.last_date_use <= new_day and user_record.usage_count >= package_plan.usage_limit:
        response_data = {
            "status": False,
            "plan_type": PlanType.FREE_PACKAGE,
            "usage_limit": package_plan.usage_limit,
            "usage_count": user_record.usage_count,
            "expire_date": new_day,
            "name": package_plan.name,
        }
        return response_data
    
    if user_record.last_date_use <= yesterday:
        user_record.usage_count = 0
        user_record.save()
    
    response_data = {
        "status": True,
        "plan_type": PlanType.FREE_PACKAGE,
        "usage_limit": package_plan.usage_limit,
        "usage_count": user_record.usage_count,
        "expire_date": new_day,
        "name": package_plan.name,
        "package": user_record,
    }
    return response_data
        
def check_unlimited_usage_access(user: Users) -> bool:
    
    try:
        unlimited_package = UnlimitedUsageSubscriptionPlans.objects.filter(user_id=user.id).latest('created_at')
    except UnlimitedUsageSubscriptionPlans.DoesNotExist:
        response_data = {
            "status": False,
            "plan_type": PlanType.UNLIMITED_USAGE,
        }
        return response_data
    
    if unlimited_package.expire_date < timezone.now():
        response_data = {
            "status": False,
            "plan_type": unlimited_package.package_plan.plan_type,
        }
        return response_data
    
    response_data = {
        "status": True,
        "plan_type": unlimited_package.package_plan.plan_type,
        "usage_limit": 0,
        "usage_count": 0,
        "expire_date": unlimited_package.expire_date,
        "name": unlimited_package.package_plan.name,
        "package": unlimited_package,
    }
    return response_data
    
def check_limited_usage_access(user: Users) -> bool:

    try:
        limited_package = LimitedUsageSubscriptionPlans.objects.filter(user_id=user.id).latest('created_at')
    except LimitedUsageSubscriptionPlans.DoesNotExist:
        response_data = {
            "status": False,
            "plan_type": PlanType.LIMITED_USAGE,
        }
        return response_data
    
    if limited_package.package_detail.plan_type == PlanType.NON_EXPIRING_LIMITED_USAGE:
        if limited_package.usage_limit <= limited_package.usage_count:
            response_data = {
                "status": False,
                "plan_type": limited_package.package_detail.plan_type,
            }
            return response_data
        
        response_data = {
            "status": True,
            "plan_type": limited_package.package_detail.plan_type,
            "usage_limit": limited_package.usage_limit,
            "usage_count": limited_package.usage_count,
            "expire_date": None,
            "name": limited_package.package_detail.name,
            "package": limited_package,
        }
        return response_data
       
    if limited_package.expire_date < timezone.now() or limited_package.usage_limit <= limited_package.usage_count:
        response_data = {
            "status": False,
            "plan_type": PlanType.LIMITED_USAGE,
        }
        return response_data
    
    response_data = {
        "status": True,
        "plan_type": limited_package.package_detail.plan_type,
        "usage_limit": limited_package.usage_limit,
        "usage_count": limited_package.usage_count,
        "expire_date": limited_package.expire_date,
        "name": limited_package.package_detail.name,
        "package": limited_package,
    }
    return response_data

def check_access(request) -> bool:    
    if request.user.is_authenticated:
        user = request.user
        result = check_limited_usage_access(user)
        if result['status'] == True: return result

        result = check_unlimited_usage_access(user)
        if result['status'] == True: return result

        return check_free_access(user)
    else:
        ip_address = request.META.get('REMOTE_ADDR')
        return check_free_unregistered_access(ip_address)

def is_user_has_active_package(user: Users) -> bool:
    limited = check_limited_usage_access(user)    
    unlimited = check_unlimited_usage_access(user)
    
    return limited['status'] or unlimited['status']

def user_package_plan_status(user: Users):
    
    limited = check_limited_usage_access(user)    
    unlimited = check_unlimited_usage_access(user)
    
    if limited['status']: return limited
    if unlimited['status']: return unlimited
    
    return check_free_access(user)
