<<<<<<< HEAD
import subprocess
from bot import LOGGER, dispatcher
from telegram import ParseMode
from telegram.ext import CommandHandler
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands
=======
from subprocess import run
from telegram import ParseMode
from telegram.ext import CommandHandler

from bot import LOGGER, dispatcher
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.message_utils import sendMessage
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9


def shell(update, context):
    message = update.effective_message
    cmd = message.text.split(' ', 1)
    if len(cmd) == 1:
<<<<<<< HEAD
        message.reply_text('No command to execute was given.')
        return
    cmd = cmd[1]
    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()
    reply = ''
    stderr = stderr.decode()
    stdout = stdout.decode()
    if stdout:
        reply += f"*Stdout*\n`{stdout}`\n"
        LOGGER.info(f"Shell - {cmd} - {stdout}")
    if stderr:
        reply += f"*Stderr*\n`{stderr}`\n"
=======
        return sendMessage('No command to execute was given.', context.bot, update)
    cmd = cmd[1]
    process = run(cmd, capture_output=True, shell=True)
    reply = ''
    stderr = process.stderr.decode('utf-8')
    stdout = process.stdout.decode('utf-8')
    if len(stdout) != 0:
        reply += f"*Stdout*\n<code>{stdout}</code>\n"
        LOGGER.info(f"Shell - {cmd} - {stdout}")
    if len(stderr) != 0:
        reply += f"*Stderr*\n<code>{stderr}</code>\n"
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
        LOGGER.error(f"Shell - {cmd} - {stderr}")
    if len(reply) > 3000:
        with open('shell_output.txt', 'w') as file:
            file.write(reply)
        with open('shell_output.txt', 'rb') as doc:
            context.bot.send_document(
                document=doc,
                filename=doc.name,
                reply_to_message_id=message.message_id,
                chat_id=message.chat_id)
<<<<<<< HEAD
    else:
        message.reply_text(reply, parse_mode=ParseMode.MARKDOWN)


SHELL_HANDLER = CommandHandler(BotCommands.ShellCommand, shell, 
=======
    elif len(reply) != 0:
        sendMessage(reply, context.bot, update)
    else:
        sendMessage('No Reply', context.bot, update)


SHELL_HANDLER = CommandHandler(BotCommands.ShellCommand, shell,
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
                                                  filters=CustomFilters.owner_filter, run_async=True)
dispatcher.add_handler(SHELL_HANDLER)
