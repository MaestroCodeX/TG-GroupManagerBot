from pyrogram import filters

from ..customClient import customClient

@customClient.on_message(filters.command('addGroup', ['/','.']) & (filters.group | filters.channel))
async def add2DB(client : customClient, m):
    #if is a channel, who can write must be admin
    if (
        (m.chat.type == 'channel' and await client.adminInChannel(m))
        or client.is_admin(m)
    ) and client.connection['chatlist'].find_one({'id': m.chat.id}) is None:
        newItem = {'id': m.chat.id, 'name': m.chat.title, 'type': m.chat.type}
        id = client.connection['chatlist'].insert_one(newItem)
        if id:
            print(f'new group added!\n{newItem}')
