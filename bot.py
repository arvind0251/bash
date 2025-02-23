import os
from telethon import TelegramClient, events
from telethon.tl.functions.users import GetFullUserRequest
from dotenv import load_dotenv

# 🔹 Load API credentials securely from .env file
load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# 🔹 Initialize the Telethon Bot Client
client = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# 📌 Command: /userinfo <user_id>
@client.on(events.NewMessage(pattern='/userinfo'))
async def user_info(event):
    try:
        # Extract user ID from the command
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
        bio = getattr(full_user, 'about', 'No Bio')  # ✅ FIX: Handle missing bio

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

        # Split groups if too long
        if group_count > 0:
            group_text = "\n".join([f"🔹 {g}" for g in groups])
            group_message = f"🏘 **Groups Joined ({group_count}):**\n\n{group_text}"
        else:
            group_message = "🏘 **No groups found.**"

        # Format response
        response = f"""
👤 **User Details**
──────────────────
🆔 ID: `{user_id}`
👤 Username: {username}
🏷 Name: {first_name} {last_name}
📜 Bio: {bio}
🏘 Groups Joined: {group_count}

{group_message}
"""

        # Split message if too long
        if len(response) > 4096:
            for chunk in [response[i:i+4096] for i in range(0, len(response), 4096)]:
                await event.reply(chunk)
        else:
            await event.reply(response)

    except Exception as e:
        await event.reply(f"❌ Error: {e}")

# 🔹 Run the bot
print("✅ Bot is running...")
client.run_until_disconnected()
