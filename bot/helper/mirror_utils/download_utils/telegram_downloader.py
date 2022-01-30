import logging
<<<<<<< HEAD
import threading
import time
from bot import LOGGER, download_dict, download_dict_lock, app, STOP_DUPLICATE
from .download_helper import DownloadHelper
=======

from time import time
from threading import RLock, Lock, Thread

from bot import LOGGER, download_dict, download_dict_lock, app, STOP_DUPLICATE
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
from ..status_utils.telegram_download_status import TelegramDownloadStatus
from bot.helper.telegram_helper.message_utils import sendMarkup, sendStatusMessage
from bot.helper.mirror_utils.upload_utils.gdriveTools import GoogleDriveHelper

<<<<<<< HEAD
global_lock = threading.Lock()
=======
global_lock = Lock()
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
GLOBAL_GID = set()
logging.getLogger("pyrogram").setLevel(logging.WARNING)


<<<<<<< HEAD
class TelegramDownloadHelper(DownloadHelper):
    def __init__(self, listener):
        super().__init__()
        self.__listener = listener
        self.__resource_lock = threading.RLock()
        self.__name = ""
        self.__start_time = time.time()
        self.__gid = ""
        self._bot = app
        self.__is_cancelled = False

    @property
    def gid(self):
        with self.__resource_lock:
            return self.__gid
=======
class TelegramDownloadHelper:
    def __init__(self, listener):
        self.name = ""
        self.size = 0
        self.progress = 0
        self.downloaded_bytes = 0
        self.__start_time = time()
        self.__listener = listener
        self.__gid = ""
        self.__user_bot = app
        self.__is_cancelled = False
        self.__resource_lock = RLock()
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9

    @property
    def download_speed(self):
        with self.__resource_lock:
<<<<<<< HEAD
            return self.downloaded_bytes / (time.time() - self.__start_time)

    def __onDownloadStart(self, name, size, file_id):
        with download_dict_lock:
            download_dict[self.__listener.uid] = TelegramDownloadStatus(self, self.__listener)
=======
            return self.downloaded_bytes / (time() - self.__start_time)

    def __onDownloadStart(self, name, size, file_id):
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
        with global_lock:
            GLOBAL_GID.add(file_id)
        with self.__resource_lock:
            self.name = name
            self.size = size
            self.__gid = file_id
<<<<<<< HEAD
        self.__listener.onDownloadStarted()
=======
        with download_dict_lock:
            download_dict[self.__listener.uid] = TelegramDownloadStatus(self, self.__listener, file_id)
        sendStatusMessage(self.__listener.update, self.__listener.bot)
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9

    def __onDownloadProgress(self, current, total):
        if self.__is_cancelled:
            self.__onDownloadError('Cancelled by user!')
<<<<<<< HEAD
            self._bot.stop_transmission()
=======
            self.__user_bot.stop_transmission()
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
            return
        with self.__resource_lock:
            self.downloaded_bytes = current
            try:
                self.progress = current / self.size * 100
            except ZeroDivisionError:
<<<<<<< HEAD
                self.progress = 0
=======
                pass
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9

    def __onDownloadError(self, error):
        with global_lock:
            try:
<<<<<<< HEAD
                GLOBAL_GID.remove(self.gid)
=======
                GLOBAL_GID.remove(self.__gid)
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
            except KeyError:
                pass
        self.__listener.onDownloadError(error)

    def __onDownloadComplete(self):
        with global_lock:
<<<<<<< HEAD
            GLOBAL_GID.remove(self.gid)
        self.__listener.onDownloadComplete()

    def __download(self, message, path):
        download = self._bot.download_media(
            message,
            progress = self.__onDownloadProgress,
            file_name = path
        )
=======
            GLOBAL_GID.remove(self.__gid)
        self.__listener.onDownloadComplete()

    def __download(self, message, path):
        try:
            download = self.__user_bot.download_media(message,
                                                progress = self.__onDownloadProgress,
                                                file_name = path
                                               )
        except Exception as e:
            LOGGER.error(str(e))
            return self.__onDownloadError(str(e))
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
        if download is not None:
            self.__onDownloadComplete()
        elif not self.__is_cancelled:
            self.__onDownloadError('Internal error occurred')

    def add_download(self, message, path, filename):
<<<<<<< HEAD
        _message = self._bot.get_messages(message.chat.id, reply_to_message_ids=message.message_id)
=======
        _message = self.__user_bot.get_messages(message.chat.id, reply_to_message_ids=message.message_id)
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
        media = None
        media_array = [_message.document, _message.video, _message.audio]
        for i in media_array:
            if i is not None:
                media = i
                break
        if media is not None:
            with global_lock:
                # For avoiding locking the thread lock for long time unnecessarily
                download = media.file_id not in GLOBAL_GID
            if filename == "":
                name = media.file_name
            else:
                name = filename
                path = path + name

            if download:
                if STOP_DUPLICATE and not self.__listener.isLeech:
                    LOGGER.info('Checking File/Folder if already in Drive...')
<<<<<<< HEAD
                    gd = GoogleDriveHelper()
                    smsg, button = gd.drive_list(name, True, True)
                    if smsg:
                        sendMarkup("File/Folder is already available in Drive.\nHere are the search results:", self.__listener.bot, self.__listener.update, button)
                        return
                sendStatusMessage(self.__listener.update, self.__listener.bot)
                self.__onDownloadStart(name, media.file_size, media.file_id)
                LOGGER.info(f'Downloading Telegram file with id: {media.file_id}')
                threading.Thread(target=self.__download, args=(_message, path)).start()
=======
                    smsg, button = GoogleDriveHelper().drive_list(name, True, True)
                    if smsg:
                        msg = "File/Folder is already available in Drive.\nHere are the search results:"
                        return sendMarkup(msg, self.__listener.bot, self.__listener.update, button)
                self.__onDownloadStart(name, media.file_size, media.file_id)
                LOGGER.info(f'Downloading Telegram file with id: {media.file_id}')
                Thread(target=self.__download, args=(_message, path)).start()
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
            else:
                self.__onDownloadError('File already being downloaded!')
        else:
            self.__onDownloadError('No document in the replied message')

    def cancel_download(self):
<<<<<<< HEAD
        LOGGER.info(f'Cancelling download on user request: {self.gid}')
=======
        LOGGER.info(f'Cancelling download on user request: {self.__gid}')
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
        self.__is_cancelled = True
