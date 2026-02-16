from telethon import TelegramClient, events
import os, re, random, redis, asyncio
from telethon.tl.types import (
    PeerChannel,
    ReactionEmoji,
    ChatAdminRights)
from telethon.errors import (
    UserAlreadyParticipantError)
from telethon.tl.functions.channels import (
    JoinChannelRequest,
    EditAdminRequest)
from telethon.tl.functions.messages import (
    ImportChatInviteRequest)
from telethon.tl.functions.messages import SendReactionRequest, GetMessagesViewsRequest
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
wfffp = 1910015590
target_user_id = 1421907917
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("bot_token")
bot_tokens = [os.getenv(f"bot_token{i}") for i in range(8, 20)]
bot = TelegramClient("code", api_id, api_hash).start(bot_token=bot_token)
ABH1 = TelegramClient("code1", int(os.getenv("API_ID1")), os.getenv("API_HASH1")).start()
ABH2 = TelegramClient("code2", int(os.getenv("API_ID2")), os.getenv("API_HASH2")).start()
ABH3 = TelegramClient("code3", int(os.getenv("API_ID3")), os.getenv("API_HASH3")).start()
ABH4 = TelegramClient("code4", int(os.getenv("API_ID4")), os.getenv("API_HASH4")).start()
ABH5 = TelegramClient("code5", int(os.getenv("API_ID5")), os.getenv("API_HASH5")).start()
ABH6 = TelegramClient("code6", int(os.getenv("API_ID6")), os.getenv("API_HASH6")).start()
ABH7 = TelegramClient("code7", int(os.getenv("API_ID7")), os.getenv("API_HASH7")).start()
ABHS = [ABH1, ABH2, ABH3, ABH4, ABH5, ABH6, ABH7]
for i, token in enumerate(bot_tokens, start=8):
    if token:
        ABHS.append(TelegramClient(f"code{i}", api_id, api_hash).start(bot_token=token))
client = ABH1
idd = ABHS[1:]
from telethon.errors import FloodWaitError
from telethon.tl.types import ChatAdminRights
from telethon.tl.functions.channels import EditAdminRequest
import asyncio

async def promote_ABHS(chat_id=None):
    if not chat_id:
        return
    
    try:
        xxx = int(chat_id)
    except Exception:
        print("❌ chat_id غير صالح")
        return

    rights = ChatAdminRights(
        change_info=True,
        post_messages=True,
        edit_messages=True,
        delete_messages=True
    )

    # for AB in idd:
    for AB in ABHS:
        try:
            id_info = await AB.get_me()

            await ABH1(EditAdminRequest(
                channel=xxx,
                user_id=id_info.id,
                admin_rights=rights,
                rank="bot"
            ))

            print(f"✅ تم رفع {id_info.id} مشرف")

            await asyncio.sleep(0.5)

        except FloodWaitError as e:
            print(f"⏳ FloodWait لمدة {e.seconds} ثانية")
            await asyncio.sleep(e.seconds)

        except Exception as E:
            print(f"⚠️ خطأ مع الحساب {AB.session.filename if hasattr(AB, 'session') else id_info.id}: {E}")
            continue

def remove_non_private_chats():
    chats = r.smembers("whitelist_chats")
    for chat_id in chats:
        chat_id_str = chat_id.decode() if isinstance(chat_id, bytes) else str(chat_id)
        if not chat_id_str.startswith("-100"):
            r.srem("whitelist_chats", chat_id_str)
            print(f"✅ تم حذف {chat_id_str}")
import random
import asyncio
from telethon.errors import FloodWaitError
from telethon.tl.functions.messages import SendReactionRequest, GetMessagesViewsRequest
from telethon.tl.types import ReactionEmoji

