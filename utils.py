import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz

# لیست دکمه‌ها برای نمایش در ربات
buttons = [
    {"name": "طلای ۱۸ عیار", "slug": "gold_18k"},
    {"name": "دلار آزاد", "slug": "dollar"},
    {"name": "انس جهانی", "slug": "ounce"},
    {"name": "گزارش کامل", "slug": "full_report"}
]

def get_tgju_data():
    """دریافت تمامی قیمت‌ها (طلا، دلار و انس) از سایت TGJU"""
    url = 'https://www.tgju.org/'
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        def get_text_by_row(slug):
            """تابع کمکی برای یافتن قیمت بر اساس اسلاگ"""
            try:
                tag = soup.find('tr', {'data-market-row': slug})
                if tag:
                    price = tag.find('td', class_='nf').text.strip()
                    return price
                return "خطا"
            except:
                return "خطا"

        return {
            "dollar": get_text_by_row('price_dollar_rl'),
            "gold_18k": get_text_by_row('geram18'),
            "ounce": get_text_by_row('ons') # دریافت انس جهانی از TGJU
        }
    except Exception as e:
        print(f"Error TGJU: {e}")
        return {"dollar": "خطا", "gold_18k": "خطا", "ounce": "خطا"}

def get_current_datetime():
    """دریافت تاریخ و زمان فعلی تهران"""
    now = datetime.now(pytz.timezone('Asia/Tehran'))
    # فرمت خروجی: سال/ماه/روز | ساعت:دقیقه
    return now.strftime("%Y/%m/%d | %H:%M")

def get_price_by_slug(slug):
    """این تابع برای پاسخ به دکمه‌های تکی ربات استفاده می‌شود"""
    data = get_tgju_data()
    
    if slug == "ounce":
        return f"💰 انس جهانی: <b>{data['ounce']}</b> دلار"
    elif slug == "dollar":
        return f"💵 دلار آزاد: <b>{data['dollar']}</b> ریال"
    elif slug == "gold_18k":
        return f"⚜️ طلا ۱۸ عیار: <b>{data['gold_18k']}</b> ریال"
    elif slug == "full_report":
        return get_full_report()
    else:
        return "گزینه نامعتبر است."

def get_full_report():
    """این تابع برای ارسال خودکار به کانال استفاده می‌شود"""
    data = get_tgju_data()
    date_time = get_current_datetime()
    
    return (
        f"⚜️ طلا ۱۸ عیار: <b>{data['gold_18k']}</b>\n"
        f"💰 اونس جهانی: <b>{data['ounce']}</b>\n"
        f"💵 دلار آزاد: <b>{data['dollar']}</b>\n"
        f"{date_time} 📅"
    )