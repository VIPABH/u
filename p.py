from ABH import ABH, events, bot_token
import json, pytz, asyncio, os, sys
from datetime import datetime
from code import *
async def run_cmd(command: str):
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return stdout.decode().strip(), stderr.decode().strip(), process.returncode
@ABH.on(events.NewMessage(pattern="^تحديث$", from_users=[1910015590]))
async def update_repo(event):
    stdout, stderr, code = await run_cmd("git pull")
    if code == 0:
        await event.reply(f" تحديث السورس بنجاح")
        os.execv(sys.executable, [sys.executable, "p.py"])
    else:
        await event.reply(f" حدث خطأ أثناء التحديث:\n\n{stderr}")
def main():
    print("config is starting...")
    ABH.start(bot_token=bot_token)
    ABH.run_until_disconnected()
if __name__ == "__main__":
    main()
