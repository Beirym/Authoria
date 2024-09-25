from django.test import TestCase

from ..models import User, Session
from ..encoding import hashPassword

import uuid


class AuthTestCase(TestCase):
    # User data
    username = "artemka"
    email = "artemka@gmail.com"
    email_confirmed = True
    password, salt = hashPassword('super_secret_pass')
    timezone = 'Europe/Volgograd'

    # Session data
    session_id = int(uuid.uuid4())
    ip = '127.0.0.1'
    
    def setUp(self):
        self.user = User.objects.create(
            username=self.username,
            email=self.email,
            email_confirmed=self.email_confirmed,
            password=self.password,
            password_salt=self.salt,
            timezone=self.timezone,
        )

        self.session = Session.objects.create(
            id=self.session_id,
            user=self.user,
            ip=self.ip,
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, self.username)
        self.assertEqual(self.user.email, self.email)
        self.assertEqual(self.user.email_confirmed, self.email_confirmed)
        self.assertEqual(self.user.password, self.password)
        self.assertEqual(self.user.password_salt, self.salt)
        self.assertEqual(self.user.timezone, self.timezone)

    def test_session_creation(self):
        self.assertEqual(self.session.id, self.session_id)
        self.assertEqual(self.session.user, self.user)
        self.assertEqual(self.session.ip, self.ip)