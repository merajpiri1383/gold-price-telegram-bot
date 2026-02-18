import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler
from utils import buttons, get_price_by_slug

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
PROXY_URL = os.getenv("PROXY_URL")

if PROXY_URL:
    os.environ["HTTP_PROXY"] = PROXY_URL
    os.environ["HTTPS_PROXY"] = PROXY_URL
    os.environ["ALL_PROXY"] = PROXY_URL

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ساخت دکمه‌ها به صورت دو تایی در هر ردیف
    keyboard = []
    row = []
    for btn in buttons:
        row.append(InlineKeyboardButton(btn["name"], callback_data=btn["slug"]))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "👋 سلام! برای دریافت قیمت لحظه‌ای، یکی از گزینه‌های زیر را انتخاب کنید:",
        reply_markup=reply_markup
    
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer(text="در حال دریافت قیمت...") # نمایش پیام موقت بالای صفحه
    
    slug = query.data
    # دریافت متن قیمت از utils
    result_text = get_price_by_slug(slug)
    
    # ویرایش پیام قبلی یا ارسال پیام جدید (اینجا پیام جدید ارسال می‌کنیم)
    await query.message.reply_text(
        text=result_text,
        parse_mode="HTML"
    )

app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_callback))

if __name__ == "__main__":
    print("Bot is running...")
    app.run_polling()