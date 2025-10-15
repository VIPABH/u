import os, re, asyncio, random, redis
from telethon import events, TelegramClient
from telethon.errors import (
    UserAlreadyParticipantError, ChatAdminRequiredError
)
from telethon.tl.types import (
    ChatAdminRights, Channel, Chat, PeerChannel, ReactionEmoji
)
from telethon.tl.functions.channels import (
    JoinChannelRequest, EditAdminRequest, GetParticipantRequest
)
from telethon.tl.functions.messages import (
    ImportChatInviteRequest, ExportChatInviteRequest, EditChatAdminRequest, SendReactionRequest
)

# إعداد Redis
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
OWNER_ID = 1910015590
target_user_id = 1421907917
wfffp = 1910015590
# تحميل المتغيرات
from telethon import TelegramClient
import os

# القيم من المتغيرات البيئية
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("bot_token")
bot_token6 = os.getenv("bot_token6")
bot_token7 = os.getenv("bot_token7")
bot_token8 = os.getenv("bot_token8")

# عملاء المستخدم (حسابات عادية)
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

# عملاء البوتات
bot = TelegramClient("code", api_id, api_hash).start(bot_token=bot_token)
ABH6 = TelegramClient("code6", api_id, api_hash).start(bot_token=bot_token6)
ABH7 = TelegramClient("code7", api_id, api_hash).start(bot_token=bot_token7)
ABH8 = TelegramClient("code8", api_id, api_hash).start(bot_token=bot_token8)

# تجميع كل العملاء في قائمة واحدة
ABHS = [ABH1, ABH2, ABH3, ABH4, ABH5, ABH6, ABH7, ABH8]

print("✅ تم تشغيل جميع العملاء بنجاح")
ABHS = [ABH1, ABH2, ABH3, ABH4, ABH5, ABH6, ABH7, ABH8]

# دوال القائمة البيضاء
def add_chat(chat_id): r.sadd("whitelist_chats", str(chat_id))
def remove_chat(chat_id): r.srem("whitelist_chats", str(chat_id))
def is_chat_allowed(chat_id): return str(chat_id) in r.smembers("whitelist_chats")


# 🔹 دالة التفاعل التلقائي
async def react(event):
    for ABH in ABHS:
        try:
            emoji = random.choice(['👍', '❤️', '🔥'])
            await ABH(SendReactionRequest(
                event.chat_id, msg_id=event.id,
                reaction=[ReactionEmoji(emoticon=emoji)], big=True
            ))
        except Exception as ex:
            await bot.send_message(OWNER_ID, f"⚠️ خطأ تفاعل: {ex}")


# 🔹 دالة إنشاء رابط دعوة
async def get_invite_link(chat_id):
    try:
        entity = await bot.get_entity(chat_id)
        result = await bot(ExportChatInviteRequest(entity))
        return result.link
    except ChatAdminRequiredError:
        print("⚠️ البوت ليس مشرفًا، لا يمكن استخراج رابط الدعوة")
        return None
    except Exception as ex:
        print(f"❌ خطأ أثناء جلب رابط الدعوة: {ex}")
        return None


# 🔹 دالة التحقق من العضوية
async def is_member(client, chat_id, user_id):
    try:
        entity = await client.get_input_entity(chat_id)
        await client(GetParticipantRequest(channel=entity, participant=user_id))
        return True
    except Exception:
        return False


# 🔹 دالة التأكد من الانضمام
async def ensure_joined(client, chat_id):
    me = await client.get_me()
    if await is_member(client, chat_id, me.id):
        return True
    link = await get_invite_link(chat_id)
    if not link:
        return False
    try:
        invite_hash = link.split("/")[-1].replace("+", "")
        await client(ImportChatInviteRequest(invite_hash))
        print(f"✅ {me.id} انضم إلى {chat_id}")
        return True
    except UserAlreadyParticipantError:
        return True
    except Exception as ex:
        print(f"⚠️ فشل الانضمام {me.id}: {ex}")
        return False


