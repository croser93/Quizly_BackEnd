from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User

class RegistrationTest(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testUser1', password='test123', email='test1@gmx.de' )
    
    def test_SignIn_Happy(self):
        url = reverse('registration')
        data = {
            'username': 'testUser',
            'password': 'test123',
            'confirmed_password': 'test123',
            'email': 'test@gmx.de'
        }
        response = self.client.post(url,data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testUser').exists())
        self.assertTrue(User.objects.get(username='testUser').check_password('test123'))


    def test_SignIn_Unhappy_Email_Exist(self):
        url = reverse('registration')
        data = {
            'username': 'testUser',
            'password': 'test123',
            'confirmed_password': 'test123',
            'email': 'test1@gmx.de'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.data ['error'], 'email exist' )

    def test_SignIn_Unhappy_Email_Required(self):
        url = reverse('registration')
        data = {
            'username': 'testUser',
            'password': 'test123',
            'confirmed_password': 'test123',
        }
        response = self.client.post(url, data)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_SignIn_Unhappy_Pw_Not_Match(self):
        url = reverse('registration')
        data = {
            'username': 'testUser',
            'password': 'test123',
            'confirmed_password': 'test1235',
            'email': 'test@gmx.de'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.data ['error'], 'password dont match' )