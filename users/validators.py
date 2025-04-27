import re

from django.conf import settings
from django.core.exceptions import ValidationError


def validate_password(field):
    pattern = re.compile(r'^[A-Za-z0-9]+$')
    language = settings.LANGUAGE_CODE
    error_message = [
        {
            'ru-ru': 'Пароль должен содержать только символы латинского алфавита и цифры!',
            'en-us': 'Must contain A-Z a-Z letters and 0-9 digits'
        },
        {
            'ru-ru': 'Длина пароля должна быть между 8 и 16 символами!',
            'en-us': 'Password length must be between 8 and 16 charters!'
        }
    ]
    if not bool(re.match(pattern, field)):
        print(error_message[0][language])
        raise ValidationError(error_message[0][language], code=error_message[0][language])
    if not 8 <= len(field) <= 16:
        print(error_message[1][language])
        raise ValidationError(error_message[1][language], code=error_message[1][language])
