from rest_framework import serializers
from quizzes_app.models import Quiz, Question


class URLSerializer (serializers.Serializer):
    url = serializers.URLField()
class QuestionSerializer(serializers.ModelSerializer):
     
    class Meta:
        model = Question
        fields = ['id','question_title','question_options','answer','created_at', 'updated_at']

        
class QuizSerializer(serializers.ModelSerializer):

        questions = QuestionSerializer(many=True, read_only=True)
        class Meta:
            model = Quiz
            fields = ['id','title','description','created_at','updated_at','video_url','questions']


