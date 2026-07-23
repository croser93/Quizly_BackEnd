from rest_framework.views import APIView
from rest_framework.permissions import  AllowAny, IsAuthenticated
from .serializer import RegisstrationSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (TokenRefreshView)

class RegistrationView(APIView):
    """
    Register a new user account.

    Endpoints:
    - POST   /api/registration/ - Create a new user account
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisstrationSerializer(data=request.data)

        data = {}
        if serializer.is_valid():
            save_account = serializer.save()
            data = {
                'username' : save_account.username,
                'email' : save_account.email,
                'user_id' : save_account.pk
            }
        else:
            return Response(serializer.errors, status=400) 
        return Response({"detail": "User created successfully!"}, status=201)
    
class LoginView(APIView):
    """
    Authenticate a user and set JWT auth cookies.

    Endpoints:
    - POST   /api/login/ - Log in and receive access/refresh token cookies
    """

    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        if serializer.is_valid():
                
            user = serializer.validated_data['user']
            token = RefreshToken.for_user(user)
            refresh_token = str(token)
            access_token = str(token.access_token)

            response = Response({'detail': 'Login successfully!', 'user': {'id':user.id, 'username': user.username, 'email': user.email}} ,status=200)
            response.set_cookie('refresh_token', refresh_token, httponly=True)
            response.set_cookie('access_token', access_token, httponly=True)
            return response
        else:
            return Response(serializer.errors, status=401)
        
class LogoutView(APIView):
    """
    Log out the authenticated user and invalidate their tokens.

    Endpoints:
    - POST   /api/logout/ - Blacklist the refresh token and clear auth cookies
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
    
        refresh = request.COOKIES.get('refresh_token')

        token = RefreshToken(refresh)
        token.blacklist()
        response = Response({"detail": "Log-Out successfully! All Tokens will be deleted. Refresh token is now invalid."}, status=status.HTTP_200_OK)
        response.delete_cookie("access_token")
        response.delete_cookie('refresh_token')

        return response

class RefreshCookieView(TokenRefreshView):
    """
    Refresh the access token using the refresh token stored in cookies.

    Endpoints:
    - POST   /api/token/refresh/ - Issue a new access token cookie
    """

    def post(self, request):

        refresh = request.COOKIES.get('refresh_token')

        if refresh is None:
            return Response({'detail':'Refresh Token ungültig oder fehlt.'}, status=status.HTTP_401_UNAUTHORIZED)
        request.data['refresh'] = refresh
        accsess = super().post(request)
        accsess_token = accsess.data['access']

        response = Response({'detail': 'Token refreshed'})
        response.set_cookie('access_token', accsess_token, httponly=True)
        return response