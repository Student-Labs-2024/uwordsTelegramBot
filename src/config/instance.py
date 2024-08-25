import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent.parent.parent
UPLOAD_DIR: Path = BASE_DIR / "audio_transfer"

# Bot
BOT_TOKEN = os.environ.get("BOT_TOKEN")
APP_TOKEN = os.environ.get("APP_TOKEN")

# MainApp
APP_URL = os.environ.get("APP_URL")

# PostgreSQL
POSTGRES_DB: str = os.environ.get("POSTGRES_DB")
POSTGRES_HOST: str = os.environ.get("POSTGRES_HOST")
POSTGRES_PORT: str = os.environ.get("POSTGRES_PORT")
POSTGRES_USER: str = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD: str = os.environ.get("POSTGRES_PASSWORD")
