from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.messages import ExportChatInviteRequest
from telethon.tl.functions.messages import SendReactionRequest
from telethon.errors import UserAlreadyParticipantError
from telethon.errors import ChatAdminRequiredError
from telethon.tl.types import ReactionEmoji
from telethon import events, TelegramClient
from telethon.tl.types import PeerChannel
import os, random, redis, re, asyncio
import random
from telethon.tl.functions.channels import EditAdminRequest
from telethon.tl.types import ChatAdminRights, Channel
from telethon import TelegramClient, events
from telethon.tl.types import Channel, ChatAdminRights
from telethon.errors import ChatAdminRequiredError
from telethon import TelegramClient
from telethon.tl.functions.channels import EditAdminRequest
from telethon.tl.types import ChatAdminRights
from telethon import events
from telethon.tl.functions.channels import EditAdminRequest
from telethon.tl.types import ChatAdminRights, Channel
from telethon.errors import ChatAdminRequiredError
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
wfffp = 1910015590
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("bot_token")
import os
import redis
from telethon import TelegramClient

# تحميل القيم من ملف البيئة (.env)
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("bot_token")

bot_token6 = os.getenv("bot_token6")
bot_token7 = os.getenv("bot_token7")
bot_token8 = os.getenv("bot_token8")
bot_token9 = os.getenv("bot_token9")
bot_token10 = os.getenv("bot_token10")
bot_token11 = os.getenv("bot_token11")
bot_token12 = os.getenv("bot_token12")
bot_token13 = os.getenv("bot_token13")
bot_token14 = os.getenv("bot_token14")
bot_token15 = os.getenv("bot_token15")
bot_token16 = os.getenv("bot_token16")

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# إنشاء الكلاينت الرئيسي (البوت الأساسي)
bot = TelegramClient("code", api_id, api_hash).start(bot_token=bot_token)

# حسابات إضافية (بدون بوت توكن)
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

# البوتات (المستندة إلى توكنات)
ABH6 = TelegramClient("code6", api_id, api_hash).start(bot_token=bot_token6)
ABH7 = TelegramClient("code7", api_id, api_hash).start(bot_token=bot_token7)
ABH8 = TelegramClient("code8", api_id, api_hash).start(bot_token=bot_token8)
ABH9 = TelegramClient("code9", api_id, api_hash).start(bot_token=bot_token9)
ABH10 = TelegramClient("code10", api_id, api_hash).start(bot_token=bot_token10)
ABH11 = TelegramClient("code11", api_id, api_hash).start(bot_token=bot_token11)
ABH12 = TelegramClient("code12", api_id, api_hash).start(bot_token=bot_token12)
ABH13 = TelegramClient("code13", api_id, api_hash).start(bot_token=bot_token13)
ABH14 = TelegramClient("code14", api_id, api_hash).start(bot_token=bot_token14)
ABH15 = TelegramClient("code15", api_id, api_hash).start(bot_token=bot_token15)
ABH16 = TelegramClient("code16", api_id, api_hash).start(bot_token=bot_token16)

# تجميع جميع الكلاينتات
ABHS = [
    ABH1, ABH2, ABH3, ABH4, ABH5,
    ABH6, ABH7, ABH8, ABH9, ABH10,
    ABH11, ABH12, ABH13, ABH14, ABH15, ABH16
]

# قائمة البوتات فقط
idd = [
    ABH6, ABH7, ABH8, ABH9, ABH10,
    ABH11, ABH12, ABH13, ABH14, ABH15, ABH16
]
client = ABH1
from telethon import events
from telethon.tl.functions.channels import EditAdminRequest
from telethon.tl.types import ChatAdminRights, Channel
from telethon.errors import ChatAdminRequiredError
async def promote_ABHS(event, chat_id=None):
    xxx = int(chat_id)
    for AB in idd:
        id = await AB.get_me()
        rights = ChatAdminRights(
            add_admins=True,
            change_info=True,
            post_messages=True,
            edit_messages=True,
            delete_messages=True
            )
        await ABH1(EditAdminRequest(
            channel=xxx,
            user_id=id.id,  # معرف البوت
            admin_rights=rights,
            rank="bot"
            ))
        print(f"✅ تم رفع البوت 6938881479 مشرف بالقناة بالصلاحيات المناسبة")
        
    #except ChatAdminRequiredError:
        #return
        #print("❌ لا تملك صلاحية تعديل المسؤولين في هذه القناة")
    #except Exception as e:
       # print(f"❌ حدث خطأ: {e}")
