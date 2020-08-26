from pyrogram import Filters, Message, InlineKeyboardButton, InlineKeyboardMarkup
from ..customClient import customClient

# Broadcast Command
@customClient.on_message(Filters.command("broadcast") & Filters.private)
async def broadcastCommand(client : customClient, m : Message):
    if client.is_admin(m) and m.reply_to_message:
        message = m.reply_to_message
        buttons = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Fissa ❌", callback_data="Fix false"),
                        InlineKeyboardButton("Notifica ❌", callback_data="Notifica false")
                    ],
                    [   InlineKeyboardButton("Send Broadcast Msg", callback_data="sendToAll")
                    ]
                ]
            )
        if message.photo:
            await client.send_photo(
                message.chat.id, 
                photo=message.photo.file_id,
                file_ref=message.photo.file_ref,
                caption=message.caption.html,
                reply_markup=buttons
                )
        else:
            await client.send_message(
                message.chat.id,
                text = message.text.html,
                reply_markup=buttons
            )
        await m.delete()

@customClient.on_callback_query(customClient.CBFilter("notifica"))
async def CBQNotificaReverse(client : customClient, cbq):
    inLineKeyArray = []
    for row in cbq.message.reply_markup.inline_keyboard:
        newrow = []
        for button in row:
            if button.text.lower().startswith("notifica"):
                newrow.append(client.invertCBQBool(button))
                continue
            newrow.append(button)
        inLineKeyArray.append(newrow)
    await cbq.edit_message_reply_markup(reply_markup = InlineKeyboardMarkup(inLineKeyArray))


@customClient.on_callback_query(customClient.CBFilter("fix"))
async def CBQFissaReverse(client, cbq):
    inLineKeyArray = []
    for row in cbq.message.reply_markup.inline_keyboard:
        newrow = []
        for button in row:
            if button.text.lower().startswith("fissa"):
                newrow.append(client.invertCBQBool(button))
                continue
            newrow.append(button)
        inLineKeyArray.append(newrow)
    await cbq.edit_message_reply_markup(reply_markup = InlineKeyboardMarkup(inLineKeyArray))



@customClient.on_callback_query(customClient.CBFilter("sendToAll"))
async def CBQSendBroadcastMessage(client : customClient, cbq):
    staffdb = client.connection["chatlist"]
    cursor = staffdb.find({"type": "supergroup"})
    fissa = cbq.message.reply_markup.inline_keyboard[0][0].callback_data.split(" ", 1)[1]
    notifica = cbq.message.reply_markup.inline_keyboard[0][1].callback_data.split(" ", 1)[1]
    for document in cursor:
        message = None
        if cbq.message.photo:
            message = await client.send_photo(
                    document['id'], 
                    photo=cbq.message.photo.file_id,
                    file_ref=cbq.message.photo.file_ref,
                    caption=cbq.message.caption.html
                )
        else:
            message = await client.send_message(document['id'], cbq.message.text.html)
        if fissa == "true":
            if notifica == "false":
                await message.pin(True)
            else:
                await message.pin()
    await cbq.edit_message_text("Sending Message...")
