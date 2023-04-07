from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User

class UserTests(APITestCase):
    def test_create_user(self):
        """
        Ensure we can create a new user object.
        """
        url = reverse('register')
        data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'phone': '+15555555555',
            'password': 'testpassword',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().name, 'Test User')
        self.assertEqual(User.objects.get().email, 'test@example.com')
        self.assertEqual(User.objects.get().phone, '+15555555555')
        self.assertEqual(User.objects.get().isSubscribed, True)

class LoginTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            name='Test User',
            email='test@example.com',
            phone='+15555555555',
            password='testpassword',
        )

    def test_login_user(self):
        """
        Ensure we can login a user.
        """
        url = reverse('login')
        data = {
            'email': 'test@example.com',
            'password': 'testpassword',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('jwt' in response.data)


class ToggleSubscriptionTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            name='Test User',
            email='test@example.com',
            phone='+15555555555',
            password='testpassword',
        )

    def test_toggle_subscription(self):
        """
        Ensure we can toggle a user's subscription.
        """
        url = reverse('toggle-subscription', args=[self.user.id])
    
        response = self.client.put(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('message' in response.data)