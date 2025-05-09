from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import logging
import os

TOKEN = os.environ.get("BOT_TOKEN")  # or replace directly as string
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "banglewebhook123")

logging.basicConfig(
    filename="telegram.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

app = Flask(__name__)
application = ApplicationBuilder().token(TOKEN).build()

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(f"✅ Received /start from user: {update.effective_user.id}")
    await update.message.reply_text("👋 হ্যালো! Flask দিয়ে Render-এ বট চলছে!")

application.add_handler(CommandHandler("start", start))

@app.route(f"/{WEBHOOK_SECRET}", methods=["POST"])
def webhook():
    try:
        data = request.get_json(force=True)
        update = Update.de_json(data, application.bot)
        application.update_queue.put_nowait(update)
    except Exception as e:
        logging.error(f"❌ Webhook Error: {e}")
    return "ok"

@app.route("/")
def home():
    return "🔋 Bot is running on Render!"

app = app
