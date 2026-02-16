import random
import asyncio
from telethon.tl.functions.messages import SendReactionRequest, GetFullChatRequest
from telethon.tl.types import ReactionEmoji, PeerChannel

async def react(event):
    chat_id = event.chat_id
    msg_id = event.message.id
    
    # تحويل الـ ID إلى صيغة PeerChannel التي يفهمها التليجرام للقنوات
    # ملاحظة: تأكد أن ID القناة يبدأ بـ -100 (مثلاً: -1003675205923)
    peer_type = PeerChannel(int(str(chat_id).replace("-100", "")))

    for ABH in ABHS:
        try:
            # الحل السحري: إجبار الحساب على جلب بيانات الكيان برمجياً
            # هذا السطر يجعل Telethon يحفظ الـ Access Hash تلقائياً
            try:
                entity = await ABH.get_input_entity(chat_id)
            except ValueError:
                # إذا لم يجدها، نحاول جلبها من الـ Dialogs (المحادثات الأخيرة)
                async for dialog in ABH.iter_dialogs():
                    if dialog.id == chat_id:
                        entity = dialog.input_entity
                        break
                else:
                    # إذا فشل كل شيء، نحاول جلب الكيان من الحدث مباشرة
                    entity = await ABH.get_entity(chat_id)

            stored = get_reactions(chat_id)
            emoji_text = random.choice(stored) if stored else random.choice(['❤️', '🕊', '🌚'])
            
            # إرسال التفاعل
            await ABH(SendReactionRequest(
                peer=entity,
                msg_id=msg_id,
                reaction=[ReactionEmoji(emoticon=emoji_text)],
                big=False
            ))
            
            await asyncio.sleep(0.1)

        except Exception as e:
            print(f"فشل التفاعل للحساب {ABH}: {e}")
            continue
