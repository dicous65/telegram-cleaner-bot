from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

async def show_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    chat_id = chat.id
    print(f"📥 Chat ID: {chat_id}")
    await update.message.reply_text(f"Chat ID: {chat_id}")

if __name__ == '__main__':
    TOKEN = "توکن_ربات_اینجا"  # مثلاً: "123456789:ABCDEF..."
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.ALL, show_chat_id))

    print("✅ ربات آماده دریافت پیام است...")
    app.run_polling()
