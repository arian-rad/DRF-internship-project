from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .api_views import RegisterAPIView, VerifyEmailAPIView, LoginAPIView, UserRetrieveDestroyAPIView, UserListAPIView


app_name = 'authentication'

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('verify-email/', VerifyEmailAPIView.as_view(), name='email_verify'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('all-users/', UserListAPIView.as_view(), name='all_users'),
    path('delete-or-retrieve-user/<int:pk>/', UserRetrieveDestroyAPIView.as_view(), name='delete_user'),

]
