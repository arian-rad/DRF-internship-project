from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework import serializers
from .models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .utils import Util
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=65, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate(self, attrs):
        if not attrs.get('username').isalnum():
            raise serializers.ValidationError('The username should only contain alphanumeric characters')
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=68, min_length=3, read_only=True)
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=8, write_only=True)
    tokens = serializers.CharField(max_length=255, min_length=3, read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = auth.authenticate(email=email, password=password)

        if not user:  # User not found
            raise AuthenticationFailed('Invalid username or password')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')
        return {'username': user.username, 'email': email, 'tokens': user.tokens()}


class LogOutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': 'Token is invalid'
    }

    def validate(self, attrs):
        self.token = attrs.get('refresh')
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')



class RequestPasswordRestEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=3)

    class Meta:
        fields = ['email']

    def validate(self, attrs):

        email = attrs['data'].get('email')
        # if User.objects.filter(email=email).exists():
        #     user = User.objects.filter(email=email)
        #     user_id_b64 = urlsafe_base64_encode(user.id)
        #     token = PasswordResetTokenGenerator().make_token(user)
        #     current_site = get_current_site(request=attrs['data'].get('request'))
        #     relative_link = reverse('authentication:password_reset_confirm', kwargs={'user_id_b64': user_id_b64, 'token': token})
        #     absolute_url = 'http://' + current_site.domain + relative_link
        #     email_body = f'Hi  User the link bellow to reset your password\n {absolute_url}'
        #     data = {'subject': 'Rest your password', 'body': email_body, 'to': user.email}
        #     Util.send_email(data)
        return super().validate(attrs)


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8, max_length=65, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    user_id_b64 = serializers.CharField(write_only=True)

    class Meta:
        fields = ['password', 'token', 'user_id_b64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            user_id_b64 = attrs.get('user_id_b64')
            user_id = force_str(urlsafe_base64_decode(user_id_b64))
            user = User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset password link is invalid', 401)
            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            raise e

