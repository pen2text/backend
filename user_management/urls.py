from django.urls import path
import user_management.views as views
urlpatterns = [
    path('auth/register', views.UserRegistrationView.as_view(), name='user-register'),
    path('users/delete/<uuid:id>', views.UserDeleteView.as_view(), name='user-delete'),
    path('users/get-all', views.UserListView.as_view(), name='user-list'),
    path('users/is-email-exists/<str:email>', views.CheckEmailExistsView.as_view(), name='check-email-exists'),
    path('users/get-by-id/<uuid:id>', views.UserRetrieveByIdView.as_view(), name='user-retrieve-by-id'),
    path('users/get-by-email/<str:email>', views.UserRetrieveByEmailView.as_view(), name='user-retrieve-by-email'),
    path('users/update', views.UserUpdateView.as_view(), name='user-update'),
    path('users/update-role', views.UpdateRoleView.as_view(), name='update-role'),
]
