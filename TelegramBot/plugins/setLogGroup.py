from pyrogram import filters

from ..customClient import customClient

@customClient.on_message(filters.command('setLog', ['/','.']) & filters.channel)
async def setLogCmd(client : customClient, m):
    if await client.adminInChannel(m):
        key = {'id': m.chat.id}
        value = {'id': m.chat.id, 'name': m.chat.title, 'type': 'LogChannel'}
        res = client.connection['chatlist'].update(key, value, upsert=True)
        await m.reply("This will be a LogChannel", False)

@customClient.on_message(filters.command('unLog', ['/','.']) & filters.channel)
async def unsetLogCmd(client : customClient, m):
    result = client.connection['chatlist'].delete_one({'id': m.chat.id, 'type': 'LogChannel'})
    if result.deleted_count == 1:
        await m.reply("Removed as Log Channel", False)
    else:
        await m.reply("This is not a Log Channel", False)