from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import Quiz, Question


class QuizTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="123456", email="testuser@gmx.de")
        self.quiz = Quiz.objects.create(user=self.user, title="testQuest1", description="test description123", video_url="https://www.youtube.com/watch?v=example" )
        self.question = Question.objects.create(quiz=self.quiz, question_title="test titel", question_options=["hallo1", "hallo2",'hallo3', "hallo4"], answer="hallo2")

    # def test_get_quiz(self):
    #     self.client.cookies['access_token'] = str(RefreshToken.for_user(self.user).access_token)
    #     url = reverse("quizzes")
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_quiz(self):
        self.client.cookies['access_token'] = str(RefreshToken.for_user(self.user).access_token)
        url = reverse("quizzes_id", kwargs={'pk': self.quiz.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_post_quiz(self):
    #     self.client.cookies['access_token'] = str(RefreshToken.for_user(self.user).access_token)

    #     url = reverse("quizzes")
    #     data = {"url": "https://www.youtube.com/watch?v=i3a7B65b6w8"}

    #     response = self.client.post(url, data)

    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(response.data['id'], 1)
    #     self.assertTrue(response.data['title'])
    #     self.assertTrue(response.data['description'])
    #     self.assertEqual(response.data['video_url'], data["url"])

    def test_get_quiz_401(self):
        url = reverse("quizzes")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_get_single_quiz_(self):
    #     self.client.cookies['access_token'] = str(RefreshToken.for_user(self.user).access_token)
    #     url = reverse("quizzes_id", kwargs={'pk': 100})
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # def test_post_quiz_400(self):
    #     self.client.cookies['access_token'] = str(RefreshToken.for_user(self.user).access_token)

    #     url = reverse("quizzes")
    #     data = {"url": 1}

    #     response = self.client.post(url, data)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    # def test_post_quiz_401(self):

    #     url = reverse("quizzes")
    #     data = {"url": "https://www.youtube.com/watch?v=i3a7B65b6w8"}

    #     response = self.client.post(url, data)
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)