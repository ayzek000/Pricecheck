import logging
from config import binance_client
from binance.client import Client

logger = logging.getLogger(__name__)

def get_crypto_price(symbol: str) -> float:
    """Получение цены криптовалюты через Binance API"""
    try:
        if not binance_client:
            logger.error("Binance client не инициализирован")
            return 0.0
            
        ticker = binance_client.get_symbol_ticker(symbol=symbol)
        return float(ticker["price"])
    except Exception as e:
        logger.error(f"Ошибка получения цены Binance для {symbol}: {e}")
        return 0.0

def get_historical_klines(symbol: str, interval: str, start_str: str):
    """Получение исторических данных для графика"""
    try:
        if not binance_client:
            logger.error("Binance client не инициализирован")
            return []
            
        return binance_client.get_historical_klines(
            symbol, 
            interval, 
            start_str
        )
    except Exception as e:
        logger.error(f"Ошибка получения исторических данных для {symbol}: {e}")
        return []