#@ABH1.on(events.NewMessage(from_users=[wfffp]))
async def promote_bot_to_admin(event):
    channel = -1002219196756
    bot_username = 6907915843
    
    await client(EditAdminRequest(
        channel=channel,
        user_id=bot_username,
        admin_rights=rights,
    ))
    await client.send_message(-1002219196756, ".")
target_user_id = 1421907917
@bot.on(events.NewMessage(pattern='شغال؟', from_users=[wfffp, 201728276]))
async def test(e):
    try:
        for ABH in ABHS:
            await ABH.send_message(e.chat_id, 'نعم', reply_to=e.id)
    except Exception as E:
        x = await ABH.get_me()
        await e.reply(f"{x.id}    {e}")
@bot.on(events.NewMessage(pattern=r"^.?كلمات (\d+)\s+(\d+)$", from_users=[1910015590, 201728276]))
async def words(event):
    num = int(event.pattern_match.group(1)) or 1
    time = int(event.pattern_match.group(2)) or 1
    for ABH in ABHS:
        for i in range(num):
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
                            text = match.group(1)
                            await asyncio.sleep(time)
                            await conv.send_message(text)
                        break
                except asyncio.TimeoutError:
                    return
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
            await ABH.send_message(f"⚠️ فشل الإرسال من {ABH.session.filename} إلى {num}: {err}")

# إعداد البوتات والحسابات
# bot و ABHS (قائمة الحسابات) مفروض تكون معرفة قبل هذا الجزء

# -------------------------------------
# وظائف إدارة القنوات البيضاء
# -------------------------------------
def add_chat(chat_id):
    r.sadd("whitelist_chats", str(chat_id))

def remove_chat(chat_id):
    r.srem("whitelist_chats", str(chat_id))

def is_chat_allowed(chat_id):
    return str(chat_id) in r.smembers("whitelist_chats")

def list_chats():
    return list(r.smembers("whitelist_chats"))

# -------------------------------------
# ردود الفعل التلقائية
# -------------------------------------

# -------------------------------------
# رفع البوتات كمشرفين بالقناة
# -------------------------------------
async def promote__ABHS(chat_id):
    if not ABHS:
        print("❌ قائمة ABHS فارغة")
        return

    try:
        channel_entity = await bot.get_input_entity(int(chat_id))
    except Exception as e:
        print(f"❌ فشل الحصول على كيان {chat_id} بواسطة البوت الأساسي: {e}")
        return

    # رفع كل البوتات
    for ABH in ABHS:
        try:
            me = await ABH.get_me()
            if not me.bot:
                print(f"⚠️ تخطي الحساب {me.id} لأنه مستخدم عادي")
                continue
            rights = ChatAdminRights(
                add_admins=True,
                change_info=True
                
            )
            await bot(EditAdminRequest(
                channel=channel_entity,
                user_id=me.id,
                admin_rights=rights,
                rank="مشرف رئيسي"
            ))
            print(f"✅ تم رفع البوت {me.id} مشرف بالقناة")
        except Exception as e:
            print(f"❌ خطأ أثناء رفع البوت {me.id}: {e}")
    print("done")
# -------------------------------------
# الحدث الأساسي
# -------------------------------------
import random
from telethon import events
from telethon.tl.functions.messages import SendReactionRequest
from telethon.tl.types import ReactionEmoji

# ======== دوال القنوات ========
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

# ======== دوال التفاعلات ========
def add_reactions(chat_id, emojis):
    key = f"chat_reactions:{chat_id}"
    for emoji in emojis:
        r.sadd(key, emoji)

def get_reactions(chat_id):
    key = f"chat_reactions:{chat_id}"
    return list(r.smembers(key))

def get_random_reaction(chat_id):
    reactions = get_reactions(chat_id)
    if reactions:
        return random.choice(reactions)
    return None

def clear_reactions(chat_id):
    key = f"chat_reactions:{chat_id}"
    r.delete(key)

def remove_reaction(chat_id, emoji):
    key = f"chat_reactions:{chat_id}"
    r.srem(key, emoji)

