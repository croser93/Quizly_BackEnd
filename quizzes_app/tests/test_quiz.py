from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class QuizTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="123456", email="testuser@gmx.de")

    def test_post_quiz(self):
        self.client.cookies['access_token'] = str(RefreshToken.for_user(self.user).access_token)

        url = reverse("quizzes")
        data = {"url": "https://www.youtube.com/watch?v=i3a7B65b6w8"}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], 1)
        self.assertEqual(response.data['title'], "TODO")
        self.assertEqual(response.data['description'], "TODO")
        self.assertEqual(response.data['video_url'], data["url"])

    def test_post_quiz_400(self):
        self.client.cookies['access_token'] = str(RefreshToken.for_user(self.user).access_token)

        url = reverse("quizzes")
        data = {"url": 1}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_post_quiz_401(self):

        url = reverse("quizzes")
        data = {"url": "https://www.youtube.com/watch?v=i3a7B65b6w8"}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)