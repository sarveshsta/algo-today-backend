from django.urls import path
from .views.auth_views import *

auth_urls = [
    path('request-otp/', RequestOTP.as_view()),
    path('verify-otp/', VerifyOTP.as_view()),
    path('signup/', UserSignup.as_view()),
    path('login/', UserLogin.as_view()),
    path('update-password/', ForgotPassword.as_view()),
    path('logout/', UserLogout.as_view()),
]

urlpatterns = auth_urls