from telethon import TelegramClient, events
api_id = int(os.getenv("API_ID") 
api_hash = os.getenv("API_HASH") 
bot_token = os.getenv("BOT_TOKEN") 
M = TelegramClient(
    "m", 
    api_id, 
    api_hash)
@M.on(events.NewMessage(from_users=[wfffp, 6520830528])
async def _(e):
