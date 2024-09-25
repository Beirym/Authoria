from django.template.response import TemplateResponse
from django.http import HttpResponse, JsonResponse

from authoria.redis_config import setRedisValue, getRedisValue, getRedisKeyTTL
from .ip import getIP


def checkAuthBan(func):
    '''Checks for the presence of the user's IP address in the ban list.'''

    def wrapper(request):
        ip = getIP(request)
        key = f'auth_banned:{ip}'
        auth_banned = getRedisValue(key)
        if auth_banned:
            auth_ban_seconds: int = getRedisKeyTTL(key)
            return TemplateResponse(
                request, 
                'auth/ban.html', 
                context={'auth_ban_mins': auth_ban_seconds // 60}
            )
        return func(request)
    return wrapper


def checkAuthAttempts(request):
    '''Counts the user's authorization attempts and temporarily 
       bans his IP address when 10 unsuccessful attempts are reached.'''

    ip = getIP(request)
    key = f'auth_attempts:{ip}'
    auth_attempts = getRedisValue(key)
    if auth_attempts:
        auth_attempts = int(auth_attempts)
        auth_attempts += 1
    else:
        auth_attempts = 1
        
    setRedisValue(key, auth_attempts, expire=60*5)

    if auth_attempts >= 10:
        setRedisValue(f'auth_banned:{ip}', value='true', expire=60*10)
        return checkAuthBan(request)
