import re
from collections import deque
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)

# حافظه لینک‌ها
message_storage = deque(maxlen=1000)

def extract_divar_links(text: str) -> list:
    # فقط لینک‌های divar
    return re.findall(r'https://divar\.ir/v/\S+', text)

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! من آماده‌ام آگهی‌های تکراری دیوار رو حذف کنم.")

# ثبت پیام‌ها
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg:
        return

    text = msg.text or msg.caption
    if not text:
        return

    links = extract_divar_links(text)
    if not links:
        return

    message_storage.append({
        "message_id": msg.message_id,
        "chat_id": msg.chat_id,
        "links": links
    })

# ارسال دکمه حذف
async def send_cleanup_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🗑 حذف آگهی‌های تکراری دیوار", callback_data='remove_duplicates')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('برای حذف آگهی‌های تکراری، دکمه زیر را بزنید:', reply_markup=reply_markup)

# حذف پیام‌های تکراری
async def remove_duplicates_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    deleted_count = 0
    seen_links = set()
    messages_to_delete = []

    for msg in message_storage:
        key = tuple(sorted(msg['links']))
        if key in seen_links:
            messages_to_delete.append(msg)
        else:
            seen_links.add(key)

    for msg in messages_to_delete:
        try:
            await context.bot.delete_message(chat_id=msg["chat_id"], message_id=msg["message_id"])
            deleted_count += 1
        except Exception as e:
            print(f"خطا در حذف پیام {msg['message_id']}: {e}")

    await query.edit_message_text(text=f"✅ {deleted_count} آگهی تکراری دیوار حذف شد.")

# اجرای ربات
if __name__ == '__main__':
    TOKEN = "8143882098:AAGiDsdMeFLnzKK0WjF4Vrh2V1y8XFVBr8o"
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("clean", send_cleanup_button))

    app.add_handler(MessageHandler(
        (filters.TEXT | filters.PHOTO | filters.VIDEO) & (~filters.COMMAND),
        handle_message
    ))

    app.add_handler(CallbackQueryHandler(remove_duplicates_button, pattern='remove_duplicates'))

    print("🤖 ربات در حال اجراست...")
    app.run_polling()
