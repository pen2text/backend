from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/list-users', views.PaginatedUserListView.as_view(), name='paginated-list-users'),
    path('dashboard/subscriptions', views.SubscriptionPlanByPlanTypeListView.as_view(), name='subscription-plans-by-plan-type'),
    path('dashboard/convert/count', views.ConvertCountEachMonthView.as_view(), name='convert-count-each-month'),
    path('dashboard/activities/count', views.UserActivityCountView.as_view(), name='user-activity-count'),
    path('dashboard/data', views.DashboardDataView.as_view(), name='dashboard-data'),
]