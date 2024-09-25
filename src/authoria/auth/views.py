from django.template.response import TemplateResponse
from django.http import HttpResponse, JsonResponse
from django.db.models import Q

from .protection import checkAuthBan, checkAuthAttempts
from .models import User
from .validation import Validator
from .sessions import createSession
from .encoding import hashPassword

import json
from django import utils

@checkAuthBan
def logIn(request):
    if request.method == 'GET':
        return TemplateResponse(request, 'auth/login.html')
    elif request.method == 'POST':
        auth_data = json.loads(request.POST.get('auth_data'))
        username_or_email, password, timezone = auth_data.values()

        validation_errors = Validator.logIn(username_or_email, password)
        if validation_errors:
            checkAuthAttempts(request)
            return JsonResponse({'errors': validation_errors}, status=401)

        user = User.objects.get(Q(username=username_or_email) | Q(email=username_or_email))
        if timezone != user.timezone:
            user.timezone = timezone
            user.save()
        createSession(request, user)

        return HttpResponse(status=204)

@checkAuthBan
def signUp(request):
    if request.method == 'GET':
        return TemplateResponse(request, 'auth/signup.html')
    elif request.method == 'POST':
        auth_data = json.loads(request.POST.get('auth_data'))
        username, email, password, password_confirm, timezone = auth_data.values()
        password, password_salt = hashPassword(password)

        validation_errors = Validator.signUp(username, email)
        if validation_errors:
            checkAuthAttempts(request)
            return JsonResponse({'errors': validation_errors}, status=401)

        user = User.objects.create(
            username=username,
            email=email,
            password=password,
            password_salt=password_salt,
            timezone=timezone,
        )
        createSession(request, user)

        return HttpResponse(status=204)