<<<<<<< HEAD
from telegram.ext import CommandHandler
from bot import dispatcher, status_reply_dict, status_reply_dict_lock, download_dict, download_dict_lock
from bot.helper.telegram_helper.message_utils import *
from telegram.error import BadRequest
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands
import threading
=======
from psutil import cpu_percent, virtual_memory, disk_usage
from time import time
from threading import Thread
from telegram.ext import CommandHandler, CallbackQueryHandler

from bot import dispatcher, status_reply_dict, status_reply_dict_lock, download_dict, download_dict_lock, botStartTime
from bot.helper.telegram_helper.message_utils import sendMessage, deleteMessage, auto_delete_message, sendStatusMessage, update_all_messages
from bot.helper.ext_utils.bot_utils import get_readable_file_size, get_readable_time, turn
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9


def mirror_status(update, context):
    with download_dict_lock:
        if len(download_dict) == 0:
<<<<<<< HEAD
            message = "Tidak ada unduhan aktif"
            reply_message = sendMessage(message, context.bot, update)
            threading.Thread(target=auto_delete_message, args=(bot, update.message, reply_message)).start()
=======
            currentTime = get_readable_time(time() - botStartTime)
            total, used, free, _ = disk_usage('.')
            free = get_readable_file_size(free)
            message = 'No Active Downloads !\n___________________________'
            message += f"\n<b>CPU:</b> {cpu_percent()}% | <b>FREE:</b> {free}" \
                       f"\n<b>RAM:</b> {virtual_memory().percent}% | <b>UPTIME:</b> {currentTime}"
            reply_message = sendMessage(message, context.bot, update)
            Thread(target=auto_delete_message, args=(context.bot, update.message, reply_message)).start()
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
            return
    index = update.effective_chat.id
    with status_reply_dict_lock:
        if index in status_reply_dict.keys():
<<<<<<< HEAD
            deleteMessage(bot, status_reply_dict[index])
=======
            deleteMessage(context.bot, status_reply_dict[index])
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
            del status_reply_dict[index]
    sendStatusMessage(update, context.bot)
    deleteMessage(context.bot, update.message)

<<<<<<< HEAD

mirror_status_handler = CommandHandler(BotCommands.StatusCommand, mirror_status,
                                       filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
dispatcher.add_handler(mirror_status_handler)
=======
def status_pages(update, context):
    query = update.callback_query
    data = query.data
    data = data.split(' ')
    query.answer()
    done = turn(data)
    if done:
        update_all_messages()
    else:
        query.message.delete()


mirror_status_handler = CommandHandler(BotCommands.StatusCommand, mirror_status,
                                       filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)

status_pages_handler = CallbackQueryHandler(status_pages, pattern="status", run_async=True)
dispatcher.add_handler(mirror_status_handler)
dispatcher.add_handler(status_pages_handler)
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
