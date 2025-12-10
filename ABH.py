from telethon.tl.types import ReactionEmoji
from telethon import TelegramClient, events
import random, os,re, asyncio, redis
from telethon.tl.types import (
    ReactionEmoji,
    ChatAdminRights,
)
from telethon.errors import (
    UserAlreadyParticipantError,
)
from telethon.tl.functions.channels import (
    EditAdminRequest,
)
from telethon.tl.functions.messages import (
    ImportChatInviteRequest,
    SendReactionRequest,
    GetMessagesViewsRequest
)
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
wfffp = 1910015590
target_user_id = 1421907917
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("bot_token")
bot_tokens = [os.getenv(f"bot_token{i}") for i in range(6, 17)]
bot = TelegramClient("code", api_id, api_hash).start(bot_token=bot_token)
ABH1 = TelegramClient("code1", int(os.getenv("API_ID1")), os.getenv("API_HASH1")).start()
ABH2 = TelegramClient("code2", int(os.getenv("API_ID2")), os.getenv("API_HASH2")).start()
ABH3 = TelegramClient("code3", int(os.getenv("API_ID3")), os.getenv("API_HASH3")).start()
ABH4 = TelegramClient("code4", int(os.getenv("API_ID4")), os.getenv("API_HASH4")).start()
ABH5 = TelegramClient("code5", int(os.getenv("API_ID5")), os.getenv("API_HASH5")).start()
ABHS = [ABH1, ABH2, ABH3, ABH4, ABH5]
for i, token in enumerate(bot_tokens, start=6):
    if token:
        ABHS.append(TelegramClient(f"code{i}", api_id, api_hash).start(bot_token=token))
idd = ABHS[5:]
client = ABH1
async def promote_ABHS(event, chat_id=None):
    xxx = int(chat_id)
    for AB in idd:
        print(1)
        id_info = await AB.get_me()
        c = await client.get_entity(xxx)  
        print(c)
        print(2)
        rights = ChatAdminRights(
            add_admins=True,
            change_info=True,
            post_messages=True,
            edit_messages=True,
            delete_messages=True
        )
        await client(EditAdminRequest(
            channel=int(xxx),
            user_id=id_info.id,
            admin_rights=rights,
            rank="bot"
        ))
        print(f"✅ تم رفع البوت {id_info.id} مشرف بالقناة بالصلاحيات المناسبة")
def add_chat(chat_id):
    r.sadd("whitelist_chats", str(chat_id))
def remove_chat(chat_id):
    r.srem("whitelist_chats", str(chat_id))
def clear_chats():
    r.delete("whitelist_chats")
def is_chat_allowed(chat_id):
    return str(chat_id) in r.smembers("whitelist_chats")
def list_chats():
    return list(r.smembers("whitelist_chats"))
def add_reactions(chat_id, emojis):
    key = f"chat_reactions:{chat_id}"
    for emoji in emojis:
        r.sadd(key, emoji)
def get_reactions(chat_id):
    key = f"chat_reactions:{chat_id}"
    return list(r.smembers(key))
def get_random_reaction(chat_id):
    reactions = get_reactions(chat_id)
    return random.choice(reactions) if reactions else None
def clear_reactions(chat_id):
    r.delete(f"chat_reactions:{chat_id}")
def remove_reaction(chat_id, emoji):
    r.srem(f"chat_reactions:{chat_id}", emoji)

async def react(event):
    for ABH in ABHS:
        try:
            stored = get_reactions(event.chat_id)
            if stored:
                emoji = random.choice(stored)
            else:
                emoji = random.choice(['❤️', '🕊', '🌚'])
            await asyncio.sleep(3)
            await ABH(
                SendReactionRequest(
                    peer=event.chat_id,
                    msg_id=event.message.id,
                    reaction=[ReactionEmoji(emoticon=emoji)],
                    big=False
                )
            )
            await ABH(
                GetMessagesViewsRequest(
                    peer=event.chat_id,    
                    id=[event.message.id], 
                    increment=True         
                )
            )
        except Exception as ex:
            print(f"⚠️ خطأ أثناء التفاعل في {event.chat_id}: {ex}")
@bot.on(events.NewMessage(pattern='شغال؟', from_users=[wfffp, 201728276]))
async def test(e):
    try:
        for ABH in ABHS:
            await ABH.send_message(e.chat_id, 'نعم', reply_to=e.id)
    except Exception as E:
        x = await ABH.get_me()
        await e.reply(f"{x.id}    {E}")
@bot.on(events.NewMessage(pattern=r"^.?كلمات (\d+)\s+(\d+)$", from_users=[1910015590, 201728276]))
async def words(event):
    num = int(event.pattern_match.group(1)) or 100
    time = int(event.pattern_match.group(2)) or 20
    for ABH in ABHS:
        for _ in range(num):
            async with ABH.conversation(event.chat_id, timeout=10) as conv:
                await conv.send_message("كلمات")
                try:
                    while True:
                        msg = await conv.get_response()
                        if msg.sender_id != target_user_id:
                            continue
                        text = msg.raw_text.strip()
                        match = re.search(r"\(\s*(.+?)\s*\)", text)
                        if match:
                            await asyncio.sleep(time)
                            await conv.send_message(match.group(1))
                        break
                except asyncio.TimeoutError:
                    return
