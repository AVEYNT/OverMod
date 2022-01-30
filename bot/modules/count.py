<<<<<<< HEAD
# Implement By - @anasty17 (https://github.com/breakdowns/slam-tg-mirror-bot/pull/111)
# (c) https://github.com/breakdowns/slam-tg-mirror-bot
# All rights reserved

from telegram.ext import CommandHandler
=======
from telegram.ext import CommandHandler

from bot import dispatcher
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
from bot.helper.mirror_utils.upload_utils.gdriveTools import GoogleDriveHelper
from bot.helper.telegram_helper.message_utils import deleteMessage, sendMessage
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands
<<<<<<< HEAD
from bot import dispatcher


def countNode(update, context):
    args = update.message.text.split(" ", maxsplit=1)
    if len(args) > 1:
        link = args[1]
        msg = sendMessage(f"Menghitung: <code>{link}</code>", context.bot, update)
        gd = GoogleDriveHelper()
        result = gd.count(link)
        deleteMessage(context.bot, msg)
        if update.message.from_user.username:
            uname = f'@{update.message.from_user.username}'
        else:
            uname = f'<a href="tg://user?id={update.message.from_user.id}">{update.message.from_user.first_name}</a>'
        if uname is not None:
            cc = f'\n\n👤Pengecek: {uname}'
        sendMessage(result + cc, context.bot, update)
    else:
        sendMessage("Berikan Tautan yang Dapat Dibagikan G-Drive untuk Menghitung.", context.bot, update)
=======
from bot.helper.ext_utils.bot_utils import is_gdrive_link, is_gdtot_link, new_thread
from bot.helper.mirror_utils.download_utils.direct_link_generator import gdtot
from bot.helper.ext_utils.exceptions import DirectDownloadLinkException

@new_thread
def countNode(update, context):
    args = update.message.text.split(" ", maxsplit=1)
    reply_to = update.message.reply_to_message
    if len(args) > 1:
        link = args[1]
        if update.message.from_user.username:
            tag = f"@{update.message.from_user.username}"
        else:
            tag = update.message.from_user.mention_html(update.message.from_user.first_name)
    elif reply_to is not None:
        link = reply_to.text
        if reply_to.from_user.username:
            tag = f"@{reply_to.from_user.username}"
        else:
            tag = reply_to.from_user.mention_html(reply_to.from_user.first_name)
    else:
        link = ''
    gdtot_link = is_gdtot_link(link)
    if gdtot_link:
        try:
            link = gdtot(link)
        except DirectDownloadLinkException as e:
            return sendMessage(str(e), context.bot, update)
    if is_gdrive_link(link):
        msg = sendMessage(f"Counting: <code>{link}</code>", context.bot, update)
        gd = GoogleDriveHelper()
        result = gd.count(link)
        deleteMessage(context.bot, msg)
        cc = f'\n\n<b>cc: </b>{tag}'
        sendMessage(result + cc, context.bot, update)
        if gdtot_link:
            gd.deletefile(link)
    else:
        sendMessage('Send Gdrive link along with command or by replying to the link by command', context.bot, update)
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9

count_handler = CommandHandler(BotCommands.CountCommand, countNode, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
dispatcher.add_handler(count_handler)
