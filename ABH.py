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
idd = ABHS[7:]
client = ABH1
async def promote_ABHS(chat_id=None):
    try:
        xxx = int(chat_id)
        for AB in idd:
            id_info = await AB.get_me()
            rights = ChatAdminRights(
                change_info=True,
                post_messages=True,
                edit_messages=True,
                delete_messages=True
            )
            await ABH1(EditAdminRequest(
                channel=xxx,
                user_id=id_info.id,
                admin_rights=rights,
                rank="bot"
            ))
            print(f"✅ تم رفع البوت {id_info.id} مشرف بالقناة بالصلاحيات المناسبة")
    except Exception as E:
        print(E)
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
chats = list_chats()
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
def remove_non_private_chats():
    chats = r.smembers("whitelist_chats")
    for chat_id in chats:
        chat_id_str = chat_id.decode() if isinstance(chat_id, bytes) else str(chat_id)
        if not chat_id_str.startswith("-100"):
            r.srem("whitelist_chats", chat_id_str)
            print(f"✅ تم حذف {chat_id_str}")
async def startup_warmup():
    print("جاري تهيئة الحسابات والتعرف على القنوات...")
    for ABH in ABHS:
        try:
            await ABH.get_dialogs(limit=20)
            print(f"تمت تهيئة الحساب: {ABH.session.filename}")
        except Exception as e:
            print(f"فشل تهيئة الحساب {ABH.session.filename}: {e}")
import random
import asyncio
from telethon.tl.functions.messages import SendReactionRequest, GetFullChannelRequest
from telethon.tl.types import ReactionEmoji

async def react(event):
    # التأكد أنها قناة (Broadcast) وليست رسالة خدمية
    if not event.is_channel or not event.message or not event.message.post:
        return

    chat_id = event.chat_id
    msg_id = event.message.id

    for ABH in ABHS:
        try:
            # جلب الكيان (Entity) وتحديث الجلسة إذا لزم الأمر
            try:
                peer = await ABH.get_input_entity(chat_id)
            except Exception:
                # إذا لم يجد الكيان، نجبره على جلب القناة بالكامل
                peer = await ABH.get_entity(chat_id)

            # لتجنب خطأ "Invalid reaction"، سنستخدم إيموجي بسيط ومضمون
            # أو يمكنك استخراج الإيموجيات المسموحة في القناة برمجياً
            await ABH(SendReactionRequest(
                peer=peer,
                msg_id=msg_id,
                reaction=[ReactionEmoji(emoticon='👍')], # جرب 👍 للتأكد من العمل
                big=False
            ))            
            
            await asyncio.sleep(0.2)
            
        except Exception as e:
            # إذا كان الخطأ بسبب الإيموجي، سيطبع لنا ذلك
            print(f"Error for account {ABH.session.filename if hasattr(ABH, 'session') else 'Bot'}: {e}")
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
@ABH1.on(events.NewMessage(pattern='تجربة', from_users=[wfffp, 201728276]))
async def reactauto(e):
    await react(e)
@ABH1.on(events.NewMessage(from_users=[wfffp, 201728276]))
async def reactauto(e):
    if not e.text:
        return
    text = e.text
    if text in names:
        reply_text = random.choice(['الزعيم', "الغالي", "كول يالامير", "تاج الراس"])
        try:
            await names[text].send_message(
                e.chat_id,
                reply_text,
                reply_to=e.id
            )
        except:
            return
@bot.on(events.NewMessage)
async def nlits(e):
    print(str(e.chat_id) in chats)
    if str(e.chat_id) in chats:
        try:
            await react(e)
        except Exception as ex:
            print(f"خطأ في التفاعل: {ex}")
@bot.on(events.NewMessage)
async def nlits(e):
    text = e.text
    sender = e.sender_id
    chat_id = None
    if text.startswith("اضف") and sender == wfffp:
        try:
            chat_id = text.split(" ", 1)[1]
        except (IndexError, ValueError):
            await e.reply("❌ يرجى تحديد رقم القناة بعد 'اضف'")
            return
        if not chat_id.startswith("-100"):
            return
        chat_id = int(chat_id)
        await promote_ABHS(chat_id)
        await e.reply(f"✅ تم إضافة القناة `{chat_id}` إلى القائمة البيضاء")
        add_chat(chat_id)
    elif text.startswith("ضيف") and sender == wfffp:
        try:
            chat_id = int(text.split(" ", 1)[1])
        except (IndexError, ValueError):
            chat_id = e.chat_id 
        await promote_ABHS(chat_id)
        await e.reply(f"✅ تم رفع البوتات في القناة `{chat_id}`")
    elif text.startswith("القنوات") and sender == wfffp:
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
    elif text == 'تصفية':
        remove_non_private_chats()
        await e.reply('تم التصفية')
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
    elif text== "حذف التفاعلات" and sender == wfffp:
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
    elif text == "حذف الكل" and sender == wfffp:
        clear_chats()
        await e.reply("🗑️ تم حذف جميع القنوات من القائمة البيضاء")
    elif text.startswith("حذف ") and sender == wfffp and not text == "حذف تفاعل" and not text == "حذف التفاعلات":
        try:
            chat_id = text.split(" ", 1)[1]
            remove_chat(chat_id)
            await e.reply(f"🗑️ تم حذف القناة `{chat_id}` من القائمة البيضاء")
        except IndexError:
            await e.reply("⚠️ استخدم: `حذف -100xxxxxxxxxx`")
print('running')
bot.run_until_disconnected()
