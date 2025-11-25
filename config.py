import os
from env_loader import setup_environment
from dataclasses import dataclass

# Инициализация переменных окружения
setup_environment()


@dataclass
class Settings:
    # API Settings
    API_AUTH_URL: str = "https://rubrain.com/api/auth/login/?active_lang=ru"
    # API_TOKEN: str = os.getenv('API_TOKEN')

    # Google Sheets
    # SPREADSHEET_ID: str = os.getenv('SPREADSHEET_ID')
    # CREDENTIALS_FILE: str = os.getenv('GOOGLE_CREDENTIALS_FILE', 'credentials.json')

    # Telegram
    TELEGRAM_BOT_TOKEN: str = os.getenv('TG_TOKEN')
    TELEGRAM_CHAT_ID: str = os.getenv('CHAT_ID_1')

    # Application
    CHECK_INTERVAL_HOURS: int = int(os.getenv('CHECK_INTERVAL_HOURS', '12'))
    MAX_RETRIES: int = int(os.getenv('MAX_RETRIES', '3'))
    RETRY_DELAY: int = int(os.getenv('RETRY_DELAY', '60'))

    # Logging
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')

