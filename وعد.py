from telethon import events
import asyncio, re
from ABH import *
target_user_id = 1421907917
@bot.on(events.NewMessage(pattern='!تجربة'))
async def test(e):
    a = 0
    for ABH in ABHS:
        x = f'ABH{a+1}'
        await x.send_message(e.chat_id, 'نعم', reply_to=e.id)
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
@bot.on(events.NewMessage(pattern=r"^.?تركيب (\d+)$", from_users=[1910015590, 201728276]))
async def unspilt(event):
    num = int(event.pattern_match.group(1)) or 1
    for i in range(num):
        async with bot.conversation(event.chat_id, timeout=10) as conv:
            await conv.send_message("تركيب")
            try:
                while True:
                    msg = await conv.get_response()
                    if msg.sender_id != target_user_id:
                        continue
                    text = msg.raw_text.strip()
                    match = re.search(r"\(\s*(.+?)\s*\)", text)
                    if match:
                        text = match.group(1)
                        merged = ''.join(text.split())
                        await conv.send_message(merged)
                    break
            except asyncio.TimeoutError:
                return
@bot.on(events.NewMessage(pattern=r"^.?تفكيك (\d+)$", from_users=[1910015590, 201728276]))
async def spilt(event):
    num = int(event.pattern_match.group(1)) or 1
    for i in range(num):
        async with bot.conversation(event.chat_id, timeout=10) as conv:
            await conv.send_message("تفكيك")
            try:
                while True:
                    msg = await conv.get_response()
                    if msg.sender_id != target_user_id:
                        continue
                    text = msg.raw_text.strip()
                    match = re.search(r"\(\s*(.+?)\s*\)", text)
                    if match:
                        text = match.group(1)
                        clean = ''.join(text.split())
                        separated = ' '.join(clean)
                        await conv.send_message(separated)
                    break
            except asyncio.TimeoutError:
                return
@bot.on(events.NewMessage(pattern=r"^.?احسب (\d+)$", from_users=[1910015590, 201728276]))
async def calc(event):
    num = int(event.pattern_match.group(1)) or 1
    for _ in range(num):
        async with bot.conversation(event.chat_id, timeout=10) as conv:
            await conv.send_message("احسب")
            try:
                while True:
                    msg = await conv.get_response()
                    if msg.sender_id != target_user_id:
                        continue

                    text = msg.raw_text.strip()
                    match = re.search(r"([\d\s\+\-\*÷\/\.]+)\s*=", text)
                    if match:
                        expression = match.group(1).replace('÷', '/').replace('×', '*').strip()
                        try:
                            result = eval(expression)
                            if isinstance(result, float) and result.is_integer():
                                result = int(result)
                            await conv.send_message(str(result))
                        except Exception:
                            await conv.send_message("خطأ في الحساب.")
                    break
            except asyncio.TimeoutError:
                return
@bot.on(events.NewMessage(pattern=r"^.?جمل (\d+)$", from_users=[1910015590, 201728276]))
async def j(event):
    num = int(event.pattern_match.group(1)) or 1
    for _ in range(num):
        async with bot.conversation(event.chat_id, timeout=10) as conv:
            await conv.send_message("جمل")
            try:
                while True:
                    msg = await conv.get_response()
                    if msg.sender_id != target_user_id:
                        continue
                    text = msg.raw_text.strip()
                    match = re.search(r"\((.*?)\)", text)
                    if match:
                        inside = match.group(1)
                        cleaned = re.sub(r"[↢⇜'«»]", "", inside)
                        normalized = re.sub(r"\s+", " ", cleaned).strip()
                        await conv.send_message(normalized)
                    else:
                        return
                    break
            except asyncio.TimeoutError:
                return
@bot.on(events.NewMessage(pattern=r"^.?تفاعل|تفاعل\s+(\d+)\s+(\d+(?:\.\d+)?)$", from_users=[1910015590, 201728276]))
async def sends(event):
    much = int(event.pattern_match.group(1))
    time = float(event.pattern_match.group(2))
    r = await event.get_reply_message()
    if not r:
        await event.reply('🤔 يجب أن ترد على رسالة.')
        return
    for i in range(much):
        await words(event)
        await asyncio.sleep(time)
