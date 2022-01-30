<<<<<<< HEAD
import io
import os
# Common imports for eval
import textwrap
import traceback
from contextlib import redirect_stdout
=======
import os

from os import path as ospath, getcwd, chdir
from traceback import format_exc
from textwrap import indent
from io import StringIO, BytesIO
from telegram import ParseMode
from telegram.ext import CommandHandler
from contextlib import redirect_stdout

>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.message_utils import sendMessage
from bot import LOGGER, dispatcher
<<<<<<< HEAD
from telegram import ParseMode
from telegram.ext import CommandHandler

namespaces = {}


=======

namespaces = {}

>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
def namespace_of(chat, update, bot):
    if chat not in namespaces:
        namespaces[chat] = {
            '__builtins__': globals()['__builtins__'],
            'bot': bot,
            'effective_message': update.effective_message,
            'effective_user': update.effective_user,
            'effective_chat': update.effective_chat,
            'update': update
        }

    return namespaces[chat]

<<<<<<< HEAD

=======
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
def log_input(update):
    user = update.effective_user.id
    chat = update.effective_chat.id
    LOGGER.info(
        f"IN: {update.effective_message.text} (user={user}, chat={chat})")

<<<<<<< HEAD

def send(msg, bot, update):
    if len(str(msg)) > 2000:
        with io.BytesIO(str.encode(msg)) as out_file:
=======
def send(msg, bot, update):
    if len(str(msg)) > 2000:
        with BytesIO(str.encode(msg)) as out_file:
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
            out_file.name = "output.txt"
            bot.send_document(
                chat_id=update.effective_chat.id, document=out_file)
    else:
        LOGGER.info(f"OUT: '{msg}'")
        bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"`{msg}`",
            parse_mode=ParseMode.MARKDOWN)

<<<<<<< HEAD

=======
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
def evaluate(update, context):
    bot = context.bot
    send(do(eval, bot, update), bot, update)

<<<<<<< HEAD

=======
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
def execute(update, context):
    bot = context.bot
    send(do(exec, bot, update), bot, update)

<<<<<<< HEAD

=======
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
def cleanup_code(code):
    if code.startswith('```') and code.endswith('```'):
        return '\n'.join(code.split('\n')[1:-1])
    return code.strip('` \n')

<<<<<<< HEAD

=======
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
def do(func, bot, update):
    log_input(update)
    content = update.message.text.split(' ', 1)[-1]
    body = cleanup_code(content)
    env = namespace_of(update.message.chat_id, update, bot)

<<<<<<< HEAD
    os.chdir(os.getcwd())
    with open(
            os.path.join(os.getcwd(),
=======
    chdir(getcwd())
    with open(
            ospath.join(getcwd(),
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
                         'bot/modules/temp.txt'),
            'w') as temp:
        temp.write(body)

<<<<<<< HEAD
    stdout = io.StringIO()

    to_compile = f'def func():\n{textwrap.indent(body, "  ")}'
=======
    stdout = StringIO()

    to_compile = f'def func():\n{indent(body, "  ")}'
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9

    try:
        exec(to_compile, env)
    except Exception as e:
        return f'{e.__class__.__name__}: {e}'

    func = env['func']

    try:
        with redirect_stdout(stdout):
            func_return = func()
    except Exception as e:
        value = stdout.getvalue()
<<<<<<< HEAD
        return f'{value}{traceback.format_exc()}'
=======
        return f'{value}{format_exc()}'
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
    else:
        value = stdout.getvalue()
        result = None
        if func_return is None:
            if value:
                result = f'{value}'
            else:
                try:
                    result = f'{repr(eval(body, env))}'
                except:
                    pass
        else:
            result = f'{value}{func_return}'
        if result:
            return result

<<<<<<< HEAD

=======
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
def clear(update, context):
    bot = context.bot
    log_input(update)
    global namespaces
    if update.message.chat_id in namespaces:
        del namespaces[update.message.chat_id]
    send("Cleared locals.", bot, update)

<<<<<<< HEAD

=======
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
def exechelp(update, context):
    help_string = '''
<b>Executor</b>
• /eval <i>Run Python Code Line | Lines</i>
• /exec <i>Run Commands In Exec</i>
• /clearlocals <i>Cleared locals</i>
'''
    sendMessage(help_string, context.bot, update)


EVAL_HANDLER = CommandHandler(('eval'), evaluate, filters=CustomFilters.owner_filter, run_async=True)
EXEC_HANDLER = CommandHandler(('exec'), execute, filters=CustomFilters.owner_filter, run_async=True)
CLEAR_HANDLER = CommandHandler('clearlocals', clear, filters=CustomFilters.owner_filter, run_async=True)
EXECHELP_HANDLER = CommandHandler(BotCommands.ExecHelpCommand, exechelp, filters=CustomFilters.owner_filter, run_async=True)

dispatcher.add_handler(EVAL_HANDLER)
dispatcher.add_handler(EXEC_HANDLER)
dispatcher.add_handler(CLEAR_HANDLER)
dispatcher.add_handler(EXECHELP_HANDLER)
