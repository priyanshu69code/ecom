# accounts/urls.py
from django.urls import path
from .views import RegisterView, RequestEmailOTPAPIView, VerifyEmailAPIView, RequestOTPAPIView, VerifyOTPAPIView, UserView
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'user'


email_urlpatterns = [
    path('email/register/', RegisterView.as_view(), name='register'),
    path('email/request-otp/', RequestEmailOTPAPIView.as_view(),
         name='request-email-otp'),
    path('email/verify-email/', VerifyEmailAPIView.as_view(),
         name='verify-emaill-otp'),
]

login_urlpatterns = [
    path('login/request-otp', RequestOTPAPIView.as_view(),
         name='login-request-otp'),
    path('login/verify-otp', VerifyOTPAPIView.as_view(), name='verify-login-otp'),
    path('', UserView.as_view(), name='user'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]


urlpatterns = email_urlpatterns + login_urlpatterns
