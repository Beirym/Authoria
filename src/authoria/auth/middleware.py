from django.shortcuts import redirect
from django.urls import reverse

from auth.models import User


class AuthMiddleware:
    def __init__(self, next):
        self.next = next

    def __call__(self, request):
        path_root = request.path.split('/')[1]
        if (path_root == 'auth') and ('user' in request.session):
            ...

        response = self.next(request)
        return response
    