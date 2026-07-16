from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User

class LoginTest(APITestCase):

    def setUp(self):
        User.objects.create_user(username='testUser', password='test123', email='test@gmx.de')

    def test_Login_Happy(self):
        url = reverse('login')
        data = {
            'username':'testUser',
            'password':'test123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'Login successfully!')
        self.assertEqual(response.data['user']['id'], 1)
        self.assertEqual(response.data['user']['username'], 'testUser')
        self.assertEqual(response.data['user']['email'], 'test@gmx.de')
        self.assertIn('refresh_token', response.cookies)
        self.assertIn('access_token', response.cookies)

    def test_Login_Wrong_PW(self):
        url = reverse('login')
        data = {
            'username':'testUser',
            'password':'test99999'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)