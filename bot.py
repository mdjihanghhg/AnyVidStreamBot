import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from extractor import extract_direct_link
import validators

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if not validators.url(url):
        return await update.message.reply_text("❌ বৈধ URL নয়।")

    dl = extract_direct_link(url)
    if dl:
        keyboard = InlineKeyboardMarkup([[ 
            InlineKeyboardButton("📥 ডাউনলোড লিংক", callback_data=f"download|{dl}") 
        ]])
        return await update.message.reply_video(video=dl, caption="🎬 ভিডিও প্রিভিউ:", reply_markup=keyboard)
    else:
        return await update.message.reply_text("❌ ভিডিও লিংক সাপোর্টেড নয়।")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    _, url = q.data.split("|", 1)
    return await q.message.reply_text(f"⬇️ ডাউনলোড লিংক:\n{url}")

def main():
    TOKEN = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()

if __name__ == "__main__":
    main()
