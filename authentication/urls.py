from django.urls import path
from authentication import views

urlpatterns = [
    path('auth/forgot-password/<str:email>/', views.ForgotPasswordView.as_view(), name='forgot-password'),
    path('auth/reset-password/', views.ResetPasswordView.as_view(), name='reset-password'),
]
