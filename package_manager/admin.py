from django.contrib import admin
from package_manager.models import PackagePlanDetails



admin.site.site_header = 'Package Manager'
admin.site.site_title = 'Package Manager'
admin.site.index_title = 'Package Manager'
admin.site.site_url = '/packages'
admin.site.register(PackagePlanDetails)
