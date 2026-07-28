import os
import json
import asyncio
import redis.asyncio as aioredis  # استخدام aioredis لتجنب إعاقة الـ Async Event Loop
from datetime import datetime, timedelta
from telethon import TelegramClient, events
from telethon.tl.types import DocumentAttributeAudio

# ============================================================
# 1) الإعدادات والمتغيرات الأساسية
# ============================================================
wfffp = 1910015590
target_user_id = 1421907917

ALLOWED_USERS = [wfffp, 6520830528]
TARGET_CHANNEL = wfffp  # آيدي القناة

CUSTOM_PERFORMER = "صدى الحسين"
CUSTOM_THUMB = "IMG_5528.jpeg"

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
QUEUE_KEY = "pending_audio_queue"
LOCK_KEY = "audio_publish_lock"
DOWNLOAD_DIR = "downloads"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

m = TelegramClient("m", api_id, api_hash).start(bot_token=os.getenv("m"))
r = aioredis.from_url(REDIS_URL, decode_responses=True)  # Async Redis client


# ============================================================
# 2) الدوال المساعدة
# ============================================================
def is_audio(e):
    return bool(e.audio) or (e.document and e.document.mime_type and e.document.mime_type.startswith("audio/"))


def get_audio_attribute(e):
    if e.document and e.document.attributes:
        for attr in e.document.attributes:
            if isinstance(attr, DocumentAttributeAudio):
                return attr
    return None


def get_original_title(e):
    audio_attr = get_audio_attribute(e)
    if audio_attr and audio_attr.title:
        return audio_attr.title
    if e.document and e.document.attributes:
        for attr in e.document.attributes:
            if hasattr(attr, "file_name") and attr.file_name:
                return os.path.splitext(attr.file_name)[0]
    return "صدى الحسين"


# ============================================================
# 3) منطق استقبال ونشر الملفات ومهمة الجدولة (Custom Loop)
# ============================================================
def register_audio_publisher(client, hour=4, minute=51):
    """
    تفعيل ميزة الاستقبال والجدولة عبر asyncio loop بديل لـ APScheduler.
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
            await r.rpush(QUEUE_KEY, json.dumps(item))
            print(f"📥 صوتي أُضيف للطابور: {original_title}")

            await e.reply(f"✅ تم استلام الملف الصوتي وإضافته للطابور:\n🎵 {original_title}")

        except Exception as E:
            print(f"⚠️ خطأ أثناء استقبال الملف: {E}")
            await e.reply(f"❌ صار خطأ أثناء استلام الملف: {E}")

    async def publish_queue():
        lock_acquired = await r.set(LOCK_KEY, "1", nx=True, ex=600)
        if not lock_acquired:
            print("⏭️ يوجد تنفيذ آخر شغال حاليًا، تم التجاوز")
            return

        try:
            items_raw = await r.lrange(QUEUE_KEY, 0, -1)
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
                                title=item["title"],
                                performer=CUSTOM_PERFORMER
                            )
                        ],
                        force_document=False
                    )
                    sent_count += 1
                    os.remove(fpath)
                except Exception as E:
                    print(f"⚠️ فشل نشر ملف: {E}")
                    failed_titles.append(item.get("title", "?"))

            await r.delete(QUEUE_KEY)
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
            await r.delete(LOCK_KEY)

    async def schedule_loop():
        """تاسك يعمل في الخلفية يحسب الوقت المتبقي لموعد النشر المنسق وينتظره"""
        while True:
            now = datetime.now()
            target_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            # إذا عبر الوقت اليوم، نصبه على يوم غد
            if now >= target_time:
                target_time += timedelta(days=1)

            sleep_seconds = (target_time - now).total_seconds()
            print(f"⏳ الموعد القادم للنشر خلال {int(sleep_seconds // 3600)} ساعة و {int((sleep_seconds % 3600) // 60)} دقيقة.")
            
            await asyncio.sleep(sleep_seconds)
            await publish_queue()

    # تشغيل التاسك بالـ loop الخاص بالبوات
    m.loop.create_task(schedule_loop())
    print(f"🎧 ميزة نشر الصوتيات مفعّلة عبر asyncio task، موعد النشر: {hour:02d}:{minute:02d}")


# ============================================================
# 4) التشغيل
# ============================================================
register_audio_publisher(m, hour=4, minute=51)

print("🚀 كل شي شغال بملف m.py ومستعد للاستيراد بـ ABH.py")
