from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    password2 = serializers.CharField(max_length=68, min_length=6, write_only=True)
    
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name',  'password', 'password2')
    
    def validate(self, attrs):
        password = attrs.get('password', '')
        password2 = attrs.get('password2', '')
        
        if password != password2:
            raise serializers.ValidationError("passwords do not match")
        return attrs
    
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data.get('email'),
            first_name = validated_data.get('first_name'),
            last_name = validated_data.get('last_name'),
            password = validated_data.get('password'),
        )
        return user



class OTPSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, min_length=6)
    password = serializers.CharField(write_only=True, max_length=68)
    full_name = serializers.CharField(max_length=255, read_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'password', 'full_name', 'access_token']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        request = self.context.get('request')
        user = authenticate(request=request, email=email, password=password)

        if not user:
            raise AuthenticationFailed("Invalid credentials, try again.")
        if not user.is_active:
            raise AuthenticationFailed("Account is not active.")

        user_token = user.token()  

        return {
            'email': user.email,
            'id': user.id,
            'full_name': user.get_fullname,
            'access_token': str(user_token.get('access')),
        }