import os
import json
import asyncio
from datetime import datetime
import redis  # ← مكتبة Redis العادية (متزامنة، بدون await)
from telethon import TelegramClient, events
from telethon.tl.types import DocumentAttributeAudio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

wfffp = 1910015590
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("m")  # ← لازم يكون معرّف بمتغير البيئة

ALLOWED_USERS = [wfffp, 6520830528]
TARGET_CHANNEL = wfffp  # ⚠️ تأكد إنه آيدي قناتك الصحيح (راجع الملاحظة تحت)
TIMEZONE = "Asia/Baghdad"

# فقط اسم الناشر (Performer) اللي بيتغير
CUSTOM_PERFORMER = "صدى الحسين"
CUSTOM_THUMB = "IMG_5528.jpeg"  # اختياري: صورة غلاف ثابتة (احذفها لو ما تبغى تغيّرها)

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
QUEUE_KEY = "pending_audio_queue"
LOCK_KEY = "audio_publish_lock"
DOWNLOAD_DIR = "downloads"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

M = TelegramClient("m", api_id, api_hash)
r = redis.from_url(REDIS_URL, decode_responses=True)  # ← عميل متزامن، بدون asyncio


def is_audio(e):
    return bool(e.audio) or (e.document and e.document.mime_type and e.document.mime_type.startswith("audio/"))


def get_original_title(e):
    """يستخرج الـ title الأصلي من attributes الملف، أو يستخدم اسم الملف كبديل"""
    if e.audio and e.audio.title:
        return e.audio.title
    # fallback: اسم الملف بدون الامتداد
    if e.document and e.document.attributes:
        for attr in e.document.attributes:
            if hasattr(attr, "file_name") and attr.file_name:
                return os.path.splitext(attr.file_name)[0]
    return "صدى الحسين"


@M.on(events.NewMessage(from_users=ALLOWED_USERS))
async def collect(e):
    if not is_audio(e):
        return

    file_path = await e.download_media(file=DOWNLOAD_DIR)

    original_title = get_original_title(e)
    duration = e.audio.duration if e.audio else 0

    item = {
        "file_path": file_path,
        "duration": duration,
        "title": original_title  # نحفظ العنوان الأصلي كما هو
    }
    r.rpush(QUEUE_KEY, json.dumps(item))  # بدون await
    print(f"📥 صوتي أُضيف للطابور: {original_title}")


async def publish_queue():
    lock_acquired = r.set(LOCK_KEY, "1", nx=True, ex=600)  # بدون await
    if not lock_acquired:
        print("⏭️ يوجد تنفيذ آخر شغال حاليًا، تم التجاوز")
        return

    try:
        items_raw = r.lrange(QUEUE_KEY, 0, -1)  # بدون await
        if not items_raw:
            print("ℹ️ ما فيه ملفات صوتية بالطابور")
            return

        sent_count = 0
        for raw in items_raw:
            item = json.loads(raw)
            fpath = item["file_path"]

            if not os.path.exists(fpath):
                print(f"⚠️ الملف غير موجود: {fpath}")
                continue

            try:
                await M.send_file(
                    TARGET_CHANNEL,
                    fpath,
                    thumb=CUSTOM_THUMB if os.path.exists(CUSTOM_THUMB) else None,
                    attributes=[
                        DocumentAttributeAudio(
                            duration=item["duration"],
                            title=item["title"],          # ← يبقى كما هو بالأصل
                            performer=CUSTOM_PERFORMER     # ← فقط هذا يتغيّر
                        )
                    ],
                    force_document=False
                )
                sent_count += 1
                os.remove(fpath)
            except Exception as E:
                print(f"⚠️ فشل نشر ملف: {E}")

        r.delete(QUEUE_KEY)  # بدون await
        print(f"✅ تم نشر {sent_count} ملف صوتي الساعة {datetime.now()}")

    finally:
        r.delete(LOCK_KEY)  # بدون await


async def main():
    # تشغيل الحساب كبوت بدل حساب مستخدم (userbot)
    await M.start(bot_token=bot_token)

    scheduler = AsyncIOScheduler(timezone=TIMEZONE)
    # scheduler.add_job(publish_queue, CronTrigger(hour=18, minute=30))  # 6:30 مساءً (الوقت الأساسي)
    scheduler.add_job(publish_queue, CronTrigger(hour=13, minute=44))  # 1:42 مساءً (تجربة)
    scheduler.start()

    print("🚀 البوت شغال، بانتظار الملفات الصوتية...")
    

