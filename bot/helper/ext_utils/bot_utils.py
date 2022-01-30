<<<<<<< HEAD
import logging
import re
import threading
import time
import math

from bot.helper.telegram_helper.bot_commands import BotCommands
from bot import dispatcher, download_dict, download_dict_lock, STATUS_LIMIT
from telegram import InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler
from bot.helper.telegram_helper import button_build, message_utils

LOGGER = logging.getLogger(__name__)
=======
from re import match, findall
from threading import Thread, Event
from time import time
from math import ceil
from psutil import virtual_memory, cpu_percent, disk_usage
from requests import head as rhead
from urllib.request import urlopen
from telegram import InlineKeyboardMarkup

from bot.helper.telegram_helper.bot_commands import BotCommands
from bot import download_dict, download_dict_lock, STATUS_LIMIT, botStartTime
from bot.helper.telegram_helper.button_build import ButtonMaker
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9

MAGNET_REGEX = r"magnet:\?xt=urn:btih:[a-zA-Z0-9]*"

URL_REGEX = r"(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+"

COUNT = 0
PAGE_NO = 1


class MirrorStatus:
<<<<<<< HEAD
    STATUS_UPLOADING = "Mengunggah...📤"
    STATUS_DOWNLOADING = "Mengunduh...📥"
    STATUS_CLONING = "Kloning...♻️"
    STATUS_WAITING = "Antri...📝"
    STATUS_FAILED = "Gagal 🚫. Cleaning Download..."
    STATUS_PAUSE = "Dijeda...⭕️"
    STATUS_ARCHIVING = "Pengarsipan...🔐"
    STATUS_EXTRACTING = "Mengekstraksi...📂"
    STATUS_SPLITTING = "Pemisahan...✂️"


PROGRESS_MAX_SIZE = 100 // 8
PROGRESS_INCOMPLETE = ['▏', '▎', '▍', '▌', '▋', '▊', '▉']
=======
    STATUS_UPLOADING = "Uploading...📤"
    STATUS_DOWNLOADING = "Downloading...📥"
    STATUS_CLONING = "Cloning...♻️"
    STATUS_WAITING = "Queued...💤"
    STATUS_FAILED = "Failed 🚫. Cleaning Download..."
    STATUS_PAUSE = "Paused...⛔️"
    STATUS_ARCHIVING = "Archiving...🔐"
    STATUS_EXTRACTING = "Extracting...📂"
    STATUS_SPLITTING = "Splitting...✂️"
    STATUS_CHECKING = "CheckingUp...📝"
    STATUS_SEEDING = "Seeding...🌧"
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9

SIZE_UNITS = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']


class setInterval:
    def __init__(self, interval, action):
        self.interval = interval
        self.action = action
<<<<<<< HEAD
        self.stopEvent = threading.Event()
        thread = threading.Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self):
        nextTime = time.time() + self.interval
        while not self.stopEvent.wait(nextTime - time.time()):
=======
        self.stopEvent = Event()
        thread = Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self):
        nextTime = time() + self.interval
        while not self.stopEvent.wait(nextTime - time()):
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
            nextTime += self.interval
            self.action()

    def cancel(self):
        self.stopEvent.set()

def get_readable_file_size(size_in_bytes) -> str:
    if size_in_bytes is None:
        return '0B'
    index = 0
    while size_in_bytes >= 1024:
        size_in_bytes /= 1024
        index += 1
    try:
        return f'{round(size_in_bytes, 2)}{SIZE_UNITS[index]}'
    except IndexError:
        return 'File too large'

def getDownloadByGid(gid):
    with download_dict_lock:
<<<<<<< HEAD
        for dl in download_dict.values():
=======
        for dl in list(download_dict.values()):
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
            status = dl.status()
            if (
                status
                not in [
                    MirrorStatus.STATUS_ARCHIVING,
                    MirrorStatus.STATUS_EXTRACTING,
                    MirrorStatus.STATUS_SPLITTING,
                ]
                and dl.gid() == gid
            ):
                return dl
    return None

def getAllDownload():
    with download_dict_lock:
<<<<<<< HEAD
        for dlDetails in download_dict.values():
