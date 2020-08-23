from pyrogram import Filters, Message
from pyrogram.errors import RPCError
from pyrogram.api import types

from ..customClient import customClient

# Global Ban Function
@customClient.on_message(Filters.command("globalban"))
async def globalbanCommand(client : customClient, m : Message):
    if client.is_admin(m):
        try:
            print(m.command)
            if len(m.command) > 1:
                peer = await client.resolve_peer(m.command[1])
                if type(peer) is types.input_peer_user.InputPeerUser:
                    await banUser(client, m, peer.user_id)
                else:
                    await m.reply('Wrong Id/username')
            if m.reply_to_message:
                await banUser(client, m, m.reply_to_message.from_user.id)
                return
        except RPCError as e:
            await m.reply(text=f"Error: {e.MESSAGE}")


# Global Unban Function
@customClient.on_message(Filters.command("globalunban"))
async def globalUnban(client : customClient, m : Message):
    if client.is_admin(m):
        try:
            if m.reply_to_message:
                await unbanUser(client, m, m.reply_to_message.from_user.id)
                return
            if len(m.command) > 1:
                peer = await client.resolve_peer(m.command[1])
                if type(peer) is types.input_peer_user.InputPeerUser:
                    await unbanUser(client, m, peer.user_id)
                else:
                    await m.reply('Wrong Id/username')
        except RPCError as e:
            await m.reply(text=f"Error: {e.MESSAGE}")

async def banUser(client : customClient, m, userID):
    chatlist = client.connection["chatlist"]
    cursor = chatlist.find({'type': { "$ne": "LogChannel" }})
    for document in cursor:
        result = await client.kick_chat_member(chat_id=document['id'], user_id=userID)
        if not result:
            await m.reply(text=f"Sorry but I can't ban {userID} from {document['name']}")
    await m.reply(f"You have globally banned {m.reply_to_message.from_user.mention if m.reply_to_message else m.command[1]} [{userID}]")
    #Log Channel
    logchannel = chatlist.find_one({'type': 'LogChannel'})
    if logchannel:
        await client.send_message(chat_id=logchannel['id'], text=f"{m.from_user.mention} [{m.from_user.id}] just did a globalban on {m.reply_to_message.from_user.mention if m.reply_to_message else m.command[1]} [{userID}]")


async def unbanUser(client : customClient, m, userID):
    chatlist = client.connection["chatlist"]
    cursor = chatlist.find({'type': { "$ne": "LogChannel" }})
    for document in cursor:
        result = await client.unban_chat_member(chat_id=document['id'], user_id=userID)
        if not result:
            await m.reply(text=f"Sorry but I can't unban {userID} from {document['name']}")
    await m.reply(f"You have unbanned {m.reply_to_message.from_user.mention if m.reply_to_message else m.command[1]} [{userID}]")
    #Log Channel
    logchannel = chatlist.find_one({'type': 'LogChannel'})
    if logchannel:
        await client.send_message(chat_id=logchannel['id'], text=f"{m.reply_to_message.from_user.mention if m.reply_to_message else m.command[1]} [{userID}] has been globally unbanned from {m.from_user.mention} [{m.from_user.id}]")