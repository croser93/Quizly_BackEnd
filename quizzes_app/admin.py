from django.contrib import admin
from .models import Quiz, Question


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'video_url', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('title', 'description', 'video_url')
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_title', 'quiz', 'answer')
    list_filter = ('quiz',)
    search_fields = ('question_title',)
