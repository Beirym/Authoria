from django import utils

from .models import Session
from .ip import getIP

import uuid
import datetime


def createSession(request, user) -> None:
    session = Session.objects.create(
        id=str(uuid.uuid4()),
        user=user, 
        ip=getIP(request)
    )
    saveUserDataInSessions(request, session, user)


def saveUserDataInSessions(request, session, user) -> None:
    request.session['session_id'] = session.id

    request.session['user'] = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'timezone': user.timezone,
        'authorized_at': str(utils.timezone.now()),
    }
    request.session.save()