=======
        for dlDetails in list(download_dict.values()):
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
            status = dlDetails.status()
            if (
                status
                not in [
                    MirrorStatus.STATUS_ARCHIVING,
                    MirrorStatus.STATUS_EXTRACTING,
                    MirrorStatus.STATUS_SPLITTING,
                    MirrorStatus.STATUS_CLONING,
                    MirrorStatus.STATUS_UPLOADING,
<<<<<<< HEAD
=======
                    MirrorStatus.STATUS_CHECKING,
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
                ]
                and dlDetails
            ):
                return dlDetails
    return None

def get_progress_bar_string(status):
    completed = status.processed_bytes() / 8
    total = status.size_raw() / 8
    p = 0 if total == 0 else round(completed * 100 / total)
    p = min(max(p, 0), 100)
    cFull = p // 8
<<<<<<< HEAD
    cPart = p % 8 - 1
    p_str = '█' * cFull
    if cPart >= 0:
        p_str += PROGRESS_INCOMPLETE[cPart]
    p_str += ' ' * (PROGRESS_MAX_SIZE - cFull)
=======
    p_str = '■' * cFull
    p_str += '□' * (12 - cFull)
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
    p_str = f"[{p_str}]"
    return p_str

def get_readable_message():
    with download_dict_lock:
        msg = ""
<<<<<<< HEAD
        start = 0
        if STATUS_LIMIT is not None:
            dick_no = len(download_dict)
            global pages
            pages = math.ceil(dick_no/STATUS_LIMIT)
            if PAGE_NO > pages and pages != 0:
                globals()['COUNT'] -= STATUS_LIMIT
                globals()['PAGE_NO'] -= 1
            start = COUNT
        for index, download in enumerate(list(download_dict.values())[start:], start=1):
            msg += f"<b>🗂Nama:</b> <code>{download.name()}</code>"
            msg += f"\n<b>♻️Status:</b> <i>{download.status()}</i>"
=======
        dlspeed_bytes = 0
        uldl_bytes = 0
        START = 0
        if STATUS_LIMIT is not None:
            tasks = len(download_dict)
            global pages
            pages = ceil(tasks/STATUS_LIMIT)
            if PAGE_NO > pages and pages != 0:
                globals()['COUNT'] -= STATUS_LIMIT
                globals()['PAGE_NO'] -= 1
            START = COUNT
        for index, download in enumerate(list(download_dict.values())[START:], start=1):
            msg += f"<b>Name:</b> <code>{download.name()}</code>"
            msg += f"\n<b>Status:</b> <i>{download.status()}</i>"
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
            if download.status() not in [
                MirrorStatus.STATUS_ARCHIVING,
                MirrorStatus.STATUS_EXTRACTING,
                MirrorStatus.STATUS_SPLITTING,
<<<<<<< HEAD
            ]:
                msg += f"\n<code>{get_progress_bar_string(download)}</code> {download.progress()}"
                if download.status() == MirrorStatus.STATUS_CLONING:
                    msg += f"\n<b>📝Dikloning:</b> <code>{get_readable_file_size(download.processed_bytes())}</code> of <code>{download.size()}</code>"
                elif download.status() == MirrorStatus.STATUS_UPLOADING:
                    msg += f"\n<b>📤Diunggah:</b> <code>{get_readable_file_size(download.processed_bytes())}</code> of <code>{download.size()}</code>"
                else:
                    msg += f"\n<b>📥Diunduh:</b> <code>{get_readable_file_size(download.processed_bytes())}</code> of <code>{download.size()}</code>"
                msg += f"\n<b>🚀Kecepatan:</b> <code>{download.speed()}</code> <b>ETA:</b> <code>{download.eta()}</code>"
                try:
                    msg += f"\n<b>📲Seeders:</b> <code>{download.aria_download().num_seeders}</code>" \
                           f" | <b>📱Peers:</b> <code>{download.aria_download().connections}</code>"
                except:
                    pass
                try:
                    msg += f"\n<b>📲Seeders:</b> <code>{download.torrent_info().num_seeds}</code>" \
                           f" | <b>🧲Leechers:</b> <code>{download.torrent_info().num_leechs}</code>"
                except:
                    pass
                msg += f"\n<b>🔑Untuk Berhenti:</b> <code>/{BotCommands.CancelMirror} {download.gid()}</code>"
            msg += "\n\n"
            if STATUS_LIMIT is not None and index == STATUS_LIMIT:
                break
        if STATUS_LIMIT is not None and dick_no > STATUS_LIMIT:
            msg += f"<b>Halaman:</b> <code>{PAGE_NO}</code>/<code>{pages}</code> | <b>Tugas:</b> <code>{dick_no}</code>\n"
            buttons = button_build.ButtonMaker()
            buttons.sbutton("Sebelumnya", "pre")
            buttons.sbutton("Selanjutnya", "nex")
            button = InlineKeyboardMarkup(buttons.build_menu(2))
            return msg, button
        return msg, ""

