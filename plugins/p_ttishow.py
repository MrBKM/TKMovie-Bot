from pyrogram import Client, filters, enums 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong, PeerIdInvalid
from info import ADMINS, LOG_CHANNEL, SUPPORT_CHAT, MELCOW_NEW_USERS
from database.users_chats_db import db
from database.ia_filterdb import Media
from utils import get_size, temp, get_settings
from script import Script
from pyrogram.errors import ChatAdminRequired

"""-----------------------------------------https://t.me/TechMasterz--------------------------------------"""


@Client.on_message(filters.command('stats') & filters.incoming & filters.user(ADMINS))
async def get_ststs(bot, message):
    rju = await message.reply('Fetching DB Stats..')
    total_users = await db.total_users_count()
    totl_chats = await db.total_chat_count()
    files = await Media.count_documents()
    size = await db.get_db_size()
    free = 536870912 - size
    size = get_size(size)
    free = get_size(free)
    await rju.edit(Script.STATUS_TXT.format(files, total_users, totl_chats, size, free))


@Client.on_message(filters.command('users') & filters.user(ADMINS))
async def list_users(bot, message):
    # വാഴ മരത്തെ കളിയാക്കിയവർ തന്നെ പേടിച്ചു ഓടിപ്പോയി
    sps = await message.reply('Getting List Of Users')
    users = await db.get_all_users()
    out = "Users Saved In DB Are:\n\n"
    async for user in users:
        out += f"<a href=tg://user?id={user['id']}>{user['name']}</a>\n"
    try:
        await sps.edit_text(out)
    except MessageTooLong:
        with open('users.txt', 'w+') as outfile:
            outfile.write(out)
        await message.reply_document('users.txt', caption="List Of Users")

@Client.on_message(filters.command('chats') & filters.user(ADMINS))
async def list_chats(bot, message):
    sps = await message.reply('Getting List Of chats')
    chats = await db.get_all_chats()
    out = "Chats Saved In DB Are:\n\n"
    async for chat in chats:
        username = chat['username']
        username = "private" if not username else "@" + username
        out += f"**- Title:** `{chat['title']}`\n**- ID:** `{chat['id']}`\n**Username:** {username}\n"
    try:
        await sps.edit_text(out)
    except MessageTooLong:
        with open('chats.txt', 'w+') as outfile:
            outfile.write(out)
        await message.reply_document('chats.txt', caption="List Of Chats")