@bot.on(events.NewMessage(pattern=r'^ارسل(?: (.+))?$', from_users=[wfffp]))
async def s(e):
    reply = await e.get_reply_message()
    if not reply:
        return
    num = e.pattern_match.group(1) or str(wfffp)
    for ABH in ABHS:
        try:
            entity = None
            if num.isdigit():
                entity = int(num)
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
            # if entity and isinstance(entity, PeerChannel):
            #     try:
            #         await ABH(JoinChannelRequest(entity))
            #     except UserAlreadyParticipantError:
            #         pass
            print(entity)
            if reply.text and not reply.media:
                await ABH.send_message(entity, reply.text)
            elif reply.media:
                await ABH.send_file(entity, reply.media, caption=reply.text or "")
        except Exception as err:
            await ABH.send_message(f"⚠️ فشل الإرسال من {ABH.session.filename} إلى {num}: {err}")
@bot.on(events.NewMessage)
async def reactauto(e):
    text = e.text.strip()
    sender = e.sender_id
    if text.startswith("اضف") and sender == wfffp:
        try:
            chat_id = text.split(" ", 1)[1]
            add_chat(chat_id)
            await promote_ABHS(e, int(chat_id))
            await e.reply(f"✅ تم إضافة القناة `{chat_id}` إلى القائمة البيضاء")
        except Exception as E:
            await e.reply(f"⚠️ حدث خطأ: {E}")
    elif text.startswith("القنوات") and sender == wfffp:
        chats = list_chats()
        msg = "📌 القنوات في القائمة البيضاء:\n" + "\n".join(chats) if chats else "⚠️ لا توجد قنوات مضافة حالياً"
        await e.reply(msg)
    elif text.startswith("التفاعلات") and sender == wfffp:
        try:
            chat_id = text.split(" ")[1]
            emojis = get_reactions(chat_id)
            if emojis:
                msg = f"📌 التفاعلات المخزنة للقناة `{chat_id}`:\n" + " ".join(emojis)
            else:
                msg = f"⚠️ لا توجد تفاعلات مخزنة للقناة `{chat_id}`"
            await e.reply(msg)
        except IndexError:
            await e.reply("⚠️ استخدم: `تفاعلات -100xxxx`")
        except Exception as ex:
            await e.reply(f"⚠️ خطأ أثناء جلب التفاعلات: {ex}")
    elif text.startswith("تفاعل") and sender == wfffp:
        try:
            parts = text.split()
            chat_id = parts[1]
            emojis = parts[2:]
            if not emojis:
                await e.reply("⚠️ أرسل الإيموجيات بعد المعرف مثل:\n`تفاعل -100xxxx 😂 ❤️ 🔥`")
                return
            existing = get_reactions(chat_id) or []
            updated = existing + emojis
            add_reactions(chat_id, updated)
            await e.reply(f"✅ تم حفظ {len(emojis)} إيموجي جديد للقناة `{chat_id}` (الإجمالي الآن {len(updated)})")
        except Exception as ex:
            await e.reply(f"⚠️ خطأ أثناء حفظ التفاعلات: {ex}")
    elif text.startswith("حذف تفاعل") and sender == wfffp:
        try:
            parts = text.split()
            if len(parts) < 4:
                await e.reply("⚠️ استخدم الصيغة الصحيحة:\n`حذف تفاعل -100xxxx 😂`")
                return
            chat_id = parts[2]
            emoji = parts[3]
            emojis = get_reactions(chat_id)
            if not emojis:
                await e.reply(f"⚠️ لا توجد تفاعلات محفوظة للقناة `{chat_id}`")
                return
            if emoji in emojis:
                emojis = [em for em in emojis if em != emoji]
                add_reactions(chat_id, emojis)
                await e.reply(f"🗑️ تم حذف جميع التكرارات للتفاعل `{emoji}` من القناة `{chat_id}`")
            else:
                await e.reply(f"⚠️ التفاعل `{emoji}` غير موجود في القناة `{chat_id}`")
        except Exception as ex:
            await e.reply(f"⚠️ خطأ أثناء حذف التفاعل: {ex}")
    elif text.startswith("حذف التفاعلات") and sender == wfffp:
        try:
            parts = text.split()
            if len(parts) < 3:
                await e.reply("⚠️ استخدم الصيغة الصحيحة:\n`حذف التفاعلات -100xxxx`")
                return
            chat_id = parts[2]
            key = f"chat_reactions:{chat_id}"
            if r.exists(key):
                r.delete(key)
                await e.reply(f"🗑️ تم حذف جميع التفاعلات المخزنة للقناة `{chat_id}` بنجاح")
            else:
                await e.reply(f"⚠️ لا توجد تفاعلات مخزنة للقناة `{chat_id}`")
        except Exception as ex:
            await e.reply(f"⚠️ خطأ أثناء حذف جميع التفاعلات: {ex}")
    elif text.startswith("حذف الكل") and sender == wfffp:
        clear_chats()
        await e.reply("🗑️ تم حذف جميع القنوات من القائمة البيضاء")
    elif text.startswith("حذف ") and sender == wfffp and not text.startswith("حذف تفاعل") and not text.startswith("حذف التفاعلات"):
        try:
            chat_id = text.split(" ", 1)[1]
            remove_chat(chat_id)
            await e.reply(f"🗑️ تم حذف القناة `{chat_id}` من القائمة البيضاء")
        except IndexError:
            await e.reply("⚠️ استخدم: `حذف -100xxxxxxxxxx`")
    elif is_chat_allowed(e.chat_id):
        try:
            await react(e)
        except Exception as ex:
            print(f"خطأ في التفاعل: {ex}")
print('...')
bot.run_until_disconnected()
