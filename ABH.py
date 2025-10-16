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

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
wfffp = 1910015590
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("bot_token")
bot_token6 = os.getenv("bot_token6")
bot_token7 = os.getenv("bot_token7")
bot_token8 = os.getenv("bot_token8")
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
# ABH = TelegramClient("ABH", api_id, api_hash).start()
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
ABH6 = TelegramClient("code6", api_id, api_hash).start(bot_token=bot_token6)
ABH7 = TelegramClient("code7", api_id, api_hash).start(bot_token=bot_token7)
ABH8 = TelegramClient("code8", api_id, api_hash).start(bot_token=bot_token8)
ABHS = [ABH1, ABH2, ABH3, ABH4, ABH5, ABH6, ABH7, ABH8]
bot_id = [6938881479, 7308514832, 6907915843]
client = ABH1
#@ABH1.on(events.NewMessage(from_users=[wfffp]))
from telethon.tl.functions.channels import EditAdminRequest, GetParticipantsRequest
from telethon.tl.types import ChatAdminRights, Channel
from telethon.tl.types import ChannelParticipantsSearch
from telethon.errors import RightForbiddenError, ChatAdminRequiredError, UserNotParticipantError

async def promote_bot_to_admin(channel):
    print("تم تشغيل الدالة")

    try:
        entity = await ABH1.get_entity(channel)

        if not isinstance(entity, Channel):
            print("❌ هذا الكيان ليس قناة.")
            return

        # حقوق المشرف الآمنة للبوت في قناة بثية
        rights = ChatAdminRights(
            post_messages=True,  # الحد الأدنى المقبول للقناة
            edit_messages=False,
            delete_messages=False,
            add_admins=False,
            manage_call=False
        )

        for bot in bot_id:
            # التأكد من أن البوت عضو في القناة
            try:
                await ABH1.get_participant(entity, bot)
            except UserNotParticipantError:
                print(f"⚠️ البوت {bot} ليس عضوًا بالقناة، يرجى إضافته يدويًا أو عبر رابط دعوة.")
                continue

            # ترقية البوت إلى مشرف
            await ABH1(EditAdminRequest(
                channel=entity,
                user_id=bot,
                admin_rights=rights,
                rank='بوت'
            ))
            print(f"✅ تم رفع البوت {bot} كمشرف بالقناة.")

    except ChatAdminRequiredError:
        print("❌ الحساب ABH1 ليس مشرفًا بصلاحية add_admins في القناة.")
    except RightForbiddenError:
        print("❌ لا يمكن منح هذا المشرف الحقوق المطلوبة في القناة.")
    except Exception as e:
        print(f"❌ حدث خطأ غير متوقع: {e}")
target_user_id = 1421907917
@bot.on(events.NewMessage(pattern='شغال؟', from_users=[wfffp, 201728276]))
async def test(e):
    for ABH in ABHS:
        await ABH.send_message(e.chat_id, 'نعم', reply_to=e.id)
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
async def react(event):
    for ABH in ABHS:
        try:
            emoji = random.choice(['👍', '🕊', '❤️'])
            await ABH.send_reaction(event.chat_id, event.message.id, emoji)
        except Exception as ex:
            await bot.send_message(wfffp, str(ex))
            pass

# -------------------------------------
# رفع البوتات كمشرفين بالقناة
# -------------------------------------
async def promote_ABHS(chat_id):
    if not ABHS:
        print("❌ قائمة ABHS فارغة")
        return
    print("جاري الرفع")
    me = await ABH1.get_me()
    rights = ChatAdminRights(
        add_admins=True
            )
    await bot(EditAdminRequest(
        channel=chat_id,
        user_id=me.id,
        admin_rights=rights,
        rank="مشرف رئيسي"
            ))
    print(f"✅ تم رفع البوت {me.id} مشرف بالقناة")
    await promote_bot_to_admin(chat_id)
# -------------------------------------
# الحدث الأساسي
# -------------------------------------
@bot.on(events.NewMessage(from_users=[wfffp]))
async def reactauto(e):
    text = e.text.strip()

    # إضافة قناة
    if text.startswith("اضف") and e.sender_id == wfffp:
        try:
            chat_id = int(text.split(" ", 1)[1])
            add_chat(chat_id)
            print(".")
            await promote_ABHS(chat_id)
            await e.reply(f"✅ تم إضافة القناة `{chat_id}` إلى القائمة البيضاء")
            
        except IndexError:
            await e.reply("⚠️ استخدم: `اضف -100xxxxxxxxxx`")

    # حذف قناة
    elif text.startswith("حذف") and e.sender_id == wfffp:
        try:
            chat_id = text.split(" ", 1)[1]
            remove_chat(chat_id)
            await e.reply(f"🗑️ تم حذف القناة `{chat_id}` من القائمة البيضاء")
        except IndexError:
            await e.reply("⚠️ استخدم: `حذف -100xxxxxxxxxx`")

    # عرض القنوات
    elif text.startswith("قنوات") and e.sender_id == wfffp:
        chats = list_chats()
        if chats:
            await e.reply("📌 القنوات في القائمة البيضاء:\n" + "\n".join(chats))
        else:
            await e.reply("⚠️ لا توجد قنوات مضافة حالياً")

    # ردود الفعل للقنوات فقط
    elif is_chat_allowed(e.chat_id):
        entity = await bot.get_entity(e.chat_id)
        if isinstance(entity, Channel) and not getattr(entity, 'megagroup', False):
            await react(e)
            print(f"✅ تمت إضافة رد فعل في القناة {e.chat_id}")
        else:
            print(f"⚠️ {e.chat_id} ليس قناة صالحة، تم تخطي العملية")

bot.run_until_disconnected()
