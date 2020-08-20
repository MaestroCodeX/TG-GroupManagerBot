from pyrogram import Filters, Message
from functools import wraps

from ..customClient import customClient

@customClient.on_message(Filters.command('addGroup', ['/','.']) & (Filters.group | Filters.channel))
async def add2DB(client : customClient, m : Message):
    #if is a channel, who can write must be admin
    if m.chat.type == 'channel' or client.is_admin(m):
        if client.connection['chatlist'].find_one({'id': m.chat.id}) == None:
            newItem = {'id': m.chat.id, 'name': m.chat.title, 'type': m.chat.type}
            id = client.connection['chatlist'].insert_one(newItem)
            if id:
                print('new group added!')
