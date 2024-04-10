from rest_framework.urls import path
import converter.views as views

urlpatterns = [
    path('convert', views.ConverterView.as_view(), name='convert'),
    path('remote-converter', views.ConvertUsingRemoteAPIView.as_view(), name='converter'),
]


