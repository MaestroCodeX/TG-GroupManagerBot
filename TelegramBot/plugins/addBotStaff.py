from pyrogram import Filters, Message
from pyrogram.api import types, functions

from ..customClient import customClient

@customClient.on_message(Filters.command('addStaff', ['/','.']) & Filters.private)
async def _(client : customClient, m : Message):
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
