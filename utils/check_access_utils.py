from datetime import timedelta
from package_manager.models import LimitedUsageSubscriptionPlans, PackagePlanDetails, PlanType, UnlimitedUsageSubscriptionPlans, UserAccessRecords
from user_management.models import Users
from django.utils import timezone

# response_data = {
#     'status': 'FAILED',
#     'message': 'You have reached the limit of your package plan',
#     'plan_type': PlanType.LIMITED_USAGE,
#     'usage_limit': 0
# }



def check_free_registered_access(user: Users, ip_address) -> bool:
 
    user_record = UserAccessRecords.objects.filter(ip_address=ip_address, user=user).first()
    package_plan = PackagePlanDetails.objects.get(plan_type=PlanType.FREE_PACKAGE)
    if not user_record: 
        UserAccessRecords.objects.create(ip_address=ip_address, user=user, package_plan=package_plan)
        return True, PlanType.LIMITED_USAGE, package_plan.usage_limit
    
    # Get the current date
    today = timezone.now()
    
    #
    yesterday = today - timedelta(days=package_plan.days)
    yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)

    # Get the end date of the current week and set time to 23:59
    new_day = yesterday + timedelta(days=package_plan.days)
    new_day = new_day.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    if user_record.last_date_use <= new_day and user_record.usage_count >= package_plan.usage_limit:
        return False, PlanType.LIMITED_USAGE, 0
    
    if user_record.last_date_use <= yesterday:
        user_record.usage_count = 0
        user_record.save()
        
    return True, PlanType.LIMITED_USAGE, package_plan.usage_limit - user_record.usage_count

def check_free_access(ip_address) -> bool:
    
    user_record = UserAccessRecords.objects.filter(ip_address=ip_address, user=None).first()
    package_plan = PackagePlanDetails.objects.get(plan_type=PlanType.FREE_UNREGISTERED_PACKAGE)
    if not user_record: 
        UserAccessRecords.objects.create(ip_address=ip_address, package_plan=package_plan)  
        return True, PlanType.LIMITED_USAGE, package_plan.usage_limit
    
    # Get the current date
    today = timezone.now()
    
    # Get the start date of the current week and set time to 00:00
    start_of_week = today - timedelta(days=today.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)

    # Get the end date of the current week and set time to 23:59
    end_of_week = start_of_week + timedelta(days=6)
    end_of_week = end_of_week.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    if user_record.last_date_use <= end_of_week and user_record.usage_count >= package_plan.usage_limit:
        return False, PlanType.LIMITED_USAGE, 0
    
    if user_record.last_date_use <= start_of_week:
        user_record.usage_count = 0
        user_record.save()
        
    return True, PlanType.LIMITED_USAGE, package_plan.usage_limit - user_record.usage_count

def check_unlimited_usage_access(user: Users) -> bool:
    
    try:
        unlimited_package = UnlimitedUsageSubscriptionPlans.objects.filter(user_id=user.id).latest('created_at')
    except UnlimitedUsageSubscriptionPlans.DoesNotExist:
        return False, PlanType.UNLIMITED_USAGE
    
    if unlimited_package.expire_date < timezone.now():
        return False, PlanType.UNLIMITED_USAGE
    
    return True, PlanType.UNLIMITED_USAGE
    
def check_limited_usage_access(user: Users) -> bool:

    try:
        limited_package = LimitedUsageSubscriptionPlans.objects.filter(user_id=user.id).latest('created_at')
    except LimitedUsageSubscriptionPlans.DoesNotExist:
        return False, PlanType.LIMITED_USAGE, 0
    
    if limited_package.package_detail.plan_type == PlanType.NON_EXPIRING_LIMITED_USAGE:
        if limited_package.usage_limit <= limited_package.usage_count:
            return False, PlanType.LIMITED_USAGE, 0
        return True, PlanType.LIMITED_USAGE, limited_package.package_detail.usage_limit - limited_package.usage_count
       
    if limited_package.expire_date < timezone.now() or limited_package.usage_limit <= limited_package.usage_count:
        return False, PlanType.LIMITED_USAGE, 0
    return True, PlanType.LIMITED_USAGE, limited_package.package_detail.usage_limit - limited_package.usage_count

def check_access(user: Users, ip_address) -> bool:
    if user:
        result = check_limited_usage_access(user)
        if result[0] == True: return result

        result = check_unlimited_usage_access(user)
        if result[0] == True: return result

        return check_free_registered_access(user, ip_address)
    else:
        return check_free_access(ip_address)

def is_user_has_active_package(user: Users) -> bool:
    limited = check_limited_usage_access(user)
    unlimited = check_unlimited_usage_access(user)
    return limited[0] or unlimited[0]