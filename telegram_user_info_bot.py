from telethon import TelegramClient, events
from telethon.tl.functions.users import GetFullUserRequest
import os

# 🔹 Replace with your Telegram API Credentials
API_ID = "21552265"
API_HASH = "1c971ae7e62cc416ca977e040e700d09"
BOT_TOKEN = "7739792030:AAFb8j42BbmXqORk5dE8ZlafBn7v9kRaV-Q"

# 🔹 Initialize the Telethon Client
client = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# 📌 Command: /userinfo <user_id>
@client.on(events.NewMessage(pattern='/userinfo'))
async def user_info(event):
    try:
        # Check if user_id is provided
        args = event.message.text.split(" ")
        if len(args) < 2:
            await event.reply("❌ Please provide a user ID or username. Example: `/userinfo 123456789`")
            return

        user_id = args[1]

        # Fetch user details
        user = await client.get_entity(user_id)
        full_user = await client(GetFullUserRequest(user))

        user_id = user.id
        username = f"@{user.username}" if user.username else "No Username"
        first_name = user.first_name or "No First Name"
        last_name = user.last_name or "No Last Name"
        bio = full_user.about if full_user.about else "No Bio"

        # Fetch user groups
        groups = []
        async for dialog in client.iter_dialogs():
            if dialog.is_group:
                try:
                    participants = await client.get_participants(dialog)
                    if any(p.id == user.id for p in participants):
                        groups.append(dialog.title)
                except:
                    continue

        group_count = len(groups)

        # Format response
        response = f"""
👤 **User Details**
──────────────────
🆔 ID: `{user_id}`
👤 Username: {username}
🏷 Name: {first_name} {last_name}
📜 Bio: {bio}
🏘 Groups Joined: {group_count}

📋 **Group List:**
{', '.join(groups) if groups else "No Groups Found"}
"""

        await event.reply(response)

    except Exception as e:
        await event.reply(f"❌ Error: {e}")

# 🔹 Run the bot
print("✅ Bot is running...")
client.run_until_disconnected()
