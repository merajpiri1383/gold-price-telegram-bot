# Load Enivronment
import os
from dotenv import load_dotenv
load_dotenv()
# Telegram Imports 
from telegram import (
    Update,
    InlineKeyboardButton,InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    CallbackQueryHandler
)

# Messages
import messages
# Utils 
from utils import buttons,get_gold_price

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")




# Start Command
async def start (update : Update, context : ContextTypes.DEFAULT_TYPE) : 

    all_buttons = [InlineKeyboardButton(
        text=item["name"],callback_data="gold_price:" + item["slug"]
    ) for item in buttons]

    keyboards = [all_buttons[i:i + 2] for i in range(0, len(all_buttons), 2)]

    markup = InlineKeyboardMarkup(
        inline_keyboard=keyboards,
    )

    await update.message.reply_text(
        text=messages.WELLCOME_MESSAGE,
        reply_markup=markup
    )



# Callback Handler 

async def callback_handler (update : Update, context : ContextTypes.DEFAULT_TYPE) : 

    query = update.callback_query
    await query.answer()

    slug = query.data.replace("gold_price:","")
    result = await get_gold_price(slug=slug)

    await context.bot.send_message(
        chat_id=query.message.chat.id,
        text=result,
        parse_mode="HTML"
    )


# Create Application Instance
app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

# Add Handlers 
app.add_handler(CommandHandler(command="start",callback=start))
app.add_handler(CallbackQueryHandler(callback=callback_handler,pattern=r"^gold_price:"))

if __name__ == "__main__" :
    print("Starting Bot ...")

    app.run_polling()