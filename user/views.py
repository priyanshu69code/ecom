from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer, RequestOTPSerializer, OTPSerializer
from rest_framework.throttling import SimpleRateThrottle
from .models import User, OTP
import random
from django.utils import timezone
from datetime import timedelta
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


class OTPThrottle(SimpleRateThrottle):
    rate = '1/m'

    def get_cache_key(self, request, view):
        email = request.data.get('email')
        return f'{email}:{self.scope}'

    def parse_rate(self, rate):
        num_requests, duration = 1, 600
        return (num_requests, duration)


# Create your views here.


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Registration successful. Please verify your email.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestEmailOTPAPIView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [OTPThrottle]

    def post(self, request):
        serializer = RequestOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                otp_record = OTP.objects.filter(user=user)
                if otp_record:
                    otp_record.delete()
                if user.is_verified:
                    return Response({'message': 'User is already verified'}, status=status.HTTP_400_BAD_REQUEST)
                # Add your OTP generation and sending logic here
                otp = ''.join(random.choices('0123456789', k=6))
                OTP.objects.create(user=user, otp=otp)
                print(f'OTP for {user.email}: {otp}')
                return Response({'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = OTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            try:
                user = User.objects.get(email=email)
                otp_record = OTP.objects.filter(
                    user=user, otp=otp, created_at__gte=timezone.now() - timedelta(minutes=10)).first()
                if user.is_verified:
                    return Response({'message': 'User is already verified'}, status=status.HTTP_400_BAD_REQUEST)

                if not otp_record:
                    return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
                otp_record.delete()
                user.is_verified = True
                user.save()
                token = generate_jwt_token(user)
                return Response({'message': 'OTP verified successfully', 'token': token}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
            except OTP.DoesNotExist:
                return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
            except AttributeError:
                return Response({'message': 'OTP expired'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestOTPAPIView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [OTPThrottle]

    def post(self, request):
        serializer = RequestOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                otp_record = OTP.objects.filter(user=user)
                if otp_record:
                    otp_record.delete()
                if not user.is_verified:
                    return Response({'message': 'User is not verified'}, status=status.HTTP_400_BAD_REQUEST)
                # Add your OTP generation and sending logic here
                otp = ''.join(random.choices('0123456789', k=6))
                OTP.objects.create(user=user, otp=otp)
                print(f'OTP for {user.email}: {otp}')
                return Response({'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = OTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            try:
                user = User.objects.get(email=email)
                otp_record = OTP.objects.filter(
                    user=user, otp=otp, created_at__gte=timezone.now() - timedelta(minutes=10)).first()
                if not user.is_verified:
                    return Response({'message': 'User is not verified'}, status=status.HTTP_400_BAD_REQUEST)

                if not otp_record:
                    return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
                otp_record.delete()

                # Generate JWT token
                access_token, refresh_token = generate_tokens_for_user(user)

                return Response({
                    'message': 'OTP verified successfully',
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
            except OTP.DoesNotExist:
                return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
            except AttributeError:
                return Response({'message': 'OTP expired'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def generate_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)
    return access_token, refresh_token


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': 'User view'})
