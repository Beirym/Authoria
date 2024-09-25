from django.db import models
from django import utils


class User(models.Model):
    username = models.CharField(max_length=64, unique=True)
    email = models.EmailField()
    email_confirmed = models.BooleanField(default=False)
    password = models.CharField(max_length=128)
    password_salt = models.CharField(max_length=32)
    timezone = models.CharField(max_length=128, default='UTC')
    registered_at = models.DateTimeField(default=utils.timezone.now)

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.username


class Session(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    ip = models.GenericIPAddressField(protocol='IPv4')
    created_at = models.DateTimeField(default=utils.timezone.now)

    class Meta:
        db_table = 'session'