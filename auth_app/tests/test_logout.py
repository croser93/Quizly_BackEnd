from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status

class LogoutTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="123456", email="testuser@gmx.de")

    def test_Logout_Happy(self):
        url = reverse('logout')