# 🔹 دالة رفع الحسابات
async def promote_ABHS(chat_identifier):
    if not ABHS:
        print("❌ قائمة ABHS فارغة")
        return

    ABH1 = ABHS[0]
    try:
        entity = await bot.get_entity(int(chat_identifier))
    except Exception as e:
        print(f"❌ فشل الحصول على الكيان: {e}")
        return

    is_supergroup = isinstance(entity, Channel) and getattr(entity, 'megagroup', False)
    is_channel = isinstance(entity, Channel) and not getattr(entity, 'megagroup', False)
    is_basic_group = isinstance(entity, Chat)

    print(f"🔹 نوع الشات: {'Supergroup' if is_supergroup else 'Channel' if is_channel else 'Basic Group'}")

    try:
        me1 = await ABH1.get_me()
        rights = ChatAdminRights(add_admins=True)
        if is_basic_group:
            await bot(EditChatAdminRequest(chat_id=chat_identifier, user_id=me1.id, is_admin=True))
        else:
            await bot(EditAdminRequest(channel=entity, user_id=me1.id, admin_rights=rights, rank="مشرف رئيسي"))
        print(f"✅ تم رفع ABH1 ({me1.id}) في الشات بنجاح")
    except Exception as e:
        print(f"❌ فشل رفع ABH1: {e}")
        return

    for ABH in ABHS[1:]:
        try:
            me = await ABH.get_me()
            if not me.bot:
                print(f"⚠️ تخطي الحساب {me.id} لأنه مستخدم عادي")
                continue
            await ensure_joined(ABH, chat_identifier)
            if is_basic_group:
                await ABH1(EditChatAdminRequest(chat_id=chat_identifier, user_id=me.id, is_admin=True))
            else:
                await ABH1(EditAdminRequest(channel=entity, user_id=me.id, admin_rights=rights, rank="مشرف"))
            print(f"✅ تم رفع البوت {me.id} بنجاح")
        except Exception as e:
            print(f"❌ خطأ مع الحساب {me.id}: {e}")

    await asyncio.sleep(2)


# 🔹 الأوامر الرئيسية
@bot.on(events.NewMessage(from_users=[OWNER_ID]))
async def control(e):
    text = e.text.strip()
    if text.startswith("اضف"):
        try:
            chat_id = text.split(" ", 1)[1]
            add_chat(chat_id)
            await promote_ABHS(chat_id)
            await e.reply(f"✅ تم إضافة المجموعة `{chat_id}` ورفع الحسابات.")
        except IndexError:
            await e.reply("⚠️ استخدم: `اضف -100xxxxxxxxx`")
    elif text.startswith("حذف"):
        try:
            chat_id = text.split(" ", 1)[1]
            remove_chat(chat_id)
            await e.reply(f"🗑️ تم حذف `{chat_id}` من القائمة البيضاء.")
        except IndexError:
            await e.reply("⚠️ استخدم: `حذف -100xxxxxxxxx`")
    elif is_chat_allowed(e.chat_id):
        await react(e)


print("🚀 النظام بدأ بنجاح")



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
def add_chat(chat_id):
    r.sadd("whitelist_chats", str(chat_id))
def remove_chat(chat_id):
    r.srem("whitelist_chats", str(chat_id))
def is_chat_allowed(chat_id):
    return str(chat_id) in r.smembers("whitelist_chats")
async def react(event):
    for ABH in ABHS:
        try:
            x = random.choice(['👍', '🕊', '❤️'])
            #await ensure_joined(event)
            await ABH(
                SendReactionRequest(
                    event.chat_id,
                    msg_id=int(event.message.id),
                    reaction=[ReactionEmoji(emoticon=f'{x}')],
                    big=True
                )
            )
            #await ABH.send_read_acknowledge(event.chat_id, int(event.message.id))
        except Exception as ex:
            await bot.send_message(wfffp, str(ex))
            pass
async def get_invite_link(chat):
    try:
        entity = await ABH.get_entity(chat)
        try:
            result = await bot(ExportChatInviteRequest(entity))
            invite_link = result.link
            
            return invite_link
        except ChatAdminRequiredError:
            print("الحساب ليس مشرفًا، لا يمكن استخراج رابط الدعوة")
            return None
    except Exception as ex:
        print(f"خطأ أثناء جلب الكيان: {ex}")
        return None
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import InputChannel
from telethon.errors import UserAlreadyParticipantError, ChatAdminRequiredError
from telethon.tl.functions.messages import ImportChatInviteRequest

async def is_member(ABH, chat_id, user_id):
    """
    يتحقق إذا كان الحساب عضو في المجموعة
    """
    try:
        # إذا كان chat_id int، حوله إلى InputChannel
        entity = await ABH.get_input_entity(chat_id)
        await ABH(GetParticipantRequest(channel=entity, user_id=user_id))
        return True
    except Exception:
        return False

