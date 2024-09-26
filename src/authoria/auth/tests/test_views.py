from django.test import TestCase
from django.urls import reverse
from django.core.cache import cache

from ..views import logIn, signUp
from ..models import User, Session
from ..protection import checkAuthBan, checkAuthAttempts

import json


redis_client = cache.client.get_client()


class AuthTestCase(TestCase):
    username = 'nikita'
    email = 'nikita@silaev.tech'
    password = 'super_secret'
    timezone = 'Europe/Volgograd'

    def setUp(self):
        redis_client.flushdb()

    def test_signup_and_login(self):
        # Sign Up
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

        signup_data = {
            'auth_data': json.dumps({
                'username': self.username,
                'email': self.email,
                'password': self.password,
                'password_confirm': self.password,
                'timezone': self.timezone,
            })
        }

        response = self.client.post(reverse('signup'), signup_data)
        self.assertEqual(response.status_code, 204)

        user = User.objects.filter(username=self.username).first()
        self.assertIsNotNone(user)

        # Delete the session that was created after registration
        session = self.client.session
        session.clear()
        session.save()

        # Log In
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

        login_data = {
            'auth_data': json.dumps({
                'username_or_email': self.username,
                'password': self.password,
                'timezone': self.timezone
            })
        }

        response = self.client.post(reverse('login'), login_data)
        self.assertEqual(response.status_code, 204)

        session_exists = Session.objects.filter(user=user).exists()
        self.assertTrue(session_exists)


class AuthBanTestCase(TestCase):
    ip = '127.0.0.1'

    def setUp(self):
        redis_client.flushdb()

    def test_auth_ban(self):
        login_data = {
            'auth_data': json.dumps({
                'username_or_email': 'some_username',
                'password': 'some_password',
                'timezone': 'some_timezone',
            })
        }

        def sendPostRequestWithIncorrectData():
            response = self.client.post(reverse('login'), login_data)
            self.assertEqual(response.status_code, 401)

        for i in range(1, 11):
            '''Makes 10 auth attemps with incorrect data to get ban'''
            sendPostRequestWithIncorrectData()
            attempts_count = int(redis_client.get(f'auth_attempts:{self.ip}'))
            self.assertEqual(i, attempts_count)

        auth_banned = redis_client.get(f'auth_banned:{self.ip}')
        self.assertTrue(auth_banned)