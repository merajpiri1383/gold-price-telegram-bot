import os
from celery import Celery
from celery.schedules import crontab
from celery.utils.log import get_task_logger
from dotenv import load_dotenv
import requests
from utils import get_full_report  # فقط تابع گزارش کامل ایمپورت می‌شود

logger = get_task_logger(__name__)
load_dotenv()

# Set Proxy if needed
PROXY_URL = os.getenv("PROXY_URL")
if PROXY_URL:
    os.environ["HTTP_PROXY"] = PROXY_URL
    os.environ["HTTPS_PROXY"] = PROXY_URL
    os.environ["ALL_PROXY"] = PROXY_URL

app = Celery(
    "telegram_bot",
    backend=os.getenv("CELERY_BACKEND"),
    broker=os.getenv("CELERY_BROKER"),
)

# تنظیم زمان‌بندی: هر ۴ دقیقه
app.conf.beat_schedule = {
    "send_gold_price_every_4_minutes": {
        "task": "celery_app.send_channel_message",
        "schedule": crontab(minute="*/4"),
    }
}

@app.task
def send_channel_message():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    channel_id = os.getenv("CHANNEL_ID")
    
    if not token or not channel_id:
        return

    # دریافت متن کامل و فرمت‌شده برای کانال
    text = get_full_report()
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": channel_id, "text": text}
    
    try:
        requests.post(url, json=payload, timeout=10)
        logger.info("Message sent to channel.")
    except Exception as e:
        logger.error(f"Failed to send message: {e}")