
from telethon.tl.functions.channels import EditAdminRequest
from telethon.tl.types import ChatAdminRights, Channel
from telethon.tl.types import ReactionEmoji
from telethon.errors import UserAlreadyParticipantError
from telethon.errors import ChatAdminRequiredError
from telethon.tl.types import ReactionEmoji
from telethon import events, TelegramClient
from telethon.tl.types import PeerChannel
import os, random, redis, re, asyncio
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
target_user_id = 1421907917
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
import random
from telethon import events, functions, types
from telethon.errors import ChatAdminRequiredError, UserAlreadyParticipantError
from telethon.tl.functions.messages import ImportChatInviteRequest, ExportChatInviteRequest
from telethon.tl.functions.channels import (
    GetParticipantRequest,
    EditAdminRequest
)
from telethon.tl.types import ChatAdminRights, Channel
from telethon.tl.custom import SendReactionRequest, ReactionEmoji

# من المفترض أنك معرف المتغيرات التالية في ملفك الرئيسي:
# r = redis.StrictRedis(...)
# bot = الكلاينت الرئيسي
# ABHS = قائمة الجلسات الثانوية
# wfffp = معرف المطور أو المالك الأساسي

# ===== دوال القوائم البيضاء =====
def add_chat(chat_id):
    r.sadd("whitelist_chats", str(chat_id))

def remove_chat(chat_id):
    r.srem("whitelist_chats", str(chat_id))

def is_chat_allowed(chat_id):
    return str(chat_id) in r.smembers("whitelist_chats")


# ===== التفاعل التلقائي مع الرسائل =====
async def react(event):
    for ABH in ABHS:
        try:
            x = random.choice(['👍', '🕊', '❤️'])
            await ensure_joined(ABH, bot, event.chat_id)
            await ABH(
                SendReactionRequest(
                    peer=event.chat_id,
                    msg_id=int(event.message.id),
                    reaction=[ReactionEmoji(emoticon=f'{x}')],
                    big=True
                )
            )
            await ABH.send_read_acknowledge(event.chat_id, int(event.message.id))
        except Exception as ex:
            await bot.send_message(wfffp, str(ex))
            pass


# ===== التأكد من وجود الحساب في المجموعة =====
async def is_member(ABH, chat_id, user_id):
    try:
        await ABH(GetParticipantRequest(chat_id, user_id))
        return True
    except Exception:
        return False


# ===== جلب رابط الدعوة =====
async def get_invite_link(ABH, chat):
    try:
        entity = await ABH.get_entity(chat)
        try:
            result = await bot(ExportChatInviteRequest(entity))
            return result.link
        except ChatAdminRequiredError:
            print("❌ الحساب ليس مشرفًا، لا يمكن استخراج رابط الدعوة")
            return None
    except Exception as ex:
        print(f"❌ خطأ أثناء جلب الكيان: {ex}")
        return None


# ===== التأكد من انضمام الحساب =====
async def ensure_joined(ABH, bot, chat_id):
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
                print(f"✅ الحساب {me.id} انضم إلى {chat_id}")
            except UserAlreadyParticipantError:
                pass
            except Exception:
                try:
                    invite_link = await get_invite_link(bot, chat_id)
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
                        print(f"✅ تم رفع الحساب {me.id} مشرفاً بعد فشل الانضمام")
                    except Exception as promote_ex:
                        print(f"❌ فشل رفع الحساب {me.id} مشرفاً: {promote_ex}")
        else:
            print(f"❌ لا يوجد رابط دعوة متاح لـ {chat_id}")
    except Exception as ex:
        print(f"❌ خطأ أثناء تنفيذ العملية: {ex}")


# ===== رفع جميع حسابات ABH =====
async def promote_ABHS(chat_identifier):
    if not ABHS:
        print("❌ قائمة ABHS فارغة")
        return

    ABH1 = ABHS[0]
    try:
        channel_entity_bot = await bot.get_input_entity(int(chat_identifier))
    except Exception as e:
        print(f"❌ فشل الحصول على كيان المجموعة {chat_identifier}: {e}")
        return

    try:
        me1 = await ABH1.get_me()
        admin_rights_add_admins_only = ChatAdminRights(
            change_info=False,
            post_messages=False,
            edit_messages=False,
            delete_messages=False,
            ban_users=False,
            invite_users=False,
            pin_messages=False,
            add_admins=True,
            manage_call=False,
            anonymous=False
        )

        await bot(EditAdminRequest(
            channel=channel_entity_bot,
            user_id=int(me1.id),
            admin_rights=admin_rights_add_admins_only,
            rank="مشرف رئيسي"
        ))
        print(f"✅ تم رفع ABH1 ({me1.id}) بصلاحية رفع مشرفين فقط")
    except Exception as e:
        print(f"❌ فشل رفع ABH1 ({me1.id}): {e}")
        return

    for ABH in ABHS[1:]:
        try:
            me = await ABH.get_me()
            if not me.bot:
                continue

            channel_entity_abh1 = await ABH1.get_input_entity(int(chat_identifier))

            try:
                await ABH1(GetParticipantRequest(channel_entity_abh1, int(me.id)))
                print(f"⚠️ البوت {me.id} عضو بالفعل، تخطي.")
                continue
            except Exception:
                pass

            await ABH1(EditAdminRequest(
                channel=channel_entity_bot,
                user_id=int(me.id),
                admin_rights=admin_rights_add_admins_only,
                rank="مشرف رئيسي"
            ))
            print(f"✅ تم رفع البوت {me.id} مشرفاً بواسطة ABH1")

        except Exception as e:
            print(f"❌ خطأ أثناء رفع {me.id}: {e}")


# ===== أوامر الإضافة والحذف من القائمة =====
@bot.on(events.NewMessage)
async def reactauto(e):
    t = e.text.strip()

    # أمر الإضافة
    if t.startswith("اضف") and e.sender_id == wfffp:
        try:
            chat_id = t.split(" ", 1)[1]
            add_chat(chat_id)
            await promote_ABHS(chat_id)
            await e.reply(f"✅ تم إضافة المجموعة `{chat_id}` إلى القائمة البيضاء.")
        except IndexError:
            await e.reply("⚠️ استخدم: `اضف -100xxxxxxxxxx`")
    elif t.startswith("حذف") and e.sender_id == wfffp:
        try:
            chat_id = t.split(" ", 1)[1]
            remove_chat(chat_id)
            await e.reply(f"🗑️ تم حذف المجموعة `{chat_id}` من القائمة البيضاء.")
        except IndexError:
            await e.reply("⚠️ استخدم: `حذف -100xxxxxxxxxx`")    
    elif is_chat_allowed(e.chat_id):
        await react(e)
        print("جاري")
bot.run_until_disconnected()
