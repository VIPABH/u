"""
audio_publisher.py
الملف الأساسي - يحتوي كل منطق استقبال الملفات الصوتية وإعادة نشرها مجدولاً.
لا تشغّل هذا الملف مباشرة، بل استدعِ الدالة register_audio_publisher من ملفك الرئيسي.
"""

import os
import json
from datetime import datetime
import redis  # مكتبة Redis العادية (متزامنة، بدون await)
from telethon import events
from telethon.tl.types import DocumentAttributeAudio
from apscheduler.triggers.cron import CronTrigger

wfffp = 1910015590

ALLOWED_USERS = [wfffp, 6520830528]
TARGET_CHANNEL = wfffp  # ⚠️ تأكد إنه آيدي قناتك الصحيح (مو آيدي مستخدم)

CUSTOM_PERFORMER = "صدى الحسين"
CUSTOM_THUMB = "IMG_5528.jpeg"  # اختياري: صورة غلاف ثابتة

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
QUEUE_KEY = "pending_audio_queue"
LOCK_KEY = "audio_publish_lock"
DOWNLOAD_DIR = "downloads"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

r = redis.from_url(REDIS_URL, decode_responses=True)  # عميل متزامن، بدون asyncio


def is_audio(e):
    return bool(e.audio) or (e.document and e.document.mime_type and e.document.mime_type.startswith("audio/"))


def get_original_title(e):
    """يستخرج الـ title الأصلي من attributes الملف، أو يستخدم اسم الملف كبديل"""
    if e.audio and e.audio.title:
        return e.audio.title
    if e.document and e.document.attributes:
        for attr in e.document.attributes:
            if hasattr(attr, "file_name") and attr.file_name:
                return os.path.splitext(attr.file_name)[0]
    return "صدى الحسين"


def register_audio_publisher(client, scheduler, hour=13, minute=44):
    """
    يفعّل ميزة استقبال الصوتيات وجدولة نشرها.
    client: كائن TelegramClient جاهز ومتصل (تم استدعاء start عليه مسبقًا)
    scheduler: كائن AsyncIOScheduler جاهز (لا تستدعي scheduler.start() هنا، خليها بالملف الرئيسي)
    hour, minute: وقت النشر اليومي (افتراضيًا 1:44 مساءً للتجربة)
    """

    @client.on(events.NewMessage(from_users=ALLOWED_USERS))
    async def collect(e):
        if not is_audio(e):
            return

        try:
            file_path = await e.download_media(file=DOWNLOAD_DIR)
            original_title = get_original_title(e)
            duration = e.audio.duration if e.audio else 0

            item = {
                "file_path": file_path,
                "duration": duration,
                "title": original_title
            }
            r.rpush(QUEUE_KEY, json.dumps(item))
            print(f"📥 صوتي أُضيف للطابور: {original_title}")

            await e.reply(f"✅ تم استلام الملف الصوتي وإضافته للطابور:\n🎵 {original_title}")

        except Exception as E:
            print(f"⚠️ خطأ أثناء استقبال الملف: {E}")
            await e.reply(f"❌ صار خطأ أثناء استلام الملف: {E}")

    async def publish_queue():
        lock_acquired = r.set(LOCK_KEY, "1", nx=True, ex=600)
        if not lock_acquired:
            print("⏭️ يوجد تنفيذ آخر شغال حاليًا، تم التجاوز")
            return

        try:
            items_raw = r.lrange(QUEUE_KEY, 0, -1)
            if not items_raw:
                print("ℹ️ ما فيه ملفات صوتية بالطابور")
                return

            sent_count = 0
            failed_titles = []

            for raw in items_raw:
                item = json.loads(raw)
                fpath = item["file_path"]

                if not os.path.exists(fpath):
                    print(f"⚠️ الملف غير موجود: {fpath}")
                    failed_titles.append(item.get("title", "?"))
                    continue

                try:
                    await client.send_file(
                        TARGET_CHANNEL,
                        fpath,
                        thumb=CUSTOM_THUMB if os.path.exists(CUSTOM_THUMB) else None,
                        attributes=[
                            DocumentAttributeAudio(
                                duration=item["duration"],
                                title=item["title"],          # يبقى كما هو بالأصل
                                performer=CUSTOM_PERFORMER     # فقط هذا يتغيّر
                            )
                        ],
                        force_document=False
                    )
                    sent_count += 1
                    os.remove(fpath)
                except Exception as E:
                    print(f"⚠️ فشل نشر ملف: {E}")
                    failed_titles.append(item.get("title", "?"))

            r.delete(QUEUE_KEY)
            summary = f"✅ تم نشر {sent_count} ملف صوتي الساعة {datetime.now().strftime('%H:%M')}"
            if failed_titles:
                summary += f"\n⚠️ فشل نشر: {', '.join(failed_titles)}"
            print(summary)

            for uid in ALLOWED_USERS:
                try:
                    await client.send_message(uid, summary)
                except Exception:
                    pass

        finally:
            r.delete(LOCK_KEY)

    scheduler.add_job(publish_queue, CronTrigger(hour=hour, minute=52))
    print(f"🚀 ميزة نشر الصوتيات مفعّلة، موعد النشر: {hour:02d}:{minute:02d}")
