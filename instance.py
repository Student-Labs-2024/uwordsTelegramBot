import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ.get('BOT_TOKEN')
SECRET = os.environ.get('SECRET')
NODE = os.environ.get('NODE')

POSTGRES_DB: str = os.environ.get("POSTGRES_DB")
POSTGRES_HOST: str = os.environ.get("POSTGRES_HOST")
POSTGRES_PORT: str = os.environ.get("POSTGRES_PORT")
POSTGRES_USER: str = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD: str = os.environ.get("POSTGRES_PASSWORD")
