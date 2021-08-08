from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .api_views import RegisterAPIView, VerifyEmailAPIView, LoginAPIView, UserRetrieveDestroyAPIView, UserListAPIView, PasswordTokenCheckAPIView, RequestPasswordRestEmailAPIView, SetNewPasswordAPIView


app_name = 'authentication'

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('verify-email/', VerifyEmailAPIView.as_view(), name='email_verify'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('all-users/', UserListAPIView.as_view(), name='all_users'),
    path('delete-or-retrieve-user/<int:pk>/', UserRetrieveDestroyAPIView.as_view(), name='delete_user'),
    path('request-reset-password/', RequestPasswordRestEmailAPIView.as_view(), name='request_reset_password'),
    path('password-reset/<user_id_b64>/<token>/', PasswordTokenCheckAPIView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', SetNewPasswordAPIView.as_view(), name='password_reset_complete'),

]
