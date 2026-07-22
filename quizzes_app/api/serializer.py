from rest_framework import serializers
from quizzes_app.models import Quiz


class URLSerializer (serializers.Serializer):
    url = serializers.URLField()
class QuizSerializer(serializers.ModelSerializer):
        
        class Meta:
            model = Quiz
            fields = ['id','title','description','created_at','updated_at','video_url']

