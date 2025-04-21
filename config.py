import os
from dotenv import load_dotenv
from binance.client import Client

# Загрузка настроек
load_dotenv()

# Конфигурация
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
BINANCE_SECRET_KEY = os.getenv('BINANCE_SECRET_KEY')
ALPHAVANTAGE_API_KEY = os.getenv('ALPHAVANTAGE_API_KEY')

# Инициализация клиентов API
binance_client = Client(BINANCE_API_KEY, BINANCE_SECRET_KEY) if BINANCE_API_KEY and BINANCE_SECRET_KEY else None

# Проверка конфигурации
if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN не найден в .env файле")

if not ALPHAVANTAGE_API_KEY:
    raise ValueError("ALPHAVANTAGE_API_KEY не найден в .env файле")