def flip(update, context):
    query = update.callback_query
    query.answer()
    global COUNT, PAGE_NO
    if query.data == "nex":
        if PAGE_NO == pages:
            COUNT = 0
            PAGE_NO = 1
        else:
            COUNT += STATUS_LIMIT
            PAGE_NO += 1
    elif query.data == "pre":
        if PAGE_NO == 1:
            COUNT = STATUS_LIMIT * (pages - 1)
            PAGE_NO = pages
        else:
            COUNT -= STATUS_LIMIT
            PAGE_NO -= 1
    message_utils.update_all_messages()

def check_limit(size, limit, tar_unzip_limit=None, is_tar_ext=False):
    LOGGER.info('Checking File/Folder Size...')
    if is_tar_ext and tar_unzip_limit is not None:
        limit = tar_unzip_limit
    if limit is not None:
        limit = limit.split(' ', maxsplit=1)
        limitint = int(limit[0])
        if 'G' in limit[1] or 'g' in limit[1]:
            if size > limitint * 1024**3:
                return True
        elif 'T' in limit[1] or 't' in limit[1]:
            if size > limitint * 1024**4:
                return True
=======
                MirrorStatus.STATUS_SEEDING,
            ]:
                msg += f"\n{get_progress_bar_string(download)} {download.progress()}"
                if download.status() == MirrorStatus.STATUS_CLONING:
                    msg += f"\n<b>Cloned:</b> {get_readable_file_size(download.processed_bytes())} of {download.size()}"
                elif download.status() == MirrorStatus.STATUS_UPLOADING:
                    msg += f"\n<b>Uploaded:</b> {get_readable_file_size(download.processed_bytes())} of {download.size()}"
                else:
                    msg += f"\n<b>Downloaded:</b> {get_readable_file_size(download.processed_bytes())} of {download.size()}"
                msg += f"\n<b>Speed:</b> {download.speed()} | <b>ETA:</b> {download.eta()}"
                try:
                    msg += f"\n<b>Seeders:</b> {download.aria_download().num_seeders}" \
                           f" | <b>Peers:</b> {download.aria_download().connections}"
                except:
                    pass
                try:
                    msg += f"\n<b>Seeders:</b> {download.torrent_info().num_seeds}" \
                           f" | <b>Leechers:</b> {download.torrent_info().num_leechs}"
                except:
                    pass
                msg += f"\n<code>/{BotCommands.CancelMirror} {download.gid()}</code>"
            elif download.status() == MirrorStatus.STATUS_SEEDING:
                msg += f"\n<b>Size: </b>{download.size()}"
                msg += f"\n<b>Speed: </b>{get_readable_file_size(download.torrent_info().upspeed)}/s"
                msg += f" | <b>Uploaded: </b>{get_readable_file_size(download.torrent_info().uploaded)}"
                msg += f"\n<b>Ratio: </b>{round(download.torrent_info().ratio, 3)}"
                msg += f" | <b>Time: </b>{get_readable_time(download.torrent_info().seeding_time)}"
                msg += f"\n<code>/{BotCommands.CancelMirror} {download.gid()}</code>"
            else:
                msg += f"\n<b>Size: </b>{download.size()}"
            msg += "\n\n"
            if STATUS_LIMIT is not None and index == STATUS_LIMIT:
                break
        total, used, free, _ = disk_usage('.')
        free = get_readable_file_size(free)
        currentTime = get_readable_time(time() - botStartTime)
        bmsg = f"<b>CPU:</b> {cpu_percent()}% | <b>FREE:</b> {free}"
        for download in list(download_dict.values()):
            speedy = download.speed()
            if download.status() == MirrorStatus.STATUS_DOWNLOADING:
                if 'K' in speedy:
                    dlspeed_bytes += float(speedy.split('K')[0]) * 1024
                elif 'M' in speedy:
                    dlspeed_bytes += float(speedy.split('M')[0]) * 1048576
            if download.status() == MirrorStatus.STATUS_UPLOADING:
                if 'KB/s' in speedy:
                    uldl_bytes += float(speedy.split('K')[0]) * 1024
                elif 'MB/s' in speedy:
                    uldl_bytes += float(speedy.split('M')[0]) * 1048576
        dlspeed = get_readable_file_size(dlspeed_bytes)
        ulspeed = get_readable_file_size(uldl_bytes)
        bmsg += f"\n<b>RAM:</b> {virtual_memory().percent}% | <b>UPTIME:</b> {currentTime}"
        bmsg += f"\n<b>DL:</b> {dlspeed}/s | <b>UL:</b> {ulspeed}/s"
        if STATUS_LIMIT is not None and tasks > STATUS_LIMIT:
            msg += f"<b>Page:</b> {PAGE_NO}/{pages} | <b>Tasks:</b> {tasks}\n"
            buttons = ButtonMaker()
            buttons.sbutton("Previous", "status pre")
            buttons.sbutton("Next", "status nex")
            button = InlineKeyboardMarkup(buttons.build_menu(2))
            return msg + bmsg, button
        return msg + bmsg, ""

