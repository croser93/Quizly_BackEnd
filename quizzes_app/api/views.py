from rest_framework.views import APIView
from rest_framework.permissions import  IsAuthenticated
from rest_framework.response import Response
from .serializer import QuizSerializer, URLSerializer
from .permission import UserIsCreatorOrAdmin
from ..models import Quiz, Question
from .service import download_audio, start_quiz_chain
from .whisper import transcript
from .gemini import gemini
import json

class QuizzesView(APIView):
    """
    Create and list quizzes for the authenticated user.

    Endpoints:
    - GET    /api/quizzes/ - List all quizzes belonging to the authenticated user
    - POST   /api/quizzes/ - Create a new quiz from a YouTube URL
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):

        quiz = Quiz.objects.filter(user=request.user)
        serializer = QuizSerializer(quiz, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = URLSerializer(data=request.data)
        if serializer.is_valid():

            try:
                try:
                    audio_path = download_audio(serializer.validated_data['url'])
                except Exception:
                    raise Exception("Error creating the quiz")

                quiz_json = json.loads(start_quiz_chain(audio_path))
            except Exception as e:
                return Response({"error": str(e)}, status=400)
            
            quiz = Quiz.objects.create(video_url=serializer.validated_data['url'], user=request.user, title=quiz_json['title'], description=quiz_json['description'])
            for element in quiz_json['questions']:
                Question.objects.create(quiz= quiz, question_title = element['question_title'], question_options = element['question_options'], answer = element['answer'])
            quiz_serializer = QuizSerializer(quiz)
            print(quiz_serializer.data)
            return Response(quiz_serializer.data, status=201)
        else:
            return Response({"error": "Ungültige URL oder Anfragedaten."}, status=400)
        
class QuizzesDetailView(APIView):
    """
    Retrieve, update or delete a single quiz owned by the authenticated user.

    Endpoints:
    - GET    /api/quizzes/{ID}/ - Retrieve a single quiz
    - PATCH  /api/quizzes/{ID}/ - Partially update a quiz
    - DELETE /api/quizzes/{ID}/ - Delete a quiz
    """

    permission_classes = [IsAuthenticated, UserIsCreatorOrAdmin]

    def get(self, request, pk):
            try:
                quiz = Quiz.objects.get(pk=pk)
                self.check_object_permissions(request, quiz)
                serializer = QuizSerializer(quiz)
                return Response(serializer.data, status=200)
            except Quiz.DoesNotExist:
                return Response ({"error": "Quiz nicht gefunden."}, status=404)

    def patch (self, request, pk):
        try:
            quiz = Quiz.objects.get(pk=pk)
            self.check_object_permissions(request, quiz)
            serializer = QuizSerializer(quiz, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            else:
                return Response({"error": "Ungültige Anfragedaten."}, status=400)
        except Quiz.DoesNotExist:
            return Response ({"error": "Quiz nicht gefunden."}, status=404)

    def delete(self, request, pk):
        try:
            quiz = Quiz.objects.get(pk=pk)
            self.check_object_permissions(request, quiz)
            quiz.delete()
            return Response(status=204)
        except Quiz.DoesNotExist:
            return Response ({"error": "Quiz nicht gefunden."}, status=404)
