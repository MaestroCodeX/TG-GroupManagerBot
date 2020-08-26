from pyrogram import Filters, InlineKeyboardMarkup, InlineKeyboardButton
from ..customClient import customClient

@customClient.on_message(Filters.group & Filters.command(["permissions", "permessi"], ['/', '.']))
async def openPermSettings(client, message):
    user = await client.get_chat_member(message.chat.id, message.from_user.id)
    if user.can_promote_members and message.reply_to_message != None:
        permission = client.connection["userPermission"]
        userID = message.reply_to_message.from_user.id
        userExist = permission.count_documents({'userID': userID}) != 0
        await sendTextButton(permission, message, message.reply_to_message.from_user, userExist)

# Manda il tasto per settare i permessi
async def sendTextButton(dbTable, message, user, alreadyExist):
    canFix = False
    if alreadyExist:
        find = dbTable.find_one({"userID": user.id})
        array = find['pinPerm']
        if message.chat.id in array:
            canFix = True
    markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text=f"Fix {'✅' if canFix else '❌'}",
                                     callback_data=f"pin {'true' if canFix else 'false'}")
            ],
            [
                InlineKeyboardButton(text="Save and Quit",
                                     callback_data=f"savePerm {user.id}")
            ]
        ])
    await message.reply_text(f"Permission of {user.mention}\nMenù opened by {message.from_user.mention}", reply_markup=markup)


@customClient.on_callback_query(customClient.CBFilter("pin"))
async def CBQPin(client : customClient, cbq):
    if cbq.message.text.markdown.split('tg://user?id=')[-1][:-1] != str(cbq.from_user.id):
        await cbq.answer("It's not for You!", show_alert=True)
        return
    inLineKeyArray = []
    for row in cbq.message.reply_markup.inline_keyboard:
        newrow = []
        for button in row:
            if button.text.startswith("Fix"):
                newrow.append(client.invertCBQBool(button))
                continue
            newrow.append(button)
        inLineKeyArray.append(newrow)
    await cbq.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(inLineKeyArray))


@customClient.on_callback_query(customClient.CBFilter("savePerm"))
async def CBQSavePerm(client : customClient, cbq):
    if cbq.message.text.markdown.split('tg://user?id=')[-1][:-1] != str(cbq.from_user.id):
        await cbq.answer("It's not for You!", show_alert=True)
        return
    canFix = cbq.message.reply_markup.inline_keyboard[0][0].callback_data.split(" ", 1)[
        1] == "true"
    userID = int(cbq.data.split()[-1])
    permission = client.connection["userPermission"]

    if permission.count_documents({'userID': userID}) == 0:
        if canFix:
            permission.insert(createNewIstanceOfUser(
                userID, cbq.message.chat.id))
    else:
        if canFix:
            permission.update({'userID': userID}, {'$addToSet': {
                              "pinPerm": cbq.message.chat.id}})
        else:
            permission.update({'userID': userID}, {
                              '$pull': {"pinPerm": cbq.message.chat.id}})
            checkEmpty(permission, userID)
    await cbq.edit_message_text("Done!")


def checkEmpty(dbcon, id):
    userinfo = dbcon.find_one({'userID': id})
    if not userinfo["pinPerm"]:
        dbcon.delete_one({'userID': id})


def createNewIstanceOfUser(userID, groupId):
    obj = {
        'userID': userID,
        'pinPerm': [groupId]
    }
    return obj
