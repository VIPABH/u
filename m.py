import os
from datetime import datetime, timedelta
from telethon import TelegramClient, events
from telethon.tl.types import DocumentAttributeAudio

# ============================================================
# 1) الإعدادات
# ============================================================
ALLOWED_USERS = [1910015590, 6520830528]
TARGET_CHANNEL = -1002980874985
PUBLISH_HOUR, PUBLISH_MINUTE = 4, 51

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

m = TelegramClient("m", int(os.getenv("API_ID", 0)), os.getenv("API_HASH", ""))

# ============================================================
# 2) دالة حساب موعد النشر المجدول القادم
# ============================================================
def get_next_schedule_time():
    now = datetime.now()
    target = now.replace(hour=PUBLISH_HOUR, minute=PUBLISH_MINUTE, second=0, microsecond=0)
    if now >= target:
        target += timedelta(days=1)
    return target

# ============================================================
# 3) استقبال الملف وجدولته مباشرة بـ Telethon
# ============================================================
@m.on(events.NewMessage(from_users=ALLOWED_USERS))
async def collect_and_schedule_audio(e):
    # التأكد أن الرسالة تحتوي على ملف صوتي
    if not (e.audio or (e.document and e.document.mime_type and e.document.mime_type.startswith("audio/"))):
        return

    try:
        # تحميل الملف محلياً لإعادة رفعه بالحقوق المطلوبة
        file_path = await e.download_media(file=DOWNLOAD_DIR)

        # استخراج عنوان الصوت ومدته
        title = "صدى الحسين"
        duration = 0
        if e.document and e.document.attributes:
            for attr in e.document.attributes:
                if isinstance(attr, DocumentAttributeAudio):
                    if attr.title:
                        title = attr.title
                    duration = attr.duration or 0
                    break
                elif hasattr(attr, "file_name") and attr.file_name:
                    title = os.path.splitext(attr.file_name)[0]

        # حساب وقت الجدولة القادم (04:51)
        schedule_time = get_next_schedule_time()

        # إرسال الملف مجدولاً مباشرة لقناة تلجرام
        await m.send_file(
            TARGET_CHANNEL,
            file_path,
            schedule=schedule_time,
            attributes=[
                DocumentAttributeAudio(
                    duration=duration,
                    title=title,
                    performer="صدى الحسين"
                )
            ]
        )

        # حذف الملف المحلي فور إرساله لسيرفرات تلجرام
        if os.path.exists(file_path):
            os.remove(file_path)

        time_str = schedule_time.strftime("%Y-%m-%d %H:%M")
        print(f"📅 تم جدولة الملف: {title} | موعد النشر: {time_str}")
        await e.reply(f"✅ تم جدولة نشر الصوت في القناة بنجاح!\n🎵 **{title}**\n📅 موعد النشر: `{time_str}`")

    except Exception as ex:
        print(f"⚠️ خطأ أثناء جدولة الملف: {ex}")
        await e.reply(f"❌ حدث خطأ أثناء جدولة الملف: {ex}")

print(f"🚀 الكود جاهز، سيتم جدولة الصوتيات تلقائياً على موعد: {PUBLISH_HOUR:02d}:{PUBLISH_MINUTE:02d}")

m.run_until_disconnected()
