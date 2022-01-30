<<<<<<< HEAD
from .status import Status
=======
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
from bot.helper.ext_utils.bot_utils import MirrorStatus, get_readable_file_size, get_readable_time
from bot import DOWNLOAD_DIR


<<<<<<< HEAD
class UploadStatus(Status):
    def __init__(self, obj, size, gid, listener):
        self.obj = obj
        self.__size = size
        self.uid = listener.uid
        self.message = listener.message
        self.__gid = gid

    def path(self):
        return f"{DOWNLOAD_DIR}{self.uid}"

    def processed_bytes(self):
        return self.obj.uploaded_bytes
=======
class UploadStatus:
    def __init__(self, obj, size, gid, listener):
        self.__obj = obj
        self.__size = size
        self.__uid = listener.uid
        self.__gid = gid
        self.message = listener.message

    def path(self):
        return f"{DOWNLOAD_DIR}{self.__uid}"

    def processed_bytes(self):
        return self.__obj.uploaded_bytes
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9

    def size_raw(self):
        return self.__size

    def size(self):
        return get_readable_file_size(self.__size)

    def status(self):
        return MirrorStatus.STATUS_UPLOADING

    def name(self):
<<<<<<< HEAD
        return self.obj.name

    def progress_raw(self):
        try:
            return self.obj.uploaded_bytes / self.__size * 100
=======
        return self.__obj.name

    def progress_raw(self):
        try:
            return self.__obj.uploaded_bytes / self.__size * 100
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
        except ZeroDivisionError:
            return 0

    def progress(self):
        return f'{round(self.progress_raw(), 2)}%'

    def speed_raw(self):
        """
        :return: Upload speed in Bytes/Seconds
        """
<<<<<<< HEAD
        return self.obj.speed()
=======
        return self.__obj.speed()
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9

    def speed(self):
        return f'{get_readable_file_size(self.speed_raw())}/s'

    def eta(self):
        try:
<<<<<<< HEAD
            seconds = (self.__size - self.obj.uploaded_bytes) / self.speed_raw()
=======
            seconds = (self.__size - self.__obj.uploaded_bytes) / self.speed_raw()
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
            return f'{get_readable_time(seconds)}'
        except ZeroDivisionError:
            return '-'

    def gid(self) -> str:
        return self.__gid

    def download(self):
<<<<<<< HEAD
        return self.obj
=======
        return self.__obj
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
