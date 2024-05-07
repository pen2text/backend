from django.urls import path
import package_manager.views as views

urlpatterns = [
    path('package-plan/create', views.PackagePlanDetailCreateView.as_view(), name='package-plan-create'),
    path('package-plan/list', views.PackagePlanDetailListView.as_view(), name='package-plan-list'),
    path('package-plan/retrieve/<uuid:id>', views.PackagePlanDetailRetrieveView.as_view(), name='package-plan-retrieve'),
    path('package-plan/update', views.PackagePlanDetailUpdateView.as_view(), name='package-plan-update'),
    path('package-plan/delete/<uuid:id>', views.PackagePlanDetailDeleteView.as_view(), name='package-plan-delete'),
]