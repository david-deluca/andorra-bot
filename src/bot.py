from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from config.settings import TELEGRAM_TOKEN

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "🤖 *Andorra Bot* activo.\n\n"
        "Comandos disponibles:\n"
        "/portfolio — Resumen de tu cartera IBKR\n"
        "/performance — Rendimiento vs benchmark\n"
        "/projection — Proyección de interés compuesto\n"
        "/ask — Pregunta libre (contexto Boglehead)\n"
        "/help — Esta ayuda",
        parse_mode="Markdown"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Comandos disponibles:\n"
        "/portfolio /performance /projection /ask"
    )

def build_application() -> Application:
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    return app