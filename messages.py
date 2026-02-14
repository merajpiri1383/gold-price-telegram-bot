


WELLCOME_MESSAGE = """سلام! به ربات اطلاع‌رسانی قیمت طلا خوش آمدید. 🌹
ما در اینجا نرخ‌های لحظه‌ای و دقیق بازار طلا را در اختیار شما قرار می‌دهیم.

برای مشاهده نرخ لحظه‌ای، لطفاً یکی از گزینه‌های زیر انتخاب کنید"""

API_ERROR_MESSAGE = "متأسفانه مشکلی در دریافت قیمت‌ها پیش آمده است. لطفاً چند لحظه دیگر دوباره امتحان کنید."


def format_gold_message(data):
    # 1. Determine emoji for change (Red for negative, Green for positive)
    change = data.get('dayChange', 0)
    if change > 0:
        change_emoji = "🟢"
        change_str = f"+{change}" # Add plus sign for positive
    elif change < 0:
        change_emoji = "🔴"
        change_str = f"{change}"
    else:
        change_emoji = "⚪️"
        change_str = "0"

    # 2. Format numbers with commas (e.g. 5042.34 -> 5,042.34)
    price = "{:,.2f}".format(data['price'])
    high = "{:,.2f}".format(data['high'])
    low = "{:,.2f}".format(data['low'])
    open_price = "{:,.2f}".format(data['open'])

    # 3. Create the message
    message = (
        f"📊 <b>{data['name']}</b>\n\n"
        f"💰 <b>قیمت لحظه‌ای:</b> {price}\n"
        f"{change_emoji} <b>تغییر روزانه:</b> {change_str}%\n\n"
        f"⬆️ <b>بالاترین:</b> {high}\n"
        f"⬇️ <b>پایین‌ترین:</b> {low}\n"
        f"🔓 <b>قیمت بازگشایی:</b> {open_price}\n\n"
        f"🕒 <b>آخرین بروزرسانی:</b>\n{data['updated_at']}"
    )
    
    return message