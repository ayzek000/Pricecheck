import os
import logging
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import pandas as pd
from api.binance_api import get_historical_klines
from models import get_asset_name

logger = logging.getLogger(__name__)

async def create_chart(symbol: str, interval: str = '1d', days: int = 30) -> dict:
    """
    Создает график для указанного символа
    
    Args:
        symbol: Символ криптовалюты
        interval: Интервал данных ('1h', '4h', '1d')
        days: Количество дней для отображения
        
    Returns:
        dict: Результат операции {'success': bool, 'filename': str, 'error': str}
    """
    try:
        # Определяем период для запроса
        start_str = f"{days} days ago UTC"
        
        # Получаем исторические данные
        klines = get_historical_klines(symbol, interval, start_str)
        
        if not klines:
            return {
                'success': False,
                'filename': '',
                'error': 'Не удалось получить исторические данные'
            }
        
        # Преобразуем данные в DataFrame
        df = pd.DataFrame(klines, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'number_of_trades',
            'taker_buy_base', 'taker_buy_quote', 'ignore'
        ])
        
        # Конвертируем timestamp в datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        
        # Преобразуем строковые значения в числовые
        df['close'] = df['close'].astype(float)
        
        # Создаем график
        plt.figure(figsize=(10, 6))
        plt.plot(df['timestamp'], df['close'], color='blue')
        
        # Настраиваем форматирование дат
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=max(1, days // 10)))
        plt.gcf().autofmt_xdate()
        
        # Добавляем заголовок и метки осей
        asset_name = get_asset_name(symbol)
        plt.title(f'{asset_name} ({symbol}) - Последние {days} дней')
        plt.xlabel('Дата')
        plt.ylabel('Цена (USDT)')
        plt.grid(True, alpha=0.3)
        
        # Создаем директорию для графиков, если она не существует
        os.makedirs('charts', exist_ok=True)
        
        # Сохраняем график
        filename = f'charts/{symbol.lower()}_{datetime.now().strftime("%Y%m%d%H%M%S")}.png'
        plt.savefig(filename)
        plt.close()
        
        return {
            'success': True,
            'filename': filename,
            'error': ''
        }
    
    except Exception as e:
        logger.error(f"Ошибка при создании графика для {symbol}: {e}")
        return {
            'success': False,
            'filename': '',
            'error': str(e)
        }