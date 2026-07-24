from rest_framework.views import APIView
from rest_framework.permissions import  IsAuthenticated
from rest_framework.response import Response
from .serializer import QuizSerializer, URLSerializer
from .permission import UserIsCreatorOrAdmin
from ..models import Quiz, Question
from .service import download_audio, start_quiz_chain
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
                audio_path = download_audio(serializer.validated_data['url'])
            except:
                return Response({'error':"Error creating the quiz"}, status=400)

            quiz_json = json.loads(start_quiz_chain(audio_path))
    
            quiz = self.create_Quiz(serializer.validated_data['url'], request, quiz_json)
            quiz_serializer = QuizSerializer(quiz)

            return Response(quiz_serializer.data, status=201)
        else:
            return Response({"error": "Invalid URL or request data."}, status=400)

    def create_Quiz(self, url, request, quiz_json):
        quiz =  Quiz.objects.create(video_url=url, user=request.user, title=quiz_json['title'], description=quiz_json['description'])
        self.create_Question(quiz,quiz_json)
        return quiz

    def create_Question(self, quiz, quiz_json):
        for element in quiz_json['questions']:
            Question.objects.create(quiz= quiz, question_title = element['question_title'], question_options = element['question_options'], answer = element['answer'])

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
                return Response ({"error": "Quiz not found."}, status=404)

    def patch (self, request, pk):
        try:
            quiz = Quiz.objects.get(pk=pk)
            self.check_object_permissions(request, quiz)
            serializer = QuizSerializer(quiz, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            else:
                return Response({"error": "Invalid request data."}, status=400)
        except Quiz.DoesNotExist:
            return Response ({"error": "Quiz not found."}, status=404)

    def delete(self, request, pk):
        try:
            quiz = Quiz.objects.get(pk=pk)
            self.check_object_permissions(request, quiz)
            quiz.delete()
            return Response(status=204)
        except Quiz.DoesNotExist:
            return Response ({"error": "Quiz not found."}, status=404)
