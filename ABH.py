from telethon import TelegramClient, events
import os, re, random, redis, asyncio, sys
from telethon.tl.types import (
    ReactionEmoji,
    ChatAdminRights)
from telethon.tl.functions.channels import (
    JoinChannelRequest,
    EditAdminRequest)
from telethon.tl.functions.messages import (
    ImportChatInviteRequest)
from telethon.tl.functions.messages import SendReactionRequest
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
wfffp = 1910015590
target_user_id = 1421907917
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("bot_token")
bot_tokens = [os.getenv(f"bot_token{i}") for i in range(1, 12)]
bot = TelegramClient("code", api_id, api_hash).start(bot_token=bot_token)
ABH1 = TelegramClient("code1", int(os.getenv("API_ID1")), os.getenv("API_HASH1")).start()
ABH2 = TelegramClient("code2", int(os.getenv("API_ID2")), os.getenv("API_HASH2")).start()
ABH3 = TelegramClient("code3", int(os.getenv("API_ID3")), os.getenv("API_HASH3")).start()
ABH4 = TelegramClient("code4", int(os.getenv("API_ID4")), os.getenv("API_HASH4")).start()
ABH5 = TelegramClient("code5", int(os.getenv("API_ID5")), os.getenv("API_HASH5")).start()
ABH6 = TelegramClient("code6", int(os.getenv("API_ID6")), os.getenv("API_HASH6")).start()
ABH7 = TelegramClient("code7", int(os.getenv("API_ID7")), os.getenv("API_HASH7")).start()
ABH8 = TelegramClient("code8", int(os.getenv("API_ID8")), os.getenv("API_HASH8")).start()
ABH9 = TelegramClient("code9", int(os.getenv("API_ID9")), os.getenv("API_HASH9")).start()
ABH10 = TelegramClient("code10", int(os.getenv("API_ID10")), os.getenv("API_HASH10")).start()
print('all userbot are working!')
ABHS = [ABH1, ABH2, ABH3, ABH4, ABH5, ABH6, ABH7, ABH8, ABH9, ABH10]
for i, token in enumerate(bot_tokens, start=1):
    if token:
        ABHS.append(TelegramClient(f"botcode{i}", api_id, api_hash).start(bot_token=token))
print('all bot are working!')
ABHS.append(bot)
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
from telethon.tl.functions.messages import SendReactionRequest, GetMessagesViewsRequest
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import ReactionEmoji

async def react(event):
    if not event.is_channel or not event.message or not event.message.post:
        return

    chat_id = event.chat_id
    msg_id = event.message.id

    for ABH in ABHS:
        try:
            # 1. جلب الكيان (Entity)
            try:
                peer = await ABH.get_input_entity(chat_id)
            except Exception:
                peer = await ABH.get_entity(chat_id)

            # 2. إضافة مشاهدة (View) للرسالة
            # إرسال هذا الطلب يخبر تلغرام أن الحساب قد "رأى" الرسالة فعلياً
            try:
                await ABH(GetMessagesViewsRequest(
                    peer=peer,
                    id=[msg_id],
                    increment=True # هذا الجزء هو المسؤول عن زيادة العداد
                ))
            except Exception as view_error:
                print(f"فشل في زيادة المشاهدة: {view_error}")

            # 3. اختيار الإيموجي وإرسال التفاعل
            stored = get_reactions(event.chat_id)
            emoji = random.choice(stored) if stored else random.choice(['❤️', '🕊', '🌚'])
            
            await ABH(SendReactionRequest(
                peer=peer,
                msg_id=msg_id,
                reaction=[ReactionEmoji(emoticon=emoji)],
                big=False
            ))            
            
            # تأخير بسيط لتجنب حظر الحسابات (Flood Wait)
            await asyncio.sleep(0.3)
            
        except Exception as e:
            print(f"Error for account {ABH.session.filename if hasattr(ABH, 'session') else 'Bot'}: {e}")
            continue
@bot.on(events.NewMessage(pattern='ABHS', from_users=[wfffp, 201728276]))
async def test(e):
    for ABH in ABHS[:8]:  # الحلقة هنا
        try:
            await ABH.send_message(e.chat_id, 'نعم', reply_to=e.id)
        except Exception as E:
            x = await ABH.get_me()
            await e.reply(f"{x.id}    {E}")
            continue  # هذا الآن صحيح، لأننا داخل الحلقة
@bot.on(events.NewMessage(pattern='شغال؟', from_users=[wfffp, 201728276]))
async def test(e):
    for ABH in ABHS:  # الحلقة هنا
        try:
            await ABH.send_message(e.chat_id, 'نعم', reply_to=e.id)
        except Exception as E:
            x = await ABH.get_me()
            await e.reply(f"{x.id}    {E}")
            continue  # هذا الآن صحيح، لأننا داخل الحلقة
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
    'ابو قتادة الرافضي': ABH2,
    'ابو قتاده الرافضي': ABH2,
    'سالو': ABH3,
    'salo': ABH3,
    'حسن جداحه': ABH4,
    'حسن جداحة': ABH4,
    'برق الشايب': ABH5,
    'هاشم محمد': ABH6,
    'كرت الحظ': ABH7,
    'الخطير حسون': ABH8,
    'حسن حسام': ABH9,
    'عبدلمستسلم': ABH10,
}
import re
import random
import asyncio
from telethon import events, functions, types
from telethon.tl.functions.messages import SendReactionRequest

