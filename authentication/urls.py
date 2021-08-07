from django.urls import path
from .api_views import RegisterAPIView, VerifyEmailAPIView


app_name = 'authentication'



urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('verify-email/', VerifyEmailAPIView.as_view(), name='email_verify'),

]
