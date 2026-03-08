@bot.on(events.NewMessage(pattern=r'^رياكت (.+)'))
async def react_cmd(event):
    link = event.pattern_match.group(1).strip()
    try:
        # استخراج الـ Entity (المعرف) بشكل صحيح
        if "/c/" in link:
            m = re.search(r't\.me/c/(-?\d+)/(\d+)', link)
            raw_chat_id = m.group(1)
            chat_id = int("-100" + raw_chat_id) if not raw_chat_id.startswith("-100") else int(raw_chat_id)
            msg_id = int(m.group(2))
            entity = chat_id
        else:
            m = re.search(r't\.me/([^\/]+)/(\d+)', link)
            chat_username = m.group(1)
            msg_id = int(m.group(2))
            entity = await bot.get_entity(chat_username)
    except Exception:
        return await event.reply("❌ الرابط غير صحيح أو البوت لا يستطيع الوصول للمحادثة")

    selected = random.sample(emoji, min(len(ABHS), len(emoji)))
    success_count = 0

    for ABH, e in zip(ABHS, selected):
        try:
            # تحويل الـ entity ليناسب الحساب الحالي
            target = await ABH.get_input_entity(entity)
            
            # إرسال الرياكت
            await ABH(SendReactionRequest(
                peer=target,
                msg_id=msg_id,
                reaction=[ReactionEmoji(emoticon=e)],
                big=False
            ))
            success_count += 1
            await asyncio.sleep(0.3) # تجنب الحظر المؤقت
            
        except Exception as er:
            err_str = str(er)
            if "reactions_uniq_max" in err_str:
                print(f"توقف: الرسالة ممتلئة بالرياكتات.")
                break # الخروج من اللوب لأن الرياكتات لن تقبل المزيد
            elif "Could not find the input entity" in err_str:
                print(f"الحساب {ABH} لا يرى المحادثة (ربما ليس منضماً).")
            else:
                print(f"فشل الرياكت: {err_str}")
            continue

    await event.reply(f"✅ تم إرسال {success_count} رياكت بنجاح.")
