from rest_framework.views import APIView
from rest_framework.permissions import  IsAuthenticated
from rest_framework.response import Response
from .serializer import QuizSerializer, URLSerializer
from ..models import Quiz, Question
from .service import download_audio
from .whisper import transcript
from .gemini import gemini
import json

class QuizzesView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        quiz = Quiz.objects.all()
        serializer = QuizSerializer(quiz, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = URLSerializer(data=request.data)
        if serializer.is_valid():

            # audio_path = download_audio(serializer.validated_data['url'])
            transcr = transcript("media/temp/i3a7B65b6w8.webm")
            quiz_json = gemini(transcr)
            quiz_json = json.loads(quiz_json)

            quiz = Quiz.objects.create(video_url=serializer.validated_data['url'], user=request.user, title=quiz_json['title'], description=quiz_json['description'])

            for element in quiz_json['questions']:
                question = Question.objects.create(quiz= quiz, question_title = element['question_title'], question_options = element['question_options'], answer = element['answer'])
            quiz_serializer = QuizSerializer(quiz)
            print(quiz_serializer.data)
            return Response(quiz_serializer.data, status=201)
        else:
            return Response({"error": "Ungültige URL oder Anfragedaten."}, status=400)
class QuizzesDetailView(APIView):

    permission_classes = [IsAuthenticated]
    def get(self, request, pk):

        try:
            quiz = Quiz.objects.get(pk=pk)
            serializer = QuizSerializer(quiz)
            return Response(serializer.data)
        except:
            return Response ({"error": " Quiz nicht gefunden."}, status=404)