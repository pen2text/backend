from django.contrib import admin
from chapa_gateway.models import ChapaTransactions


admin.site.site_header = 'Transaction Manager'
admin.site.site_title = 'Transaction Manager'
admin.site.index_title = 'Transaction Manager'
admin.site.site_url = '/transactions'
admin.site.register(ChapaTransactions)