@bot.on(events.NewMessage(pattern=r'^رياكت(?: (.+))?', from_users=[wfffp, 201728276]))
async def react_cmd(event):
    # 1. تحديد الرسالة المستهدفة (سواء عبر الرابط أو عبر الـ Reply)
    reply = await event.get_reply_message()
    input_str = event.pattern_match.group(1)
    
    msg_id = None
    entity = None

    if input_str and "t.me/" in input_str:
        # استخراج البيانات من الرابط المرسل في الأمر
        link_parts = re.search(r't\.me/(?:c/)?([\w+]+)/(\d+)', input_str)
        if link_parts:
            chat_info = link_parts.group(1)
            msg_id = int(link_parts.group(2))
            entity = int(f"-100{chat_info}") if chat_info.isdigit() else chat_info
    elif reply:
        # إذا لم يوجد رابط، نستخدم الرسالة التي تم الرد عليها
        msg_id = reply.id
        entity = reply.chat_id
    else:
        return await event.reply("❌ يرجى إرسال رابط الرسالة أو الرد على الرسالة المطلوبة.")

    # 2. إعداد قائمة الإيموجي
    emoji = ["❤️", "👍", "👏", "🤔", "🤯", "🙏", "👌", "😎", "🫡" ]
    selected = random.sample(emoji, min(len(ABHS), len(emoji)))
    success_count = 0

    await event.reply(f"🚀 جاري إرسال {len(selected)} رياكت...")

    # 3. إرسال الرياكتات عبر الحسابات
    for ABH, e in zip(ABHS[:10], selected):
        try:
            # تحويل الـ entity لكل حساب لضمان الوصول
            target = await ABH.get_input_entity(entity)
            
            await ABH(SendReactionRequest(
                peer=target,
                msg_id=msg_id,
                reaction=[types.ReactionEmoji(emoticon=e)],
                big=False
            ))
            success_count += 1
            await asyncio.sleep(0.5) 
            
        except Exception as er:
            print(f"فشل الرياكت من {ABH}: {er}")
            continue

    await event.reply(f"✅ تم إرسال {success_count} رياكت بنجاح.")
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
    if str(e.chat_id) in list_chats():
        try:
            await react(e)
        except Exception as ex:
            print(f"خطأ في التفاعل: {ex}")
@bot.on(events.NewMessage)
async def nlits(e):
    if not event.is_private:return
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
async def run_cmd(command: str):
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return stdout.decode().strip(), stderr.decode().strip(), process.returncode
@bot.on(events.NewMessage(pattern="^تحديث$", from_users=[1910015590]))
async def update_repo(event):
    msg = await event.respond(" جاري جلب آخر التحديثات من الريبو عبر...")
    stdout, stderr, code = await run_cmd("git pull")
    if code == 0:
        await msg.edit(f" تحديث السورس بنجاح")
        os.execv(sys.executable, [sys.executable, "p.py"])
    else:
        await msg.edit(f" حدث خطأ أثناء التحديث:\n\n{stderr}")
import re
from telethon import events

# دالة لحذف رسائل البوت
async def delete_bot_messages(client, chat, limit=None):
    """
    تحذف رسائل البوت من المحادثة المحددة.
    
    :param client: كائن Telethon
    :param chat: الـ chat أو chat_id
    :param limit: عدد الرسائل للحذف (None = كل الرسائل)
    :return: عدد الرسائل المحذوفة
    """
    messages = []
    deleted_count = 0

    async for msg in client.iter_messages(chat, from_user='me', limit=limit):
        messages.append(msg.id)

        # حذف على دفعات لتجنب مشاكل الـ flood
        if len(messages) >= 100:
            await client.delete_messages(chat, messages)
            deleted_count += len(messages)
            messages = []

    # حذف الباقي
    if messages:
        await client.delete_messages(chat, messages)
        deleted_count += len(messages)

    return deleted_count

# أمر تيليجرام لحذف رسائل البوت
@bot.on(events.NewMessage(pattern=r'^حذف رسائل(?: (.+))?', from_users=[wfffp, 201728276]))
async def react_cmd(event):
    reply = await event.get_reply_message()
    input_str = event.pattern_match.group(1)

    msg_id = None
    entity = None

    # التعامل مع رابط t.me
    if input_str and "t.me/" in input_str:
        link_parts = re.search(r't\.me/(?:c/)?([\w\d]+)/(\d+)', input_str)
        if link_parts:
            chat_info = link_parts.group(1)
            msg_id = int(link_parts.group(2))
            # تحويل chat_id للقناة إذا كان رقمي
            entity = int(f"-100{chat_info}") if chat_info.isdigit() else chat_info
        else:
            return await event.reply("❌ الرابط غير صالح.")
    elif reply:
        # إذا لم يوجد رابط، استخدم الرسالة التي تم الرد عليها
        msg_id = reply.id
        entity = reply.chat_id
    else:
        return await event.reply("❌ يرجى إرسال رابط الرسالة أو الرد على الرسالة المطلوبة.")

    # حذف الرسائل لكل عميل موجود في ABHS
    total_deleted = 0
    for ABH in ABHS:
        count = await delete_bot_messages(ABH, entity)
        total_deleted += count

    await event.reply(f"✅ تم حذف {total_deleted} رسالة بنجاح.")
        
print('running')
bot.run_until_disconnected()
