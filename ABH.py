import random
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.messages import SendReactionRequest
from telethon.errors import UserAlreadyParticipantError
from telethon.tl.types import ReactionEmoji
from telethon import events, TelegramClient
from telethon.tl.types import PeerChannel
import os, random
wfffp = 1910015590
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("bot_token")
ABH = TelegramClient("ABH", api_id, api_hash).start()
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
@bot.on(events.NewMessage(pattern=r'^ارسل(?: (\S+))?$', from_users=wfffp))
async def s(e):
    reply = await e.get_reply_message()
    if not reply:
        return
    num = e.pattern_match.group(1) or str(wfffp)
    for ABH in ABHS:
        try:
            entity = None
            if num.isdigit():
                chat_id = int(num)
                if str(num).startswith("-100"):
                    entity = PeerChannel(chat_id)
                else:
                    entity = await ABH.get_entity(chat_id)
            else:
                try:
                    entity = await ABH.get_entity(num)
                except ValueError:
                    if "t.me/+" in num or "joinchat" in num:
                        invite = num.split("/")[-1].replace("+", "")
                        try:
                            entity = await ABH(ImportChatInviteRequest(invite))
                        except UserAlreadyParticipantError:
                            entity = await ABH.get_entity(num)
            if entity and isinstance(entity, PeerChannel):
                try:
                    await ABH(JoinChannelRequest(entity))
                except UserAlreadyParticipantError:
                    pass
            if reply.text and not reply.media:
                await ABH.send_message(entity, reply.text)
            elif reply.media:
                await ABH.send_file(entity, reply.media, caption=reply.text or "")
        except Exception as err:
            print(f"⚠️ فشل الإرسال من {ABH.session.filename} إلى {num}: {err}")
async def react(event):
    for ABH in ABHS:
        x = random.choice(['👍', '🤣', '😁'])
        await ABH(SendReactionRequest(
            peer=event.chat_id,
            msg_id=event.id,
            reaction=[ReactionEmoji(emoticon=f'{x}')],
            big=True
        ))
@bot.on(events.NewMessage)
async def reactaotu(e):
    if e.chat_id == -1002398894610:
        for ABH in ABHS:
            await react(e)
print("✅ البوت والحسابات الإضافية اشتغلوا")
bot.run_until_disconnected()
