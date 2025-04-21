import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)
from api import (
    get_crypto_price, 
    get_stock_price, 
    get_forex_price, 
    get_commodity_price
)
from models import ASSETS, get_asset_type, get_asset_name, get_asset_info
from handlers.alerts import price_check_callback
from handlers.callbacks import start_menu
from utils.price_utils import get_price  # Импорт из правильного модуля

logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда /start - показывает главное меню"""
    await start_menu(update.message, context)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда /help - показывает справку"""
    help_text = """
📌 Доступные команды:
/start - Главное меню
/price [код] - Цена актива (например: /price BTCUSDT)
/alert [код] [%] - Уведомление (например: /alert AAPL 2)
/graph [код] - График (только для криптовалют)

Или используйте кнопки меню для удобства
"""
    await update.message.reply_text(help_text)

async def price_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /price"""
    if not context.args:
        await update.message.reply_text("❌ Укажите код актива (например: /price BTCUSDT)")
        return
    
    symbol = context.args[0].upper()
    price = get_price(symbol)
    
    if price == 0.0:
        await update.message.reply_text(f"❌ Не удалось получить цену для {symbol}")
        return
    
    asset_type = get_asset_type(symbol)
    if not asset_type:
        await update.message.reply_text("❌ Актив не найден")
        return
    
    await update.message.reply_text(f"💰 {get_asset_name(symbol)}: ${price:.2f}")

async def alert_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /alert"""
    if len(context.args) != 2:
        await update.message.reply_text("❌ Используйте: /alert [код] [процент]")
        return
    
    symbol = context.args[0].upper()
    try:
        threshold = float(context.args[1])
    except ValueError:
        await update.message.reply_text("❌ Процент должен быть числом")
        return
    
    asset_type = get_asset_type(symbol)
    if not asset_type:
        await update.message.reply_text("❌ Актив не найден")
        return
    
    current_price = get_price(symbol)
    if current_price == 0.0:
        await update.message.reply_text(f"❌ Не удалось получить текущую цену для {symbol}")
        return
        
    context.bot_data[f"last_price_{symbol}"] = current_price
    
    context.job_queue.run_repeating(
        price_check_callback,
        interval=60,
        first=10,
        chat_id=update.effective_chat.id,
        data={'symbol': symbol, 'threshold': threshold},
        name=f'{update.effective_chat.id}_{symbol}'
    )
    
    await update.message.reply_text(
        f"🔔 Уведомление для {get_asset_name(symbol)} установлено на {threshold}%"
    )

async def graph_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /graph"""
    if not context.args:
        await update.message.reply_text("❌ Укажите код актива (например: /graph BTCUSDT)")
        return
    
    symbol = context.args[0].upper()
    asset_type = get_asset_type(symbol)
    
    if not asset_type:
        await update.message.reply_text("❌ Актив не найден")
        return
    
    if asset_type != 'crypto':
        await update.message.reply_text("⚠️ Графики доступны только для криптовалют")
        return
    
    from utils.chart import create_chart
    result = await create_chart(symbol)
    
    if result['success']:
        await update.message.reply_photo(photo=open(result['filename'], 'rb'))
    else:
        await update.message.reply_text(f"❌ Ошибка: {result['error']}")

def register_commands(app: Application) -> None:
    """Регистрация обработчиков команд"""
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("price", price_command))
    app.add_handler(CommandHandler("alert", alert_command))
    app.add_handler(CommandHandler("graph", graph_command))
