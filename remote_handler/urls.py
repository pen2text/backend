from rest_framework.urls import path
import remote_handler.views as views

urlpatterns = [
    path('api-token/create', views.RemoteAPITokenManagerCreateView.as_view(), name='remote-api-token-create'),
    path('api-token/list', views.RemoteAPITokenManagerListView.as_view(), name='remote-api-token-list'),
    path('api-token/delete/<uuid:id>', views.RemoteAPITokenManagerDeleteView.as_view(), name='remote-api-token-delete'),
]