async def ensure_joined(event):
    """
    يضيف الحساب إذا لم يكن عضوًا، وإذا فشل يحاول رفعه مشرفًا.
    """
    chat_id = event.chat_id
    try:
        me = await ABH.get_me()
        member = await is_member(ABH, chat_id, me.id)

        if member:
            return

        invite_link = await get_invite_link(bot, chat_id)
        if invite_link:
            invite_hash = invite_link.split("/")[-1].replace("+", "")
            try:
                await ABH(ImportChatInviteRequest(invite_hash))
                print(f"✅ الحساب {me.id} انضم إلى {chat_id} عبر الرابط")
            except UserAlreadyParticipantError:
                pass
            except Exception:
                try:
                    invite_link = await get_invite_link(chat_id)
                    invite_hash = invite_link.split("/")[-1].replace("+", "")
                    await ABH(ImportChatInviteRequest(invite_hash))
                except Exception:
                    try:
                        await bot.edit_admin(
                            chat_id,
                            me.id,
                            title="مشرف احتياطي",
                            invite_users=True,
                            change_info=False,
                            ban_users=False,
                            delete_messages=False,
                            pin_messages=False,
                            manage_call=False
                        )
                        print(f"✅ تم رفع الحساب {me.id} مشرفاً في {chat_id} بعد فشل الانضمام")
                    except Exception as promote_ex:
                        print(f"❌ فشل رفع الحساب {me.id} مشرفاً: {promote_ex}")
        else:
            print(f"❌ لا يوجد رابط دعوة متاح لـ {chat_id}")

    except Exception as ex:
        print(f"❌ حدث خطأ أثناء تنفيذ العملية للحساب {me.id}: {ex}")

client = bot

import asyncio
from telethon.tl.functions.channels import EditAdminRequest, GetParticipantRequest
from telethon.tl.functions.messages import EditChatAdminRequest
from telethon.tl.types import ChatAdminRights, Channel, Chat

async def promote_ABHS(chat_identifier):
    if not ABHS:
        print("❌ قائمة ABHS فارغة")
        return

    ABH1 = ABHS[0]

    try:
        entity = await bot.get_entity(int(chat_identifier))
    except Exception as e:
        print(f"❌ فشل الحصول على الكيان: {e}")
        return

    is_supergroup = isinstance(entity, Channel) and getattr(entity, 'megagroup', False)
    is_channel = isinstance(entity, Channel) and not getattr(entity, 'megagroup', False)
    is_basic_group = isinstance(entity, Chat)

    print(f"🔹 نوع الشات: {'Supergroup' if is_supergroup else 'Channel' if is_channel else 'Basic Group'}")

    try:
        me1 = await ABH1.get_me()
        rights = ChatAdminRights(add_admins=True)
        if is_basic_group:
            await bot(EditChatAdminRequest(chat_id=chat_identifier, user_id=me1.id, is_admin=True))
        else:
            await bot(EditAdminRequest(channel=entity, user_id=me1.id, admin_rights=rights, rank="مشرف رئيسي"))
        print(f"✅ تم رفع ABH1 ({me1.id}) في {'Supergroup' if is_supergroup else 'Channel' if is_channel else 'Basic Group'}")
    except Exception as e:
        print(f"❌ فشل رفع ABH1 ({me1.id}): {e}")
        return

    for ABH in ABHS[1:]:
        try:
            me = await ABH.get_me()
            if not me.bot:
                print(f"⚠️ تخطي الحساب {me.id} لأنه مستخدم عادي")
                continue

            try:
                participant = await ABH1(GetParticipantRequest(channel=entity, participant=me1.id))
                admin_rights = getattr(participant.participant, 'admin_rights', None)
                if not admin_rights or not getattr(admin_rights, 'add_admins', False):
                    print(f"❌ ABH1 ({me1.id}) لا يملك صلاحية add_admins، تخطي رفع {me.id}")
                    continue
            except Exception:
                pass

            if is_basic_group:
                await ABH1(EditChatAdminRequest(chat_id=chat_identifier, user_id=me.id, is_admin=True))
            else:
                await ABH1(EditAdminRequest(channel=entity, user_id=me.id, admin_rights=rights, rank="مشرف"))
            print(f"✅ تم رفع البوت {me.id} بنجاح")
        except Exception as e:
            print(f"❌ حدث خطأ مع الحساب {me.id}: {e}")

    await asyncio.sleep(2)
@bot.on(events.NewMessage(from_users=[wfffp]))
async def reactauto(e):
    t = e.text.strip()
    if t.startswith("اضف") and e.sender_id == wfffp:
        try:
            chat_id = t.split(" ", 1)[1]
            add_chat(chat_id)
            await promote_ABHS(chat_id)
            await e.reply(f"✅ تم إضافة المجموعة `{chat_id}` إلى القائمة البيضاء")
        except IndexError:
            await e.reply("⚠️ استخدم: `اضف -100xxxxxxxxxx`")
    elif t.startswith("حذف") and e.sender_id == wfffp:
        try:
            chat_id = t.split(" ", 1)[1]
            remove_chat(chat_id)
            await e.reply(f"🗑️ تم حذف المجموعة `{chat_id}` من القائمة البيضاء")
        except IndexError:
            await e.reply("⚠️ استخدم: `حذف -100xxxxxxxxxx`")
    elif is_chat_allowed(e.chat_id):
        await react(e)
        
bot.run_until_disconnected()
