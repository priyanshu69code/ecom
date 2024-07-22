from rest_framework import serializers
from .models import User
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name',
                  'last_name', 'phone_number', 'username']

    def validate(self, data):
        required_fields = ['email', 'first_name',
                           'last_name', 'phone_number', 'username']
        missing_fields = [
            field for field in required_fields if not data.get(field)]
        if missing_fields:
            raise ValidationError(f'Missing required fields: {
                                  ", ".join(missing_fields)}')
        return data


class RequestOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()


class OTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
