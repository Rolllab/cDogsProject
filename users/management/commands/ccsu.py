# ------------------------------------- Command create superuser ----------------------------------------------------
import os
from django.core.management import BaseCommand
from dotenv import load_dotenv

from users.models import User


load_dotenv()

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        admin_user = User.objects.create(
            email=os.getenv('ADMIN_EMAIL'),
            first_name=os.getenv('ADMIN_FIRST_NAME'),
            last_name=os.getenv('ADMIN_LAST_NAME'),
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )

        admin_user.set_password(os.getenv('ADMIN_PASSWORD'))
        admin_user.save()
        print("Создан новый пользователь")