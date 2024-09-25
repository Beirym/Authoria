from django.urls import path

from .views import *


urlpatterns = [
    path('login/', logIn, name='login'),
    path('signup/', signUp, name='signup'),
]