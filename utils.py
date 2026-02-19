import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz

# لیست دکمه‌ها برای نمایش در ربات
buttons = [
    {"name": "قیمت مظنه", "slug": "mazaneh"},
    {"name": "قیمت هر گرم طلا", "slug": "gold_18k"},
    {"name": "دلار آزاد", "slug": "dollar"},
    {"name": "انس جهانی", "slug": "ounce"},
    {"name": "گزارش کامل", "slug": "full_report"}
]

def get_tgju_data():
    """دریافت تمامی قیمت‌ها (طلا، مظنه، دلار و انس) از سایت TGJU"""
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
                
        def to_toman(price_str):
            """تبدیل رشته قیمتی ریال به تومان با جداکننده هزارگان"""
            if price_str == "خطا":
                return price_str
            try:
                # حذف کاماها و تبدیل به عدد صحیح (بدون در نظر گرفتن اعشار احتمالی)
                clean_str = price_str.replace(',', '').split('.')[0]
                num = int(clean_str)
                # تقسیم بر ۱۰ برای تبدیل ریال به تومان و فرمت‌بندی مجدد با کاما
                return f"{num // 10:,}"
            except Exception:
                return price_str

        return {
            "dollar": to_toman(get_text_by_row('price_dollar_rl')),
            "gold_18k": to_toman(get_text_by_row('geram18')),
            "mazaneh": to_toman(get_text_by_row('mesghal')),  # دریافت مظنه
            "ounce": get_text_by_row('ons') # انس جهانی بر اساس دلار است و نیازی به تبدیل ندارد
        }
    except Exception as e:
        print(f"Error TGJU: {e}")
        return {"dollar": "خطا", "gold_18k": "خطا", "mazaneh": "خطا", "ounce": "خطا"}

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
        return f"💵 دلار آزاد: <b>{data['dollar']}</b> تومان"
    elif slug == "gold_18k":
        return f"⚜️ قیمت هر گرم طلای ۱۸ عیار: <b>{data['gold_18k']}</b> تومان"
    elif slug == "mazaneh":
        return f"⚖️ قیمت مظنه طلا: <b>{data['mazaneh']}</b> تومان"
    elif slug == "full_report":
        return get_full_report()
    else:
        return "گزینه نامعتبر است."

def get_full_report():
    """این تابع برای ارسال خودکار به کانال و بات استفاده می‌شود"""
    data = get_tgju_data()
    date_time = get_current_datetime()
    
    return (
        f"⚖️ قیمت مظنه طلا: <b>{data['mazaneh']}</b> تومان\n"
        f"⚜️ هر گرم طلای ۱۸ عیار: <b>{data['gold_18k']}</b> تومان\n"
        f"💰 اونس جهانی: <b>{data['ounce']}</b> دلار\n"
        f"💵 دلار آزاد: <b>{data['dollar']}</b> تومان\n"
        f"📅 {date_time}"
    )