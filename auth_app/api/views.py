from rest_framework.views import APIView
from rest_framework.permissions import  AllowAny
from .serializer import RegisstrationSerializer
from rest_framework.response import Response
from rest_framework import status

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