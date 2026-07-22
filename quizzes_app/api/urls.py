from django.urls import path
from .views import QuizzesView, QuizzesDetailView


urlpatterns = [
    path('quizzes/', QuizzesView.as_view(), name='quizzes'),
    path('quizzes/<int:pk>/', QuizzesDetailView.as_view(), name='quizzes_id'),

]





