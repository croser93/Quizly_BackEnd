from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status


class QuizTest(APITestCase):


    def test_post_quiz(self):
        url = reverse("quizzes")
        data = {"url": "https://www.youtube.com/watch?v=i3a7B65b6w8"}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)