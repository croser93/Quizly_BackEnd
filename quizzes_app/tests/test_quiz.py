from rest_framework.test import APITestCase
from django.urls import reverse


class QuizTest(APITestCase):

    def test_post_quiz(self):
        url = reverse("quizzes")
        data = {"url": "https://www.youtube.com/watch?v=i3a7B65b6w8"}

        self.client.post(url, data)