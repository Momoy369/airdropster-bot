from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, filters, ContextTypes
from image_sender import send_utc_image

# Kata kunci
airdrop_keywords = [
    "airdrop", "ada airdrop?", "airdrop terbaru", "info airdrop",
    "airdop", "airdorp", "ada drop?", "kapan airdrop", "airdrop mana bang", "garap", "garapan"
]

time_keywords = [
    "jam berapa", "utc", "kapan mulai", "waktu airdrop", "waktunya kapan",
    "jam drop", "jam claim", "jam snapshot", "waktu snapshot"
]

bot_keywords = [
    "admin", "bot", "min", "halo bot", "bang bot", "info dong", "bantu dong"
]

fallback_keywords = [
    "claim", "snapshot", "token gratis", "dapet token", "reward", "crypto gratis"
]

jp_keywords = [
    "jp", "jackpot"
]

jual_keywords = [
    "jual", "menjual", "bejual", "jualan"
]

# Glosarium
glossary = {
    "early access": "🔓 *Early Access* artinya kamu bisa menggunakan atau mencoba platform lebih awal dari publik. Kadang dapat reward juga!",
    "testnet": "🧪 *Testnet* adalah jaringan percobaan, tempat kita bisa mencoba aplikasi blockchain tanpa pakai uang asli.",
    "faucet": "🚰 *Faucet* adalah tempat untuk mendapatkan token gratis di testnet. Biasanya dipakai buat testing transaksi.",
    "bep-20": "📦 *BEP-20* adalah standar token di jaringan Binance Smart Chain. Mirip seperti ERC-20 di Ethereum.",
    "evm": "⚙️ *EVM (Ethereum Virtual Machine)* adalah mesin virtual untuk menjalankan smart contract. Banyak jaringan support EVM, termasuk BSC dan Polygon.",
    "waitlist": "📋 *Waitlist* artinya kamu mendaftar lebih dulu untuk dapat kesempatan ikut project/token sebelum dibuka untuk umum.",
    "wallet": "👛 *Wallet* adalah dompet digital untuk menyimpan dan mengelola aset kripto. Pastikan simpan seed phrase dengan aman!",
    "kyc": "KYC adalah singkatan dari Know Your Customer. Beberapa proyek airdrop membutuhkan KYC untuk mengenali atau memverifikasi identitas pengguna",
    "snapshot": "Snapshot adalah salinan data atau keadaan suatu sistem pada titik waktu tertentu",
    "mainnet": "Mainnet adalah jaringan blockchain utama yang digunakan untuk transaksi sebenarnya dengan aset kripto",
    "swap": "Swap kripto adalah proses menukar satu aset kripto dengan aset kripto lainnya secara langsung, tanpa melalui proses konversi ke mata uang fiat terlebih dahulu",
    "bridge": "Bridge kripto adalah teknologi yang memungkinkan transfer aset dan data antar berbagai jaringan blockchain yang berbeda",
    "staking": "Staking kripto adalah proses mengamankan jaringan blockchain dengan cara menyimpan atau mengunci aset kripto dalam dompet digital untuk mendukung operasi jaringan. Sebagai imbalannya, pemilik aset akan mendapatkan reward berupa token atau koin tambahan dari jaringan tersebut.",
    "stake": "Staking kripto adalah proses mengamankan jaringan blockchain dengan cara menyimpan atau mengunci aset kripto dalam dompet digital untuk mendukung operasi jaringan. Sebagai imbalannya, pemilik aset akan mendapatkan reward berupa token atau koin tambahan dari jaringan tersebut.",
    "cex": "CEX dalam konteks mata uang kripto adalah singkatan dari Centralized Exchange, atau dalam bahasa Indonesia disebut Bursa Terpusat.",
    "dex": "DEX dalam kripto adalah singkatan dari Decentralized Exchange, atau dalam bahasa Indonesia disebut Bursa Terdesentralisasi.",
    "lfg": "LFG adalah singkatan dari Lets Fucking Go",
    "tge": "TGE adalah singkatan dari Token Generation Event, acara peluncuran token",
    "node": "Node crypto adalah komputer yang terhubung ke jaringan blockchain dan berperan dalam memvalidasi transaksi, menyimpan data, dan memastikan integritas jaringan. Biasanya butuh koneksi dan data besar.",
    "DePin": "DePIN, singkatan dari Decentralized Physical Infrastructure Networks, adalah jaringan infrastruktur fisik yang terdesentralisasi yang memanfaatkan teknologi blockchain dan token kripto untuk membangun, mengelola, dan mengoperasikan aset infrastruktur secara bersama-sama oleh komunitas."
}

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"[START] User {update.effective_user.username} memulai bot.")
    await update.message.reply_text("👋 Selamat datang di Airdropster!")

# /utc command
async def send_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"[IMAGE] Mengirim gambar UTC ke {update.effective_user.username}")
    await send_utc_image(update, context)

# Auto-reply berdasarkan keyword
async def keyword_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or update.message.caption or ""
    text = text.lower()

    user = update.effective_user.username or update.effective_user.first_name
    print(f"[MESSAGE] {user}: {text}")

    if update.message.photo:
        print(f"[PHOTO] {user} mengirim gambar.")

    if any(kw in text for kw in airdrop_keywords):
        await update.message.reply_text("🚀 Airdrop terbaru akan dibagikan di channel @airdropsterich, stay tuned ya!")
    elif any(kw in text for kw in time_keywords):
        await send_utc_image(update, context)
    elif any(kw in text for kw in bot_keywords):
        await update.message.reply_text("🤖 Saya di sini bantu info airdrop dan waktu claim. Gunakan kata kunci seperti 'airdrop' atau 'utc' ya!")
    elif any(kw in text for kw in fallback_keywords):
        await update.message.reply_text("🎁 Banyak token gratis lewat airdrop. Cek update-nya di @airdropsterich.")
    elif any(kw in text for kw in jp_keywords):
        await update.message.reply_text("Iya, iya. Kalau JP jangan lupa bagi-bagi ke admin")
    elif any(kw in text for kw in jual_keywords):
        await update.message.reply_text("Jangan jual koin kalau belum listing, nanti kamu nyesel harga meroket")
    else:
        for term, definition in glossary.items():
            if term in text:
                await update.message.reply_markdown(definition)
                return

# Setup handler
def setup_handlers(application):
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("utc", send_schedule))

    # Gunakan filter PTB v20
    smart_filter = (
        filters.TEXT |
        filters.PHOTO |
        filters.Caption() |
        filters.Entity("mention") |
        filters.REPLY
    )

    application.add_handler(MessageHandler(smart_filter, keyword_reply))
