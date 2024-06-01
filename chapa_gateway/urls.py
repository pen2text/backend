from django.urls import path
from . import views

urlpatterns = [
    path('chapa-payment/initiate', views.ChapaTransactionInitiateView.as_view(), name='chapa-initiate'),
    path('chapa-payment/verify/<uuid:pk>', views.ChapaTransactionVerifyView.as_view(), name='chapa-verify'),
    path('chapa-payment/webhook', views.ChapaWebhookView, name='chapa-webhook'),
]