from django.contrib import admin
from .models import UserActivities, Users 

admin.site.site_header = 'User Management'
admin.site.site_title = 'User Management'
admin.site.index_title = 'User Management'
admin.site.site_url = '/users'
admin.site.register(Users)
admin.site.register(UserActivities)
