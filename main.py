from src.bot import build_application

def main():
    print("Arrancando andorra-bot...")
    app = build_application()
    print("Bot activo. Ctrl+C para detener.")
    app.run_polling(allowed_updates=["message"])

if __name__ == "__main__":
    main()