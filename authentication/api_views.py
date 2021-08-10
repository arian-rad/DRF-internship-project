from rest_framework.generics import GenericAPIView, RetrieveDestroyAPIView, ListAPIView
from rest_framework.views import APIView
from .serializers import RegisterSerializer, EmailVerificationSerializer, LoginSerializer, UserSerializer, \
    RequestPasswordRestEmailSerializer, SetNewPasswordSerializer, LogOutSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utils import Util
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .renderes import UserRenderer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework import permissions


class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(email=serializer.data['email'])
            token = RefreshToken.for_user(user).access_token
            current_site = get_current_site(request)
            relative_link = reverse('authentication:email_verify')
            absolute_url = 'http://' + current_site.domain + relative_link + "?token=" + str(token)
            email_body = f'Hi {user.username} User the link bellow to verify your email\n {absolute_url}'
            data = {'subject': 'Verify your email', 'body': email_body, 'to': user.email}
            Util.send_email(data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailAPIView(APIView):
    serializer_class = EmailVerificationSerializer
    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description='Description',
                                           type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutAPIView(GenericAPIView):
    serializer_class = LogOutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserRetrieveDestroyAPIView(RetrieveDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RequestPasswordRestEmailAPIView(GenericAPIView):
    serializer_class = RequestPasswordRestEmailSerializer

    def post(self, request):
        # data = {'request': request, 'data': request.data}  # we need to access to request in
        # # RequestPasswordRestEmailSerializer.
        # # Since there is not self.request in RequestPasswordRestEmailSerializer, we sent data as a dictionary
        # # containing request
        # serializer = self.serializer_class(data=data)
        # serializer.is_valid(raise_exception=True)
        # return Response({'success': 'we have sent you an email to reset your password'}, status=status.HTTP_200_OK)

        serializer = self.serializer_class(data=request.data)
        email = request.data['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            user_id_b64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request)
            relative_link = reverse('authentication:password_reset_confirm',
                                    kwargs={'user_id_b64': user_id_b64, 'token': token})
            absolute_url = 'http://' + current_site.domain + relative_link
            email_body = f'Hi  User the link bellow to reset your password\n {absolute_url}'
            data = {'subject': 'Rest your password', 'body': email_body, 'to': user.email}
            Util.send_email(data)
        return Response({'success': 'we have sent you an email to reset your password'}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPIView(GenericAPIView):
    def get(self, request, user_id_b64, token):
        try:
            user_id = smart_str((urlsafe_base64_decode(user_id_b64)))
            user = User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):  # returns False if the user has already
                # used the token
                return Response({'error': 'Token is valid. please request a new one'},
                                status=status.HTTP_401_UNAUTHORIZED)

            return Response(
                {'success': True, 'message': 'Credentials Valid', 'user_id_b64': user_id_b64, 'token': token},
                status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError:
            return Response({'error': 'Token is valid. please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)


class SetNewPasswordAPIView(GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password is rest Successfully'}, status=status.HTTP_200_OK)