async def react(event):

    if not event.message or not event.chat_id:
        return

    stored = get_reactions(event.chat_id)
    default_emojis = ['❤️', '🕊', '🌚']

    for ABH in ABHS:
        try:
            emoji = random.choice(stored) if stored else random.choice(default_emojis)

            # الأفضل جلب entity لتفادي أخطاء peer
            try:
                peer = await ABH.get_input_entity(event.chat_id)
            except Exception:
                peer = event.chat_id

            await ABH(SendReactionRequest(
                peer=peer,
                msg_id=event.message.id,
                reaction=[ReactionEmoji(emoticon=emoji)],
                big=False
            ))

            try:
                await ABH(GetMessagesViewsRequest(
                    peer=peer,
                    id=[event.message.id],
                    increment=True
                ))
            except Exception:
                pass

            await asyncio.sleep(0.4)

        except FloodWaitError as e:
            print(f"⏳ FloodWait {e.seconds}s")
            await asyncio.sleep(e.seconds)

        except Exception as e:
            print(f"⚠️ خطأ مع {ABH.session.filename if hasattr(ABH,'session') else 'account'}: {e}")
            continue

@bot.on(events.NewMessage(pattern='شغال؟', from_users=[wfffp, 201728276]))
async def test(e):
    try:
        for ABH in ABHS:
            await ABH.send_message(e.chat_id, 'نعم', reply_to=e.id)
    except Exception as E:
        x = await ABH.get_me()
        await e.reply(f"{x.id}    {E}")
import asyncio
import random

# قائمة المجموعات
groups = [-1002541767486, -1002522016427, -1002069775937]

@ABH1.on(events.NewMessage(pattern=r"النشر تفعيل", from_users=[1910015590, 201728276]))
async def words(e):
    await e.reply('تدلل حبيبي')
    async def run_task(group_id):
        while True:
            client = random.choice([ABH1, ABH2, ABH3, ABH4, ABH5])
            try:
                async with client.conversation(group_id, timeout=10) as conv:
                    await conv.send_message("كلمات")
                    while True:
                        msg = await conv.get_response()
                        if msg.sender_id != target_user_id:
                            continue
                        text = msg.raw_text.strip()
                        match = re.search(r"\(\s*(.+?)\s*\)", text)
                        if match:
                            await asyncio.sleep(10) 
                            await conv.send_message(match.group(1))
                        break 
            except asyncio.TimeoutError:
                print(f"انتهى الوقت في المجموعة {group_id}، إعادة المحاولة...")
            except Exception as ex:
                print(f"خطأ في المجموعة {group_id}: {ex}")
            await asyncio.sleep(2) 
    tasks = [run_task(g_id) for g_id in groups]
    await asyncio.gather(*tasks)
import re

@bot.on(events.NewMessage(pattern=r'^ارسل(?: (\S+))?(?: (.*))?$', from_users=wfffp))
async def send_to_target(e):
    reply = await e.get_reply_message()
    if not reply:
        return
    
    target = e.pattern_match.group(1)
    extra_arg = e.pattern_match.group(2)
    reply_to_id = None

    # --- منطق الاستخراج الذكي ---
    # إذا كان الـ target نفسه عبارة عن رابط رسالة
    if target and "t.me/" in target:
        # استخراج اليوزر وأيدي الرسالة من الرابط
        # يدعم الروابط العامة والروابط الخاصة t.me/c/xxxx/yyyy
        link_parts = re.search(r't\.me/(?:c/)?([\w+]+)/(\d+)', target)
        if link_parts:
            target = link_parts.group(1)
            reply_to_id = int(link_parts.group(2))
            # إذا كان الرابط خاص (أرقام)، نحوله لصيغة -100
            if target.isdigit():
                target = int(f"-100{target}")

    # إذا كان هناك وسيط ثانٍ (extra_arg) وكان رابطاً
    if extra_arg and "t.me/" in extra_arg:
        link_parts = re.search(r't\.me/(?:c/)?([\w+]+)/(\d+)', extra_arg)
        if link_parts:
            reply_to_id = int(link_parts.group(2))
    elif extra_arg and extra_arg.isdigit():
        reply_to_id = int(extra_arg)
    elif extra_arg and "reply_to=" in extra_arg:
        digits = re.findall(r'\d+', extra_arg)
        if digits: reply_to_id = int(digits[0])

    # إذا لم يتم تحديد target نهائياً
    if not target:
        target = str(wfffp)

    # --- بد السيرفرات ---
    for ABH in ABHS:
        try:
            entity = None
            # تحديد نوع الكيان
            if isinstance(target, int) or (isinstance(target, str) and (target.startswith("-100") or target.replace('-', '').isdigit())):
                try: entity = await ABH.get_entity(int(target))
                except: entity = int(target)
            elif "t.me/+" in str(target) or "joinchat/" in str(target):
                invite_hash = target.split("/")[-1].replace("+", "")
                try: await ABH(ImportChatInviteRequest(invite_hash))
                except: pass
                entity = await ABH.get_entity(target)
            else:
                entity = await ABH.get_entity(target)

            if entity:
                try: await ABH(JoinChannelRequest(entity))
                except: pass
                
                # الإرسال النهائي
                await ABH.send_message(entity, reply, reply_to=reply_to_id)
                
        except Exception as err:
            print(f"Error in {ABH.session.filename}: {err}")
