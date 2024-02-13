from django.urls import path
from .views import *

urlpatterns = [
    path('request-otp/', RequestOTP.as_view()),
    path('verify-otp/', VerifyOTP.as_view()),
    path('signup/', UserSignup.as_view()),
    path('login/', UserLogin.as_view()),
]