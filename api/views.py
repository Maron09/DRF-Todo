from rest_framework.generics import GenericAPIView
from .serializers import UserSerializer, OTPSerializer
from rest_framework.response import Response
from rest_framework import status
from .utils import *
from rest_framework import authentication, permissions
from django.contrib.sites.shortcuts import get_current_site
from rest_framework_simplejwt.authentication import JWTAuthentication







class UserRegistration(GenericAPIView):
    serializer_class = UserSerializer
    
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = serializer.data
            
            send_code(user['email'])
            
            return Response({
                'data': user,
                'message': f"hi {user['first_name']} thanks for signing up a passcode has been sent to your email"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmail(GenericAPIView):
    serializer_class = OTPSerializer
    
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True) 
        otp_code = serializer.validated_data.get("otp")
        
        try:
            user_code_obj = OneTimePass.objects.get(code=otp_code)
            user = user_code_obj.user
            if not user.is_active:
                user.is_active = True
                user.save()
                return Response({
                    'message': 'User Account Is Active'
                }, status=status.HTTP_200_OK)
        except OneTimePass.DoesNotExist:
            return Response({
                'message': 'Invalid passcode'
            }, status=status.HTTP_404_NOT_FOUND)
        return Response({'message': 'OTP verified'}, status=status.HTTP_200_OK)