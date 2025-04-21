import logging
import requests
from config import ALPHAVANTAGE_API_KEY

logger = logging.getLogger(__name__)

BASE_URL = "https://www.alphavantage.co/query"

def get_stock_price(symbol: str) -> float:
    """Получение цены акции через Alpha Vantage API"""
    try:
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": ALPHAVANTAGE_API_KEY
        }
        
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        
        # Проверка на наличие ошибок и данных
        if "Global Quote" in data and "05. price" in data["Global Quote"]:
            return float(data["Global Quote"]["05. price"])
        else:
            if "Error Message" in data:
                logger.error(f"Alpha Vantage ошибка: {data['Error Message']}")
            else:
                logger.error(f"Неожиданный формат ответа: {data}")
            return 0.0
    except Exception as e:
        logger.error(f"Ошибка получения цены акции {symbol}: {e}")
        return 0.0

def get_forex_price(from_currency: str, to_currency: str) -> float:
    """Получение курса валют через Alpha Vantage API"""
    try:
        params = {
            "function": "CURRENCY_EXCHANGE_RATE",
            "from_currency": from_currency,
            "to_currency": to_currency,
            "apikey": ALPHAVANTAGE_API_KEY
        }
        
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        
        # Проверка на наличие ошибок и данных
        if "Realtime Currency Exchange Rate" in data and "5. Exchange Rate" in data["Realtime Currency Exchange Rate"]:
            return float(data["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
        else:
            if "Error Message" in data:
                logger.error(f"Alpha Vantage ошибка: {data['Error Message']}")
            else:
                logger.error(f"Неожиданный формат ответа: {data}")
            return 0.0
    except Exception as e:
        logger.error(f"Ошибка получения курса {from_currency}/{to_currency}: {e}")
        return 0.0

def get_commodity_price(symbol: str) -> float:
    """Получение цены сырьевых товаров через Alpha Vantage API"""
    try:
        # Для сырьевых товаров используем тот же метод, что и для акций
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": ALPHAVANTAGE_API_KEY
        }
        
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        
        # Проверка на наличие ошибок и данных
        if "Global Quote" in data and "05. price" in data["Global Quote"]:
            return float(data["Global Quote"]["05. price"])
        else:
            if "Error Message" in data:
                logger.error(f"Alpha Vantage ошибка: {data['Error Message']}")
            else:
                logger.error(f"Неожиданный формат ответа: {data}")
            return 0.0
    except Exception as e:
        logger.error(f"Ошибка получения цены товара {symbol}: {e}")
        return 0.0