import requests
from bs4 import BeautifulSoup
import yfinance as yf
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
    """یک تابع کمکی برای دریافت قیمت‌ها از TGJU"""
    url = 'https://www.tgju.org/'
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # استخراج دلار
        dollar_elem = soup.find('tr', {'data-market-row': 'price_dollar_rl'})
        dollar = dollar_elem.find('td', class_='nf').text.strip() if dollar_elem else "نامشخص"
        
        # استخراج طلا ۱۸
        gold_elem = soup.find('tr', {'data-market-row': 'geram18'})
        gold18 = gold_elem.find('td', class_='nf').text.strip() if gold_elem else "نامشخص"
        
        return {"dollar": dollar, "gold_18k": gold18}
    except Exception as e:
        print(f"Error TGJU: {e}")
        return {"dollar": "خطا", "gold_18k": "خطا"}

def get_ounce_price():
    """دریافت قیمت انس از یاهو"""
    try:
        ticker = yf.Ticker("GC=F")
        price = ticker.history(period="1d")['Close'].iloc[-1]
        return f"{price:,.2f}$"
    except:
        return "خطا"

def get_current_time():
    return datetime.now(pytz.timezone('Asia/Tehran')).strftime("%H:%M")

def get_price_by_slug(slug):
    """این تابع برای دکمه‌های ربات استفاده می‌شود"""
    if slug == "ounce":
        price = get_ounce_price()
        return f"💰 <b>انس جهانی:</b> {price}"
    
    # برای دلار و طلا نیاز به TGJU داریم
    data = get_tgju_data()
    
    if slug == "dollar":
        return f"💵 <b>دلار آزاد:</b> {data['dollar']} ریال"
    elif slug == "gold_18k":
        return f"⚜️ <b>طلا ۱۸ عیار:</b> {data['gold_18k']} ریال"
    elif slug == "full_report":
        return get_full_report() # اگر دکمه گزارش کامل را زد
    else:
        return "گزینه نامعتبر است."

def get_full_report():
    """این تابع برای ارسال خودکار به کانال استفاده می‌شود"""
    tgju = get_tgju_data()
    ounce = get_ounce_price()
    time = get_current_time()
    
    return (
        f"طلا ۱۸ عیار: {tgju['gold_18k']}\n"
        f"اونس جهانی: {ounce}\n"
        f"دلار آزاد: {tgju['dollar']}\n"
        f"{time} | TradingView + TGJU"
    )