def turn(data):
    try:
        with download_dict_lock:
            global COUNT, PAGE_NO
            if data[1] == "nex":
                if PAGE_NO == pages:
                    COUNT = 0
                    PAGE_NO = 1
                else:
                    COUNT += STATUS_LIMIT
                    PAGE_NO += 1
            elif data[1] == "pre":
                if PAGE_NO == 1:
                    COUNT = STATUS_LIMIT * (pages - 1)
                    PAGE_NO = pages
                else:
                    COUNT -= STATUS_LIMIT
                    PAGE_NO -= 1
        return True
    except:
        return False
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9

def get_readable_time(seconds: int) -> str:
    result = ''
    (days, remainder) = divmod(seconds, 86400)
    days = int(days)
    if days != 0:
        result += f'{days}d'
    (hours, remainder) = divmod(remainder, 3600)
    hours = int(hours)
    if hours != 0:
        result += f'{hours}h'
    (minutes, seconds) = divmod(remainder, 60)
    minutes = int(minutes)
    if minutes != 0:
        result += f'{minutes}m'
    seconds = int(seconds)
    result += f'{seconds}s'
    return result

def is_url(url: str):
<<<<<<< HEAD
    url = re.findall(URL_REGEX, url)
=======
    url = findall(URL_REGEX, url)
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
    return bool(url)

def is_gdrive_link(url: str):
    return "drive.google.com" in url

<<<<<<< HEAD
=======
def is_gdtot_link(url: str):
    url = match(r'https?://.*\.gdtot\.\S+', url)
    return bool(url)

>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
def is_mega_link(url: str):
    return "mega.nz" in url or "mega.co.nz" in url

def get_mega_link_type(url: str):
    if "folder" in url:
        return "folder"
    elif "file" in url:
        return "file"
    elif "/#F!" in url:
        return "folder"
    return "file"

def is_magnet(url: str):
<<<<<<< HEAD
    magnet = re.findall(MAGNET_REGEX, url)
=======
    magnet = findall(MAGNET_REGEX, url)
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
    return bool(magnet)

def new_thread(fn):
    """To use as decorator to make a function call threaded.
    Needs import
    from threading import Thread"""

    def wrapper(*args, **kwargs):
<<<<<<< HEAD
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
=======
        thread = Thread(target=fn, args=args, kwargs=kwargs)
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
        thread.start()
        return thread

    return wrapper

<<<<<<< HEAD

next_handler = CallbackQueryHandler(flip, pattern="nex", run_async=True)
previous_handler = CallbackQueryHandler(flip, pattern="pre", run_async=True)
dispatcher.add_handler(next_handler)
dispatcher.add_handler(previous_handler)
=======
def get_content_type(link: str):
    try:
        res = rhead(link, allow_redirects=True, timeout=5)
        content_type = res.headers.get('content-type')
    except:
        content_type = None

    if content_type is None:
        try:
            res = urlopen(link, timeout=5)
            info = res.info()
            content_type = info.get_content_type()
        except:
            content_type = None
    return content_type

>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
