from pyrogram import filters
from ..customClient import customClient

@customClient.on_message(filters.command("up", [".","/","!"]) & filters.group)
async def PermFissaMod(client : customClient, message):
    if message.reply_to_message != None:
        permission = client.connection["userPermission"]
        if permission.count_documents({'userID': message.from_user.id}) != 0:
            userPerm = permission.find({'userID': message.from_user.id}, {"_id": 0, "pinPerm": 1})
            if message.chat.id in userPerm[0]["pinPerm"]:
                await message.reply_to_message.pin(True)
