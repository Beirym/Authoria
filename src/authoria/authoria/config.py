import os
from dotenv import load_dotenv


load_dotenv()


DJANGO_SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

TELEGRAM_LOGS_BOT_TOKEN = os.environ.get("TELEGRAM_LOGS_BOT_TOKEN")
TELEGRAM_LOGS_BOT_USERS: list = os.environ.get("TELEGRAM_LOGS_BOT_USERS").split(',')