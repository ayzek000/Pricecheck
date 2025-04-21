import logging
from telegram import Update
from telegram.ext import ContextTypes
from utils.price_utils import get_price
from models import get_asset_name



logger = logging.getLogger(__name__)

async def handle_set_alert(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Меню установки уведомления"""
    query = update.callback_query
    await query.answer()
    symbol = query.data.split('_')[1]
    
    # Получаем текущую цену для инициализации
    current_price = get_price(symbol)
    if current_price == 0.0:
        await query.message.reply_text(f"❌ Не удалось получить текущую цену для {get_asset_name(symbol)}")
        return
        
    context.user_data['alert_symbol'] = symbol
    context.bot_data[f"last_price_{symbol}"] = current_price
    
    await query.message.reply_text(
        f"Введите процент для уведомления по {get_asset_name(symbol)}:\n"
        "Например: 2.5 (изменение на 2.5%)"
    )

async def set_alert(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Установка уведомления на основе введенного процента"""
    try:
        symbol = context.user_data.get('alert_symbol')
        if not symbol:
            await update.message.reply_text("❌ Сначала выберите актив для уведомления")
            return
            
        threshold = float(update.message.text)
        
        # Проверяем, что процент положительный
        if threshold <= 0:
            await update.message.reply_text("❌ Процент должен быть положительным числом")
            return
        
        # Устанавливаем уведомление
        context.job_queue.run_repeating(
            price_check_callback,
            interval=60,  # Проверка каждую минуту
            first=10,     # Первая проверка через 10 секунд
            chat_id=update.effective_chat.id,
            data={'symbol': symbol, 'threshold': threshold},
            name=f'{update.effective_chat.id}_{symbol}'
        )
        
        await update.message.reply_text(
            f"🔔 Уведомление для {get_asset_name(symbol)} установлено на {threshold}%"
        )
        
        # Очищаем выбранный символ
        context.user_data.pop('alert_symbol', None)
        
    except ValueError:
        await update.message.reply_text("❌ Введите число (например: 2.5)")

async def price_check_callback(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Проверка изменения цены"""
    job = context.job
    symbol = job.data['symbol']
    threshold = job.data['threshold']
    
    # Получаем текущую цену
    current_price = get_price(symbol)
    
    # Если не удалось получить цену, пропускаем проверку
    if current_price == 0.0:
        logger.warning(f"Не удалось получить цену для {symbol} при проверке уведомления")
        return
    
    # Получаем последнюю сохраненную цену
    last_price = context.bot_data.get(f"last_price_{symbol}", current_price)
    
    # Рассчитываем изменение в процентах
    change = (current_price - last_price) / last_price * 100
    
    # Проверяем, превышен ли порог
    if abs(change) >= threshold:
        direction = "↗️ выросла на" if change > 0 else "↘️ упала на"
        await context.bot.send_message(
            chat_id=job.chat_id,
            text=f"🚨 {get_asset_name(symbol)} {direction} {abs(change):.2f}%!\n"
                 f"Цена: ${current_price:.2f} (было: ${last_price:.2f})"
        )
        
        # Обновляем сохраненную цену после отправки уведомления
        context.bot_data[f"last_price_{symbol}"] = current_price
    
    # Если изменение меньше порога, просто обновляем цену
    else:
        context.bot_data[f"last_price_{symbol}"] = current_price