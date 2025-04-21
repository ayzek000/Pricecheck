from api import (
    get_crypto_price,
    get_stock_price,
    get_forex_price,
    get_commodity_price
)
from models import get_asset_type

def get_price(symbol: str) -> float:
    """Получает цену актива по его символу"""
    asset_type = get_asset_type(symbol)

    if asset_type == 'crypto':
        return get_crypto_price(symbol)
    elif asset_type == 'stocks':
        return get_stock_price(symbol)
    elif asset_type == 'forex':
        return get_forex_price(symbol)
    elif asset_type == 'commodities':
        return get_commodity_price(symbol)
    else:
        return 0.0
