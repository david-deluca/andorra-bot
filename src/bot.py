from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from config.settings import TELEGRAM_TOKEN
from src.ibkr import get_account_data
from src.portfolio import format_portfolio_message
from src.performance import generate_performance_chart
from src.claude import ask_claude
from src.projection import generate_projection_chart

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

async def portfolio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("⏳ Obteniendo datos de IBKR...")
    
    try:
        data = await get_account_data()
        message = format_portfolio_message(data)
        await update.message.reply_text(message, parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"❌ Error conectando a IBKR: {e}")

async def performance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("⏳ Generando gráfico...")
    try:
        buf = generate_performance_chart()
        await update.message.reply_photo(photo=buf, caption="📊 Rendimiento vs Benchmark — Últimos 6 meses")
    except Exception as e:
        await update.message.reply_text(f"❌ Error generando gráfico: {e}")

async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    question = " ".join(context.args)
    if not question:
        await update.message.reply_text(
            "❓ Escribe tu pregunta después del comando.\n"
            "Ejemplo: /ask ¿Debo rebalancear mi portfolio ahora?"
        )
        return
    await update.message.reply_text("⏳ Consultando...")
    try:
        response = await ask_claude(question)
        await update.message.reply_text(response)
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def projection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args
    if len(args) != 4:
        await update.message.reply_text(
            "📊 Uso: /projection <capital_inicial> <aportacion_mensual> <retorno_anual_%> <años>\n"
            "Ejemplo: /projection 10000 500 7 20"
        )
        return

    try:
        initial_capital = float(args[0])
        monthly_contribution = float(args[1])
        annual_return = float(args[2]) / 100
        years = int(args[3])

        if years < 1 or years > 50:
            await update.message.reply_text("❌ El plazo debe estar entre 1 y 50 años.")
            return
        if annual_return <= 0 or annual_return > 0.30:
            await update.message.reply_text("❌ El retorno debe estar entre 0.1% y 30%.")
            return

    except ValueError:
        await update.message.reply_text("❌ Parámetros inválidos. Usa números.")
        return

    await update.message.reply_text("⏳ Calculando proyección...")

    try:
        buf, data = generate_projection_chart(
            initial_capital, monthly_contribution, annual_return, years
        )
        caption = (
            f"📈 *Proyección a {years} años*\n\n"
            f"Capital final: €{data['final_value']:,.0f}\n"
            f"Total invertido: €{data['total_invested']:,.0f}\n"
            f"Rendimiento generado: €{data['total_return']:,.0f}"
        )
        await update.message.reply_photo(photo=buf, caption=caption)
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

def build_application() -> Application:
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("portfolio", portfolio))
    app.add_handler(CommandHandler("performance", performance))
    app.add_handler(CommandHandler("ask", ask))
    app.add_handler(CommandHandler("projection", projection))
    return app