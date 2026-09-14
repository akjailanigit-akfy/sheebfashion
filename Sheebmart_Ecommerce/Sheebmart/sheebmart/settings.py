import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-sheebmart-dev-key")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "sheebfashion-production.up.railway.app",
]

CSRF_TRUSTED_ORIGINS = [
    "https://sheebfashion-production.up.railway.app",
]