from pyrogram import filters
from pyrogram.errors import RPCError
from ..customClient import customClient

@customClient.on_message(filters.command("revokelink", ['.', '/']) & filters.group)
async def revokeOneGroup(client : customClient, message):
    if client.is_admin(message):
        try:
            result = await client.export_chat_invite_link(message.chat.id)
            if result:
                await client.send_message(-1001390923977, f"{message.from_user.mention} revoked the link for the group {message.chat.title}")
                await client.send_message(message.chat.id, "Link revoked " + message.chat.title)
            else:
                await client.send_message(-1001390923977, "I haven't generated any link for the group " + message.chat.title)
        except RPCError:
            await client.send_message(message.chat.id, "I'm not an admin, I have no active link!")


@customClient.on_message(filters.command("getlink", ['.', '/']) & filters.group)
async def getLinkCommand(client : customClient, message):
    if client.is_admin(message):
        chat = await client.get_chat(message.chat.id)
        link = chat.invite_link
        if link is not None:
            await client.send_message(message.from_user.id, link)
        else:
            try:
                link = await client.export_chat_invite_link(message.chat.id)
                await client.send_message(message.from_user.id, link)
            except RPCError:
                await client.send_message(message.chat.id, "I'm not an Admin!")


@customClient.on_message(filters.command("revokeAll", ['.', '/']) & filters.private)
async def revokeLinkCommand(client : customClient, message):
    if client.is_admin(message):
        staffdb = client.connection["chatlist"]
        cursor = staffdb.find({})
        for document in cursor:
            try:
                result = await client.export_chat_invite_link(document['id'])   
                print(result)        
                if not result:
                    await client.send_message(-1001390923977, f"Sorry i couldn't revoke link for the group {document['title']}[{document['id']}]")
            except RPCError:
                await client.send_message(message.chat.id, f"I'm not admin in {document['title']}[{document['id']}]")
        await client.send_message(-1001390923977, "Link revoked in all groups")
