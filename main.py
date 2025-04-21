import logging
from config import TELEGRAM_TOKEN
from telegram.ext import Application
from handlers.commands import register_commands
from handlers.callbacks import register_callbacks

# Настройка логов
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main() -> None:
    """Запуск бота"""
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Регистрация обработчиков
    register_commands(app)
    register_callbacks(app)

    # Запуск бота
    logger.info("Бот запущен")
    app.run_polling()

if __name__ == "__main__":
    main()