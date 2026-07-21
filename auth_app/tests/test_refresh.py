from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

class RefreshTokenTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="123456", email="testuser@gmx.de")

    def test_refresh_happy(self):
        self.client.cookies['refresh_token'] = str(RefreshToken.for_user(self.user))
        url = reverse('token_refresh')
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], "Token refreshed")
        self.assertIn('access_token', response.cookies)

    def test_refresh_unhappy_401(self):
        url = reverse('token_refresh')
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], "Refresh Token ungültig oder fehlt.")