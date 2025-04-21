import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters
)
from models import ASSETS, get_asset_type, get_asset_name
from utils.price_utils import get_price  # ✅ Правильный импорт
from handlers.alerts import handle_set_alert, set_alert
from utils.chart import create_chart

logger = logging.getLogger(__name__)

async def start_menu(message, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Главное меню"""
    keyboard = [
        [InlineKeyboardButton("💰 Криптовалюты", callback_data='crypto')],
        [InlineKeyboardButton("📈 Акции (В ПРОЦЕССЕ РАЗРАБОТКИ)", callback_data='stocks')],
        [InlineKeyboardButton("💱 Форекс (В ПРОЦЕССЕ РАЗРАБОТКИ)", callback_data='forex')],
        [InlineKeyboardButton("🛢️ Сырьевые товары (В ПРОЦЕССЕ РАЗРАБОТКИ)", callback_data='commodities')],
        [InlineKeyboardButton("ℹ️ Помощь", callback_data='help')]
    ]
    await message.reply_text(
        "📊 Выберите категорию активов:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Помощь по командам"""
    help_text = """
📌 Доступные команды:
/start - Главное меню
/price [код] - Цена актива (например: /price BTCUSDT)
/alert [код] [%] - Уведомление (например: /alert AAPL 2)
/graph [код] - График (только для криптовалют)

Или используйте кнопки меню для удобства
"""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(help_text)

async def handle_category(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка выбора категории"""
    query = update.callback_query
    await query.answer()
    category = query.data

    buttons = [
        [InlineKeyboardButton(asset['name'], callback_data=f'price_{symbol}')]
        for symbol, asset in ASSETS[category].items()
    ]
    buttons.append([InlineKeyboardButton("🔙 Назад", callback_data='back')])

    category_names = {
        'crypto': 'Криптовалюты',
        'stocks': 'Акции',
        'forex': 'Форекс',
        'commodities': 'Сырьевые товары'
    }

    await query.edit_message_text(
        f"Выберите актив ({category_names.get(category, category)}):",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

async def handle_price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показать цену актива"""
    query = update.callback_query
    await query.answer()
    symbol = query.data.split('_')[1]
    price = get_price(symbol)
    
    asset_type = get_asset_type(symbol)
    asset_name = get_asset_name(symbol)
    
    keyboard = [
        [InlineKeyboardButton("🔄 Обновить", callback_data=f'price_{symbol}')],
        [InlineKeyboardButton("🔔 Уведомление", callback_data=f'setalert_{symbol}')]
    ]
    
    # Добавляем кнопку графика только для криптовалют
    if asset_type == 'crypto':
        keyboard.insert(0, [InlineKeyboardButton("📈 График", callback_data=f'graph_{symbol}')])
    
    keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data=f'back_{asset_type}')])
    
    price_text = f"💰 {asset_name}: ${price:.2f}" if price > 0 else f"❌ Не удалось получить цену для {asset_name}"
    
    await query.edit_message_text(
        price_text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_graph(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Генерация графика"""
    query = update.callback_query
    await query.answer()
    symbol = query.data.split('_')[1]
    
    asset_type = get_asset_type(symbol)
    if asset_type == 'crypto':
        result = await create_chart(symbol)
        if result['success']:
            await query.message.reply_photo(photo=open(result['filename'], 'rb'))
        else:
            await query.message.reply_text(f"❌ Ошибка: {result['error']}")
    else:
        await query.message.reply_text("⚠️ Графики доступны только для криптовалют")

async def handle_back(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка кнопки Назад"""
    query = update.callback_query
    await query.answer()
    
    # Если указана категория для возврата
    if '_' in query.data:
        category = query.data.split('_')[1]
        query.data = category
        await handle_category(update, context)
    else:
        await start_menu(query.message, context)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик ошибок"""
    logger.error(f"Ошибка: {context.error}")
    if update.callback_query:
        await update.callback_query.answer("⚠️ Произошла ошибка")
        await update.callback_query.message.reply_text("⚠️ Произошла ошибка. Попробуйте позже.")
    else:
        await update.message.reply_text("⚠️ Произошла ошибка. Попробуйте позже.")

def register_callbacks(app: Application) -> None:
    """Регистрация обработчиков callback-запросов"""
    app.add_handler(CallbackQueryHandler(handle_help, pattern='^help$'))
    app.add_handler(CallbackQueryHandler(handle_category, pattern='^(crypto|stocks|forex|commodities)$'))
    app.add_handler(CallbackQueryHandler(handle_price, pattern='^price_'))
    app.add_handler(CallbackQueryHandler(handle_graph, pattern='^graph_'))
    app.add_handler(CallbackQueryHandler(handle_set_alert, pattern='^setalert_'))
    app.add_handler(CallbackQueryHandler(handle_back, pattern='^back'))
    
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, set_alert))
    
    app.add_error_handler(error_handler)
