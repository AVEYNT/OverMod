<<<<<<< HEAD
from telegram.ext import CommandHandler
import threading
from telegram import Update
=======
from threading import Thread
from telegram import Update
from telegram.ext import CommandHandler

>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
from bot import dispatcher, LOGGER
from bot.helper.telegram_helper.message_utils import auto_delete_message, sendMessage
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.mirror_utils.upload_utils import gdriveTools
<<<<<<< HEAD


def deletefile(update, context):
	msg_args = update.message.text.split(None, 1)
	msg = ''
	try:
		link = msg_args[1]
		LOGGER.info(link)
	except IndexError:
		msg = 'Kirim tautan bersama dengan perintah'

	if msg == '' : 
		drive = gdriveTools.GoogleDriveHelper()
		msg = drive.deletefile(link)
	LOGGER.info(f"DeleteFileCmd: {msg}")
	reply_message = sendMessage(msg, context.bot, update)

	threading.Thread(target=auto_delete_message, args=(context.bot, update.message, reply_message)).start()
=======
from bot.helper.ext_utils.bot_utils import is_gdrive_link


def deletefile(update, context):
    args = update.message.text.split(" ", maxsplit=1)
    reply_to = update.message.reply_to_message
    if len(args) > 1:
        link = args[1]
    elif reply_to is not None:
        link = reply_to.text
    else:
        link = ''
    if is_gdrive_link(link):
        LOGGER.info(link)
        drive = gdriveTools.GoogleDriveHelper()
        msg = drive.deletefile(link)
    else:
        msg = 'Send Gdrive link along with command or by replying to the link by command'
    reply_message = sendMessage(msg, context.bot, update)
    Thread(target=auto_delete_message, args=(context.bot, update.message, reply_message)).start()
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9

delete_handler = CommandHandler(command=BotCommands.DeleteCommand, callback=deletefile, filters=CustomFilters.owner_filter | CustomFilters.sudo_user, run_async=True)
dispatcher.add_handler(delete_handler)
