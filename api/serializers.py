from rest_framework import serializers
from .models import User



class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name',  'password1', 'password2')
    
    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({
                "password": "Passwords do not match"
            })
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