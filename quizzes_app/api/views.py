from rest_framework.views import APIView
from rest_framework.permissions import  IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .serializer import QuizSerializer

class QuizzesView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:
            serializer = QuizSerializer(data=request.data)
            if serializer.is_valid():
                return Response(serializer.data, status=201)
            else:
                return Response({"error": "Ungültige URL oder Anfragedaten."}, status=400)
        except:
            pass
class QuizzesDetailView(APIView):
    pass