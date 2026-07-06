from rest_framework.views import APIView
from .serializer import RegisstrationSerializer
from rest_framework.response import Response
from rest_framework import status

class RegistrationView(APIView):
    
    def post(self, request):
        serializer = RegisstrationSerializer

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
        return Response(data)