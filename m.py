import os
import json
from datetime import datetime
import redis
from telethon import TelegramClient, events
from telethon.tl.types import DocumentAttributeAudio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

# ============================================================
# 2) منطق استقبال ونشر الملفات الصوتية
# ============================================================
wfffp = 1910015590
target_user_id = 1421907917

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


def get_audio_attribute(e):
    """يبحث عن كائن DocumentAttributeAudio داخل attributes الملف (فيه title و duration الحقيقيين)"""
    if e.document and e.document.attributes:
        for attr in e.document.attributes:
            if isinstance(attr, DocumentAttributeAudio):
                return attr
    return None


def get_original_title(e):
    """يستخرج الـ title الأصلي من attributes الملف، أو يستخدم اسم الملف كبديل"""
    audio_attr = get_audio_attribute(e)
    if audio_attr and audio_attr.title:
        return audio_attr.title
    if e.document and e.document.attributes:
        for attr in e.document.attributes:
            if hasattr(attr, "file_name") and attr.file_name:
                return os.path.splitext(attr.file_name)[0]
    return "صدى الحسين"


def register_audio_publisher(client, scheduler, hour=13, minute=44):
    """
    يفعّل ميزة استقبال الصوتيات وجدولة نشرها.
    client: كائن TelegramClient جاهز ومتصل
    scheduler: كائن AsyncIOScheduler جاهز (لا تستدعي scheduler.start() هنا)
    hour, minute: وقت النشر اليومي
    """

    @client.on(events.NewMessage(from_users=ALLOWED_USERS))
    async def collect(e):
        if not is_audio(e):
            return

        try:
            file_path = await e.download_media(file=DOWNLOAD_DIR)
            original_title = get_original_title(e)
            audio_attr = get_audio_attribute(e)
            duration = audio_attr.duration if audio_attr else 0

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

    scheduler.add_job(publish_queue, CronTrigger(hour=hour, minute=minute))
    print(f"🎧 ميزة نشر الصوتيات مفعّلة، موعد النشر: {hour:02d}:{minute:02d}")


# ============================================================
# 3) تفعيل الميزة فعليًا (يشتغل تلقائيًا بمجرد استيراد هذا الملف)
# ============================================================
scheduler = AsyncIOScheduler(timezone="Asia/Baghdad")
register_audio_publisher(m, scheduler, hour=2, minute=30)


async def _start_scheduler():
    scheduler.start()

bot.loop.run_until_complete(_start_scheduler())

print("🚀 كل شي شغال بملف m.py، جاهز للاستيراد بـ ABH.py")

# ⚠️ ملاحظة مهمة: لا تضيف هنا bot.run_until_disconnected()
# لأن هذا الملف يُستورد داخل ABH.py عبر "from m import *"،
# ولو حطينا هنا استدعاء يوقف وينتظر للأبد، ABH.py ما راح يكمل تشغيل باقي كوده
# (مثل الـ event handlers الخاصة بالمشرفين والتفاعلات وغيرها).
# خلي  بآخر ملف ABH.py أو p.py كما هو موجود عندك حاليًا.
