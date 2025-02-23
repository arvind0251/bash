import os
from telethon import TelegramClient, events
from telethon.tl.functions.users import GetFullUserRequest

# ✅ Set API credentials
API_ID = 21552265  # Replace with your API_ID
API_HASH = "1c971ae7e62cc416ca977e040e700d09"  # Replace with your API_HASH

# ✅ Create a UserBot session
client = TelegramClient("userbot_session", API_ID, API_HASH)

# 📌 UserBot Login
async def main():
    print("🔹 Logging in... Enter phone number if required.")
    await client.start()

# 📌 Command: /userinfo <user_id>
@client.on(events.NewMessage(pattern='/userinfo'))
async def user_info(event):
    try:
        args = event.message.text.split(" ")
        if len(args) < 2:
            await event.reply("❌ Please provide a user ID or username. Example: `/userinfo 123456789`")
            return

        user_id = args[1]
        user = await client.get_entity(user_id)
        full_user = await client(GetFullUserRequest(user))

        user_id = user.id
        username = f"@{user.username}" if user.username else "No Username"
        first_name = user.first_name or "No First Name"
        last_name = user.last_name or "No Last Name"
        bio = getattr(full_user.full_user, 'about', 'No Bio')

        # ✅ Fetch all groups the user is in
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
        group_text = "\n".join([f"🔹 {g}" for g in groups]) if groups else "No Groups Found"

        response = f"""
👤 **User Details**
──────────────────
🆔 ID: `{user_id}`
👤 Username: {username}
🏷 Name: {first_name} {last_name}
📜 Bio: {bio}
🏘 Groups Joined: {group_count}

📋 **Group List:**
{group_text}
"""

        await event.reply(response)

    except Exception as e:
        await event.reply(f"❌ Error: {e}")

# ✅ Start the UserBot
with client:
    client.loop.run_until_complete(main())
    client.run_until_disconnected()
