from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

class LogoutTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="123456", email="testuser@gmx.de")
    
    def test_Logout_Happy(self):
        self.client.cookies['access_token'] = str(RefreshToken.for_user(self.user).access_token)
        url = reverse('logout')
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.cookies['access_token'].value, "")
        self.assertEqual(response.cookies['refresh_token'].value, "")
        self.assertEqual(response.data['detail'],"Erfolgreicher Logout")

    def test_Logout_Unhappy_401(self):
        url = reverse('logout')
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
