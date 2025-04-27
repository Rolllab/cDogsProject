# ------------------------------------- Command create database ----------------------------------------------------
import psycopg2
from django.core.management import BaseCommand

from config.settings import USER, PASSWORD, HOST, PORT


class Command(BaseCommand):
    """Устанавливает соединение и создает новую базу данных."""

    help = 'Создает новую базу данных в PostgreSQL.'

    def add_arguments(self, parser):
        # help — это описание аргумента, которое отображается при использовании python manage.py ccdb --help
        parser.add_argument('db_name', type=str, help='Имя новой базы данных')

    def handle(self, *args, **kwargs):
        db_name = kwargs['db_name']  # Получаем имя базы данных из аргументов

        # Проверка имени базы данных:
        if not db_name.replace("_", "").isalnum():
            print("Ошибка: Недопустимое имя базы данных. Используйте только буквы, цифры и подчеркивания.")
            return

        query = f'CREATE DATABASE {db_name};'

        conn = None
        try:
            # Подключаемся к существующей базе данных (например, postgres)
            conn = psycopg2.connect(
                host=HOST,
                database="postgres",  # Подключаемся к системной базе данных
                user=USER,
                password=PASSWORD,
                port=PORT
            )
            conn.autocommit = True  # Включаем autocommit для выполнения DDL-запросов
            with conn.cursor() as cursor:
                cursor.execute(query)
                print(f"База данных {db_name} успешно создана.")

        except Exception as e:
            print(f"Ошибка при подключении к базе данных: {e}")
            if conn:
                conn.rollback()
