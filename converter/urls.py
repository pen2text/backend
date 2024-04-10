from rest_framework.urls import path
import converter.views as views

urlpatterns = [
    path('converter/convert', views.ConverterView.as_view(), name='convert'),
    path('converter/remote-converter', views.ConvertUsingRemoteAPIView.as_view(), name='converter'),
]


