from telegram import Update
from telegram.ext import ContextTypes

async def send_utc_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open("utc_schedule.jpg", "rb") as img:
        await update.message.reply_photo(
            photo=img,
            caption="🕒 Ini jadwal airdrop berdasarkan waktu UTC."
        )
