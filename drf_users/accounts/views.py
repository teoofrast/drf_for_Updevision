import requests

from rest_framework import generics, permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken
from .models import CustomUser
from .serializers import UserSerializer, LoginSerializer

class SignupView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        return Response({
            'ID type': user.id_type,
            'Bearer': str(access),
        }, status=status.HTTP_201_CREATED)

class SigninView(GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    @staticmethod
    def post(request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            id_ = serializer.validated_data['id']
            password = serializer.validated_data['password']

            user = authenticate(request, id=id_, password=password)

            if user:
                login(request, user)
                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class InfoView(GenericAPIView):
    serializer_class = UserSerializer

    @staticmethod
    def post(request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = authenticate(
                request,
                id=serializer.validated_data['id'],
                password=serializer.validated_data['password'],
            )
            if user:
                refresh = RefreshToken.for_user(user)
                access = refresh.access_token
                return Response({'message': 'Login successful',}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid id or password'}, status=status.HTTP_401_UNAUTHORIZED)

class LatencyView(GenericAPIView):

    @staticmethod
    def get(request):
        user = CustomUser.objects.get(id=request.data['id'])
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        try:
            response = requests.get('https://ya.ru', timeout=5)
            response.raise_for_status()

            latency = response.elapsed.total_seconds() * 1000
            return Response({'latency': latency}, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LogoutView(GenericAPIView):
    serializer_class = UserSerializer

    @staticmethod
    def post(request):
        if request.data['all'] == 'true':
            tokens = OutstandingToken.objects.filter(user_id=request.data['id'])
            for token in tokens:
                t, _ = BlacklistedToken.objects.get_or_create(token=token)
            return Response({'message': 'Logout successful'}, status=status.HTTP_205_RESET_CONTENT)

        elif request.data['all'] == 'false':
            tokens = OutstandingToken.objects.filter(user_id=request.data['id'])
            BlacklistedToken.objects.get_or_create(token=tokens[0])
            return Response({'message': 'Logout successful'}, status=status.HTTP_205_RESET_CONTENT)

        else:
            return Response({'message': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)