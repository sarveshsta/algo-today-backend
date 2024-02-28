import jwt
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q

from ..models import PhoneOTP, User
from ..utils import send_otp
from ..serilaizers import *


class UserDetails(APIView):
    def get(self, request):
        try:
            users = User.objects.all()
            api_response = []
            for user in users:
                api_response.append({
                    "id": str(user.id),
                    "name": user.name,
                    "phone": user.phone,
                    "email": user.email,
                    
                })
            return Response({"message":"User details", "success":True, "data": api_response}, status=status.HTTP_200_OK)
        except Exception as e: return Response({"message": f"Error - {str(e)}", "success":False}, status=status.HTTP_400_BAD_REQUEST)


