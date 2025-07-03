from telethon import TelegramClient, events
from telethon.sessions import StringSession
import asyncio, os, json
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
SESSION_FILE = "session.txt"
if os.path.exists(SESSION_FILE):
    with open(SESSION_FILE, "r") as f:
        session_str = f.read().strip()
else:
    session_str = None
ABH = TelegramClient(StringSession(session_str), api_id, api_hash)
@ABH.on(events.NewMessage(pattern=r"^(كود الجلسة|/session)$", outgoing=True))
async def send_session(event):
    session_string = ABH.session.save()
    with open(SESSION_FILE, "w") as f:
        f.write(session_string)
    await ABH.send_message("me", f" Session String:\n`{session_string}`")
    await event.edit(" تم إرسال الجلسة إلى الرسائل المحفوظة")
