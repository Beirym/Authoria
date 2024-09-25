from django.db.models import Q

from .models import User
from .encoding import checkPassword


class Validator:
    @staticmethod
    def logIn(username_or_email: str, password: str) -> list:
        errors = []

        # Check "username or email"
        try:
            user = User.objects.only('password', 'password_salt').get(
                Q(username=username_or_email) | Q(email=username_or_email)
            )

            if checkPassword(password, user.password, user.password_salt) is False:
                errors.append({
                    'field': 'password',
                    'text': 'Неверный пароль',
                })

        except User.DoesNotExist:
            errors.append({
                'field': 'username_or_email', 
                'text': 'Такого пользователя не существует'
            })

        except User.MultipleObjectsReturned:
            errors.append({
                'field': 'username_or_email', 
                'text': 'Для входа используйте имя пользователя'
            })

        return errors

    @staticmethod
    def signUp(username: str, email: str) -> list:
        errors = []

        # Check username
        if len(User.objects.filter(username=username)) > 0:
            errors.append({
                'field': 'username', 
                'text': 'Данное имя пользователя занято'
            })

        # Check email
        if len(User.objects.filter(Q(email=email) & Q(email_confirmed=True))) > 0:
            errors.append({
                'field': 'email', 
                'text': 'Данный e-mail адрес занят'
            })

        return errors