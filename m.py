import os
import json
import asyncio
from datetime import datetime, timedelta
import redis.asyncio as aioredis
from telethon import TelegramClient, events
from telethon.tl.types import DocumentAttributeAudio

# ============================================================
# 1) الإعدادات
# ============================================================
ALLOWED_USERS = [1910015590, 6520830528]
TARGET_CHANNEL = -1002980874985

CUSTOM_PERFORMER = "صدى الحسين"
CUSTOM_THUMB = "IMG_5528.jpeg"

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
QUEUE_KEY = "pending_audio_queue"
LOCK_KEY = "audio_publish_lock"
DOWNLOAD_DIR = "downloads"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("m", "")


# ============================================================
# 2) كلاس إدارة الصوتيات والنشر المجدول
# ============================================================
class AudioPublisher:
    def __init__(self, client: TelegramClient, publish_hour=4, publish_minute=51):
        self.client = client
        self.hour = publish_hour
        self.minute = publish_minute
        self.redis = aioredis.from_url(REDIS_URL, decode_responses=True)

    def register_handlers(self):
        """تسجيل مستمع الرسائل الصوتية وتفعيل مهمة الخلفية"""
        
        @self.client.on(events.NewMessage(from_users=ALLOWED_USERS))
        async def collect_audio_handler(e):
            if not self._is_audio(e):
                return

            try:
                file_path = await e.download_media(file=DOWNLOAD_DIR)
                title = self._get_original_title(e)
                audio_attr = self._get_audio_attribute(e)
                duration = audio_attr.duration if audio_attr else 0

                item = {
                    "file_path": file_path,
                    "duration": duration,
                    "title": title
                }
                await self.redis.rpush(QUEUE_KEY, json.dumps(item))
                print(f"📥 صوتي أُضيف للطابور: {title}")
                await e.reply(f"✅ تم استلام الملف الصوتي وإضافته للطابور:\n🎵 {title}")

            except Exception as ex:
                print(f"⚠️ خطأ أثناء استقبال الملف: {ex}")
                await e.reply(f"❌ صار خطأ أثناء استلام الملف: {ex}")

        # جدولة Task الخلفية عند توفر الـ Loop
        self.client.loop.create_task(self._schedule_loop())
        print(f"🎧 ميزة نشر الصوتيات مفعّلة | موعد النشر اليومي: {self.hour:02d}:{self.minute:02d}")

    async def publish_queue(self):
        """منطق قراءة طابور Redis ونشره في القناة"""
        lock = await self.redis.set(LOCK_KEY, "1", nx=True, ex=600)
        if not lock:
            print("⏭️ يوجد تنفيذ آخر شغال حاليًا، تم التجاوز")
            return

        try:
            items_raw = await self.redis.lrange(QUEUE_KEY, 0, -1)
            if not items_raw:
                print("ℹ️ لا توجد ملفات صوتية في الطابور")
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
                    await self.client.send_file(
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
                except Exception as ex:
                    print(f"⚠️ فشل نشر ملف: {ex}")
                    failed_titles.append(item.get("title", "?"))

            await self.redis.delete(QUEUE_KEY)
            
            summary = f"✅ تم نشر {sent_count} ملف صوتي الساعة {datetime.now().strftime('%H:%M')}"
            if failed_titles:
                summary += f"\n⚠️ فشل نشر: {', '.join(failed_titles)}"
            print(summary)

            for uid in ALLOWED_USERS:
                try:
                    await self.client.send_message(uid, summary)
                except Exception:
                    pass

        finally:
            await self.redis.delete(LOCK_KEY)

    async def _schedule_loop(self):
        """Loop لحساب الانتظار حتى الموعد المحدد"""
        while True:
            now = datetime.now()
            target_time = now.replace(hour=self.hour, minute=self.minute, second=0, microsecond=0)

            if now >= target_time:
                target_time += timedelta(days=1)

            sleep_seconds = (target_time - now).total_seconds()
            hours, remainder = divmod(sleep_seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            
            print(f"⏳ موعد النشر القادم بعد: {int(hours)} ساعة و {int(minutes)} دقيقة.")

            await asyncio.sleep(sleep_seconds)
            await self.publish_queue()

    # --- Helpers ---
    @staticmethod
    def _is_audio(e):
        return bool(e.audio) or (e.document and e.document.mime_type and e.document.mime_type.startswith("audio/"))

    @staticmethod
    def _get_audio_attribute(e):
        if e.document and e.document.attributes:
            for attr in e.document.attributes:
                if isinstance(attr, DocumentAttributeAudio):
                    return attr
        return None

    def _get_original_title(self, e):
        audio_attr = self._get_audio_attribute(e)
        if audio_attr and audio_attr.title:
            return audio_attr.title
        if e.document and e.document.attributes:
            for attr in e.document.attributes:
                if hasattr(attr, "file_name") and attr.file_name:
                    return os.path.splitext(attr.file_name)[0]
        return "صدى الحسين"


# ============================================================
# 3) تهيئة العميل وتصدير الموديل
# ============================================================
m = TelegramClient("m", API_ID, API_HASH)

publisher = AudioPublisher(m, publish_hour=4, publish_minute=51)

# تسجيل الـ Handlers والـ Tasks مباشرة
publisher.register_handlers()

print("🚀 كلاس AudioPublisher جاهز للاستيراد والتشغيل عبر ABH.py")
