from telethon import events, TelegramClient
from telethon.tl.types import PeerUser
import os
wfffp = 1910015590
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("bot_token")
bot = TelegramClient("code", api_id, api_hash).start(bot_token=bot_token)
api_id1 = int(os.getenv("API_ID1"))
api_hash1 = os.getenv("API_HASH1")
ABH1 = TelegramClient("code1", api_id1, api_hash1).start()
api_id2 = int(os.getenv("API_ID2"))
api_hash2 = os.getenv("API_HASH2")
ABH2 = TelegramClient("code2", api_id2, api_hash2).start()
api_id3 = int(os.getenv("API_ID3"))
api_hash3 = os.getenv("API_HASH3")
ABH3 = TelegramClient("code3", api_id3, api_hash3).start()
api_id4 = int(os.getenv("API_ID4"))
api_hash4 = os.getenv("API_HASH4")
ABH4 = TelegramClient("code4", api_id4, api_hash4).start()
api_id5 = int(os.getenv("API_ID5"))
api_hash5 = os.getenv("API_HASH5")
ABH5 = TelegramClient("code5", api_id5, api_hash5).start()
ABHS = [ABH1, ABH2, ABH3, ABH4, ABH5]
@bot.on(events.NewMessage(pattern='^ارسل$', from_users=wfffp))
async def s(e):
    if e.is_private:
        for ABH in ABHS:
            try:
                user = await ABH.get_input_entity(wfffp)
                await ABH.send_message(user, "ها")
            except ValueError:
                print(f"❌ {ABH.session.filename} لم يجد المستخدم، يحتاج التفاعل أولًا.")
bot.run_until_disconnected()
