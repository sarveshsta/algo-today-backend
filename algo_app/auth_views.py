import random
from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q

from .models import PhoneOTP, User
from .utils import send_otp
from .serilaizers import *


class RequestOTP(APIView):
    def post(self, request):
        data = self.request.data
        phone = data['phone']
        try:
            otp = random.randint(100000, 999999)
            send_otp(otp, phone)

            phoneOTP_obj, create_status = PhoneOTP.objects.get_or_create(phone=phone)
            phoneOTP_obj.otp = otp
            print("OTP", otp)
            phoneOTP_obj.save()
            
            return Response({"message": "OTP sent", "success":True, "data":{"otp": otp}}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message": f"Error - {e}", "success":False}, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTP(APIView):
    def post(self, request):
        data = self.request.data
        phone = data['phone']
        otp = data['otp']

        try:
            phoneotp_obj = PhoneOTP.objects.get(phone=phone, otp=otp)
            phoneotp_obj.is_verified = True
            phoneotp_obj.save()
        except PhoneOTP.DoesNotExist:
            return Response({"message": "Invalid OTP", "success":False}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"message":f"Error {e}", "success":False}, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    serialzer_class = LoginSerializer
    def post(self, request):
        data = self.request.data
        serializer = self.serialzer_class(data=data)

        if not data.is_valid():
            return Response({"message": str(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)
        
        phone = data['phone']
        otp = data['otp']
        password = data['password']

        try:
            PhoneOTP.objects.get(phone=phone, otp=otp, is_verified=True)
            user = User.objects.get(phone=phone)
            # user = authenticate(request, username=user.email, password=make_password(password))
            if check_password(password, user.password):
                login(request, user)
                # token = self._generate_jwt_token(user)
                return Response({"message": "Login successful", "success": True}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid credentials", "success": False}, status=status.HTTP_401_UNAUTHORIZED)
        except PhoneOTP.DoesNotExist:
            return Response({"message": "Invalid OTP", "success":False}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": f"Error {e}", "success": False}, status=status.HTTP_400_BAD_REQUEST)
        
    # def _generate_jwt_token(self, user):
    #     payload = {
    #         'user_id': str(user.id),
    #         'exp': datetime.utcnow() + timedelta(days=1),  # Token expiration time (1 day in this example)
    #         'iat': datetime.utcnow(),  # Issued at time
    #     }
    #     token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256').decode('utf-8')
    #     return token


class UserSignup(APIView):
    serialzer_class = SignupSerializer
    def post(self, request):
        data = self.request.data
        serializer = self.serialzer_class(data=data)

        if not data.is_valid():
            return Response({"message": str(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            phone = data['phone']
            otp = data['otp']
            email = data['email']
            name = data['name']
            password = data['password']

            PhoneOTP.objects.get(phone=phone, otp=otp, is_verified=True)
            if User.objects.filter(Q(phone=phone)|Q(email=email)).exists():
                return Response({"message":"Email/Phone already exists", "success":False}, status=status.HTTP_400_BAD_REQUEST)
            User.objects.create(email=email, phone=phone, name=name, password=make_password(password))
            return Response({"message": "Signup successful", "success": True}, status=status.HTTP_201_CREATED)
        except PhoneOTP.DoesNotExist:
            return Response({"message": "Invalid OTP", "success":False}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"message": f"Error {e}", "success": False}, status=status.HTTP_400_BAD_REQUEST)
        

class ForgotPassword(APIView):
    serialzer_class = LoginSerializer
    def post(self, request):
        data = self.request.data
        serializer = self.serialzer_class(data=data)

        if not data.is_valid():
            return Response({"message": str(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)
        
        phone = data['phone']
        otp = data['otp']
        password = data['password']

        try:
            PhoneOTP.objects.get(phone=phone, otp=otp, is_verified=True)
            user = User.objects.get(phone=phone)
            
            if check_password(password, user.password):
                user.password = make_password(password=password)       
                return Response({"message": "Login successful", "success": True}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid credentials", "success": False}, status=status.HTTP_401_UNAUTHORIZED)
        except PhoneOTP.DoesNotExist:
            return Response({"message": "Invalid OTP", "success":False}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": f"Error {e}", "success": False}, status=status.HTTP_400_BAD_REQUEST)

                