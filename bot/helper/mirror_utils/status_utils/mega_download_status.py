from bot.helper.ext_utils.bot_utils import get_readable_file_size,MirrorStatus, get_readable_time
from bot import DOWNLOAD_DIR
<<<<<<< HEAD
from .status import Status


class MegaDownloadStatus(Status):

    def __init__(self, obj, listener):
        self.uid = obj.uid
        self.listener = listener
        self.obj = obj
        self.message = listener.message

    def name(self) -> str:
        return self.obj.name

    def progress_raw(self):
        try:
            return round(self.processed_bytes() / self.obj.size * 100,2)
=======


class MegaDownloadStatus:

    def __init__(self, obj, listener):
        self.__uid = obj.uid
        self.__listener = listener
        self.__obj = obj
        self.message = listener.message

    def name(self) -> str:
        return self.__obj.name

    def progress_raw(self):
        try:
            return round(self.processed_bytes() / self.__obj.size * 100,2)
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
        except ZeroDivisionError:
            return 0.0

    def progress(self):
        """Progress of download in percentage"""
        return f"{self.progress_raw()}%"

    def status(self) -> str:
        return MirrorStatus.STATUS_DOWNLOADING

    def processed_bytes(self):
<<<<<<< HEAD
        return self.obj.downloaded_bytes
=======
        return self.__obj.downloaded_bytes
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9

    def eta(self):
        try:
            seconds = (self.size_raw() - self.processed_bytes()) / self.speed_raw()
            return f'{get_readable_time(seconds)}'
        except ZeroDivisionError:
            return '-'

    def size_raw(self):
<<<<<<< HEAD
        return self.obj.size
=======
        return self.__obj.size
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9

    def size(self) -> str:
        return get_readable_file_size(self.size_raw())

    def downloaded(self) -> str:
<<<<<<< HEAD
        return get_readable_file_size(self.obj.downloadedBytes)

    def speed_raw(self):
        return self.obj.speed

    def speed(self) -> str:
        return f'{get_readable_file_size(self.speed_raw())}/s' 

    def gid(self) -> str:
        return self.obj.gid

    def path(self) -> str:
        return f"{DOWNLOAD_DIR}{self.uid}"

    def download(self):
        return self.obj
=======
        return get_readable_file_size(self.__obj.downloadedBytes)

    def speed_raw(self):
        return self.__obj.speed

    def speed(self) -> str:
        return f'{get_readable_file_size(self.speed_raw())}/s'

    def gid(self) -> str:
        return self.__obj.gid

    def path(self) -> str:
        return f"{DOWNLOAD_DIR}{self.__uid}"

    def download(self):
        return self.__obj
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
