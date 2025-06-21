import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder
from handlers import setup_handlers

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Buat aplikasi berbasis async
app = ApplicationBuilder().token(TOKEN).build()

# Pasang semua handler
setup_handlers(app)

# Jalankan polling
if __name__ == "__main__":
    print("[BOT] Bot berjalan...")
    app.run_polling()
