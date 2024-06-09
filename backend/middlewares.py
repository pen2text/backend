from user_management.models import UserActivities


class ActivityLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
                
        paths = ['/api/users/register/', 'api/converter/remote-convert', '/api/converter/convert']
        if request.path not in paths:
            user_id = request.user.id if request.user.is_authenticated else None
            data = {
                'user_id': user_id,
                'ip_address': request.META.get('REMOTE_ADDR'),
                'type': 'web-visitor'
            }
            UserActivities.objects.create(**data)    
        
        return response

