from pyrogram import Client, filters
import os
import asyncio

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_ID = int(os.environ["CHANNEL_ID"])

app = Client(
    "mybot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)


@app.on_message(filters.command("start"))
async def start_cmd(client, message):
    user_id = message.from_user.id

    try:
        member = await client.get_chat_member(CHANNEL_ID, user_id)
        if member.status not in ["member", "creator", "administrator"]:
            await message.reply("برای استفاده از ربات باید عضو کانال شوید.")
            return
    except:
        await message.reply("برای استفاده از ربات باید عضو کانال شوید.")
        return

    await message.reply("سلام! لینک ویدئو را بفرست تا نمایش دهم.")


@app.on_message(filters.text)
async def send_video(client, message):
    link = message.text

    msg = await message.reply("⏳ در حال دانلود و ارسال ویدئو...")

    try:
        sent = await client.send_video(
            chat_id=message.chat.id,
            video=link
        )

        await asyncio.sleep(300)
        await client.delete_messages(message.chat.id, [sent.id])

        await msg.delete()

    except Exception as e:
        await msg.edit(f"خطا: {e}")


app.run()