# ======== دالة التفاعل ========
async def react(event):
    for ABH in ABHS:
        try:
            # استخدام التفاعلات المخزونة فقط
            stored = get_reactions(event.chat_id)
            if stored:
                x = random.choice(stored)
            else:
                continue  # إذا ماكو مخزون ما يسوي أي تفاعل

            await ABH(
                SendReactionRequest(
                    peer=int(event.chat_id),
                    msg_id=int(event.message.id),
                    reaction=[ReactionEmoji(emoticon=f'{x}')],
                    big=True
                )
            )

        except Exception as ex:
            # إعادة محاولة باستخدام المخزون فقط
            stored = get_reactions(event.chat_id)
            if stored:
                try:
                    x = random.choice(stored)
                    await ABH(
                        SendReactionRequest(
                            peer=int(event.chat_id),
                            msg_id=int(event.message.id),
                            reaction=[ReactionEmoji(emoticon=f'{x}')],
                            big=True
                        )
                    )
                except Exception as ex2:
                    await bot.send_message(wfffp, str(ex2))
            else:
                await bot.send_message(wfffp, f"❌ لا توجد تفاعلات مخزونة لهذه القناة: {event.chat_id}\n{ex}")
            pass

# ======== الحدث الرئيسي ========
@bot.on(events.NewMessage)
async def reactauto(e):
    text = e.text.strip()
    sender = e.sender_id

    # إضافة قناة
    if text.startswith("اضف") and sender == wfffp:
        try:
            chat_id = text.split(" ", 1)[1]
            add_chat(chat_id)
            await promote_ABHS(e, chat_id)
            await e.reply(f"✅ تم إضافة القناة `{chat_id}` إلى القائمة البيضاء")
        except Exception as E:
            await e.reply(f"⚠️ حدث خطأ: {E}")


    # عرض القنوات
    elif text.startswith("قنوات") and sender == wfffp:
        chats = list_chats()
        if chats:
            await e.reply("📌 القنوات في القائمة البيضاء:\n" + "\n".join(chats))
        else:
            await e.reply("⚠️ لا توجد قنوات مضافة حالياً")
    elif text.startswith("تفاعلات") and sender == wfffp:
        try:
            chat_id = text.split(" ")[1]
            emojis = get_reactions(chat_id)
            if emojis:
                await e.reply(f"📌 التفاعلات المخزنة للقناة `{chat_id}`:\n" + " ".join(emojis))
            else:
                await e.reply(f"⚠️ لا توجد تفاعلات مخزنة للقناة `{chat_id}`")
        except IndexError:
            await e.reply("⚠️ استخدم: `تفاعلات -100xxxx`")
        except Exception as ex:
            await e.reply(f"⚠️ خطأ أثناء جلب التفاعلات: {ex}")

    # إضافة تفاعلات للقناة
    elif text.startswith("تفاعل") and sender == wfffp:
        try:
            parts = text.split(" ")
            chat_id = parts[1]
            emojis = parts[2:]
            if not emojis:
                await e.reply("⚠️ أرسل الإيموجيات بعد المعرف مثل:\n`تفاعل -100xxxx 😂 ❤️ 🔥`")
                return
            add_reactions(chat_id, emojis)
            await e.reply(f"✅ تم حفظ {len(emojis)} إيموجي للقناة `{chat_id}`")
        except Exception as ex:
            await e.reply(f"⚠️ خطأ أثناء حفظ التفاعلات: {ex}")

    # عرض التفاعلات المخزنة

    # حذف تفاعل واحد
    elif text.startswith("حذف تفاعل") and sender == wfffp:
        try:
            parts = text.split(" ")
            chat_id = parts[1]
            emoji = parts[2]
            remove_reaction(chat_id, emoji)
            await e.reply(f"🗑️ تم حذف التفاعل `{emoji}` من القناة `{chat_id}`")
        except IndexError:
            await e.reply("⚠️ استخدم: `حذف_تفاعل -100xxxx 😂`")
        except Exception as ex:
            await e.reply(f"⚠️ خطأ أثناء حذف التفاعل: {ex}")

    #     # حذف الكل
    elif text.startswith("حذف الكل") and sender == wfffp:
        clear_chats()
        await e.reply("🗑️ تم حذف جميع القنوات من القائمة البيضاء")

    # حذف قناة واحدة
    elif text.startswith("حذف ") and sender == wfffp:
        try:
            chat_id = text.split(" ", 1)[1]
            remove_chat(chat_id)
            await e.reply(f"🗑️ تم حذف القناة `{chat_id}` من القائمة البيضاء")
        except IndexError:
            await e.reply("⚠️ استخدم: `حذف -100xxxxxxxxxx`")

    # ردود الفعل للقنوات المسموح بها فقط
    elif is_chat_allowed(e.chat_id):
        try:
            await react(e)
        except Exception as ex:
            print(f"خطأ في التفاعل: {ex}")

# تشغيل البوت
bot.run_until_disconnected()

