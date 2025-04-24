from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, WebhookHandler
import logging
import os

TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "banglewebhook123")

logging.basicConfig(
    filename="telegram.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

app = Flask(__name__)
application = ApplicationBuilder().token(TOKEN).build()
webhook_handler = WebhookHandler(application)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(f"✅ Received /start from user: {update.effective_user.id}")
    await update.message.reply_text("👋 হ্যালো! Flask দিয়ে বট চলছে Render-এ!")

application.add_handler(CommandHandler("start", start))

@app.route(f"/{WEBHOOK_SECRET}", methods=["POST"])
def webhook():
    return webhook_handler.handle_update(request)

@app.route("/")
def home():
    return "🔋 Bot is running on Render!"

app = app
