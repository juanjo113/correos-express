import os
from dotenv import load_dotenv

# Cargar variables de entorno desde un archivo .env
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-change-me')

    # Base de datos: usa DATABASE_URL (Render/Heroku style) o SQLite local
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///vehiculos.db')
    if DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Correo SMTP (Gmail u otro)
    SMTP_HOST = os.getenv('SMTP_HOST', '')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    SMTP_USER = os.getenv('SMTP_USER', '')
    SMTP_PASS = os.getenv('SMTP_PASS', '')
    SMTP_USE_TLS = os.getenv('SMTP_USE_TLS', 'true').lower() == 'true'
    FROM_EMAIL = os.getenv('FROM_EMAIL', os.getenv('SMTP_USER', ''))

    # Ventana de aviso (días antes)
    ALERT_DAYS = int(os.getenv('ALERT_DAYS', '14'))
