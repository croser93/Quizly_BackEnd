from rest_framework.views import APIView
from rest_framework.permissions import  IsAuthenticated
from rest_framework.response import Response
from .serializer import QuizSerializer, URLSerializer
from ..models import Quiz
from .service import download_audio

class QuizzesView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
            serializer = URLSerializer(data=request.data)
            if serializer.is_valid():
                audio = download_audio(serializer.validated_data['url'])

                quiz = Quiz.objects.create(video_url=serializer.validated_data['url'], user=request.user, title="TODO", description="TODO")
                quiz_serializer = QuizSerializer(quiz)
                return Response(quiz_serializer.data, status=201)
            else:
                return Response({"error": "Ungültige URL oder Anfragedaten."}, status=400)
class QuizzesDetailView(APIView):
    pass