# Словарь активов
ASSETS = {
    'crypto': {
        'BTCUSDT': {'name': 'Bitcoin', 'source': 'binance'},
        'ETHUSDT': {'name': 'Ethereum', 'source': 'binance'},
        'BNBUSDT': {'name': 'Binance Coin', 'source': 'binance'},
        'SOLUSDT': {'name': 'Solana', 'source': 'binance'},
        'ADAUSDT': {'name': 'Cardano', 'source': 'binance'},
        'DOTUSDT': {'name': 'Polkadot', 'source': 'binance'}
    },
    'stocks': {
        'AAPL': {'name': 'Apple Inc.', 'source': 'alphavantage'},
        'MSFT': {'name': 'Microsoft', 'source': 'alphavantage'},
        'GOOGL': {'name': 'Alphabet (Google)', 'source': 'alphavantage'},
        'AMZN': {'name': 'Amazon', 'source': 'alphavantage'},
        'TSLA': {'name': 'Tesla', 'source': 'alphavantage'},
        'META': {'name': 'Meta Platforms', 'source': 'alphavantage'}
    },
    'forex': {
        'EUR/USD': {'name': 'EUR/USD', 'source': 'alphavantage', 'from': 'EUR', 'to': 'USD'},
        'USD/JPY': {'name': 'USD/JPY', 'source': 'alphavantage', 'from': 'USD', 'to': 'JPY'},
        'GBP/USD': {'name': 'GBP/USD', 'source': 'alphavantage', 'from': 'GBP', 'to': 'USD'},
        'USD/CHF': {'name': 'USD/CHF', 'source': 'alphavantage', 'from': 'USD', 'to': 'CHF'},
        'AUD/USD': {'name': 'AUD/USD', 'source': 'alphavantage', 'from': 'AUD', 'to': 'USD'},
        'USD/CAD': {'name': 'USD/CAD', 'source': 'alphavantage', 'from': 'USD', 'to': 'CAD'}
    },
    'commodities': {
        'GC': {'name': 'Gold', 'source': 'alphavantage'},
        'SI': {'name': 'Silver', 'source': 'alphavantage'},
        'CL': {'name': 'Crude Oil', 'source': 'alphavantage'},
        'NG': {'name': 'Natural Gas', 'source': 'alphavantage'},
        'HG': {'name': 'Copper', 'source': 'alphavantage'},
        'PL': {'name': 'Platinum', 'source': 'alphavantage'}
    }
}

def get_asset_type(symbol: str) -> str:
    """Получение типа актива по символу"""
    for asset_type, assets in ASSETS.items():
        if symbol in assets:
            return asset_type
    return None

def get_asset_name(symbol: str) -> str:
    """Получение названия актива по символу"""
    asset_type = get_asset_type(symbol)
    if asset_type and symbol in ASSETS[asset_type]:
        return ASSETS[asset_type][symbol]['name']
    return symbol

def get_asset_info(symbol: str) -> dict:
    """Получение всей информации об активе"""
    asset_type = get_asset_type(symbol)
    if asset_type and symbol in ASSETS[asset_type]:
        return ASSETS[asset_type][symbol]
    return {}