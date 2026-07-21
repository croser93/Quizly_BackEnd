from rest_framework.views import APIView
from rest_framework.permissions import  AllowAny, IsAuthenticated
from .serializer import RegisstrationSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class RegistrationView(APIView):
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
    permission_classes = [IsAuthenticated]
    pass
    