names = {
    'العميل الاول': ABH1,
    'كرت الحظ': ABH2,
    'ابو صالح': ABH3,
    'هاشم محمد': ABH4,
    'سالو': ABH5,
    'salo': ABH5,
    'حسن جداحه': ABH6,
    'حسن جداحة': ABH6,
    'برق الشايب': ABH7,    
}
@ABH1.on(events.NewMessage(from_users=[wfffp, 201728276]))
async def reactauto(e):
    if not e.text:
        return
    text = e.text
    if text in names:
        reply_text = "عيني"
        try:
            await names[text].send_message(
                e.chat_id,
                reply_text,
                reply_to=e.id
            )
        except:
            return
# =========================
# WHITELIST MANAGEMENT
# =========================

def add_chat(chat_id: int):
    r.sadd("whitelist_chats", str(chat_id))

def remove_chat(chat_id: int):
    r.srem("whitelist_chats", str(chat_id))

def clear_chats():
    r.delete("whitelist_chats")

def is_chat_allowed(chat_id: int) -> bool:
    return r.sismember("whitelist_chats", str(chat_id))

def list_chats():
    return [chat.decode() if isinstance(chat, bytes) else chat 
            for chat in r.smembers("whitelist_chats")]
# =========================
# REACTIONS MANAGEMENT
# =========================

def add_reactions(chat_id: int, emojis: list):
    key = f"chat_reactions:{chat_id}"
    for emoji in emojis:
        r.sadd(key, emoji)

def get_reactions(chat_id: int):
    key = f"chat_reactions:{chat_id}"
    data = r.smembers(key)
    return [e.decode() if isinstance(e, bytes) else e for e in data]

def remove_reaction(chat_id: int, emoji: str):
    r.srem(f"chat_reactions:{chat_id}", emoji)

def clear_reactions(chat_id: int):
    r.delete(f"chat_reactions:{chat_id}")

def get_random_reaction(chat_id: int):
    reactions = get_reactions(chat_id)
    return random.choice(reactions) if reactions else None
@bot.on(events.NewMessage)
async def nlits(e):

    if not e.text:
        return

    text = e.text.strip()
    sender = e.sender_id

    # =====================
    # AUTO REACTION SYSTEM
    # =====================
    if is_chat_allowed(e.chat_id):
        try:
            await react(e)
        except Exception as ex:
            print(f"[REACT ERROR] {ex}")
    if text.startswith("اضف") and sender == wfffp:
        parts = text.split()

        if len(parts) < 2:
            await e.reply("❌ استخدم: اضف -100xxxx")
            return

        chat_id = parts[1]

        if not chat_id.startswith("-100"):
            await e.reply("❌ يجب أن يبدأ المعرف بـ -100")
            return

        chat_id = int(chat_id)

        add_chat(chat_id)
        await promote_ABHS(chat_id)

        await e.reply(f"✅ تمت إضافة `{chat_id}` للقائمة البيضاء")
    elif text.startswith("حذف تفاعل") and sender == wfffp:
        parts = text.split()

        if len(parts) < 4:
            await e.reply("❌ استخدم: حذف تفاعل -100xxxx 😂")
            return

        chat_id = int(parts[2])
        emoji = parts[3]

        remove_reaction(chat_id, emoji)

        await e.reply(f"🗑️ تم حذف `{emoji}` من `{chat_id}`")
    elif text == "القنوات" and sender == wfffp:
        chats = list_chats()

        if not chats:
            await e.reply("⚠️ لا توجد قنوات حالياً")
        else:
            msg = "📌 القنوات:\n" + "\n".join(chats)
            await e.reply(msg)

print('running')
bot.run_until_disconnected()
