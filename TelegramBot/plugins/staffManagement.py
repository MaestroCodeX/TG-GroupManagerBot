from pyrogram import Filters, Message
from pyrogram.api import types, functions

from ..customClient import customClient

@customClient.on_message(Filters.command('addStaff', ['/','.']) & Filters.private)
async def addStaffCmd(client : customClient, m : Message):
    #if is a channel, who can write must be admin
    if m.from_user.id == client.CREATOR_ID:
        if len(m.command) == 2:
            peer = await client.resolve_peer(m.command[1])
            if type(peer) is types.input_peer_user.InputPeerUser:
                user = types.InputUser(user_id=peer.user_id, access_hash=peer.access_hash)
                fullUser = await client.send(functions.users.GetFullUser(id=user))
                allStaff = client.connection["stafflist"]
                key = {'id': fullUser.user.id}
                value = {"id": fullUser.user.id, "first_name": fullUser.user.first_name, "username": fullUser.user.username}
                result = allStaff.update(key, value, upsert=True)

                if result['nModified'] == 0:
                    #if not modified => added a new one
                    await client.send_message(chat_id=m.chat.id, text=fullUser.user.first_name + " is admin now")
                    client.loadAdmin()
                else:
                    #there is already a document with this id
                    await client.send_message(chat_id=m.chat.id, text=fullUser.user.first_name + " is already admin")


# Remove Staff from DB 
@customClient.on_message(Filters.command("rmStaff") & Filters.private)
async def removeStaffCmd(client : customClient, message : Message):
    if message.chat.id == client.CREATOR_ID:
        if len(message.command) == 2:
            peer = await client.resolve_peer(message.command[1])
            if type(peer) is types.input_peer_user.InputPeerUser:
                user = types.InputUser(user_id=peer.user_id, access_hash=peer.access_hash)
                fullUser = await client.send(functions.users.GetFullUser(id=user))
                allStaff = client.connection["stafflist"]
                result = allStaff.delete_one({"id": fullUser.user.id})
                if result.deleted_count == 1:
                    await client.send_message(chat_id=message.chat.id, text=fullUser.user.first_name + " removed from staff")
                    client.loadAdmin() 
                else:
                    await client.send_message(chat_id=message.chat.id, text=fullUser.user.first_name + " is not an admin")

                
# Staff List Function
@customClient.on_message(Filters.command("staff") & Filters.private)
async def staffCmd(client : customClient, m : Message):
    msg = "Staff List:\n"
    staffdb = client.connection["stafflist"]
    cursor = staffdb.find({})
    for document in cursor:
        msg += f"<a href='tg://user?id={document['id']}'>{document['first_name']}</a>\n"
    await client.send_message(chat_id=m.chat.id, text=msg, parse_mode="HTML")
