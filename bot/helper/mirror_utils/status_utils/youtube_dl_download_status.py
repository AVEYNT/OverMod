from bot import DOWNLOAD_DIR
from bot.helper.ext_utils.bot_utils import MirrorStatus, get_readable_file_size, get_readable_time
<<<<<<< HEAD
from .status import Status
from bot.helper.ext_utils.fs_utils import get_path_size

class YoutubeDLDownloadStatus(Status):
    def __init__(self, obj, listener):
        self.obj = obj
        self.uid = listener.uid
        self.message = listener.message

    def gid(self):
        return self.obj.gid

    def path(self):
        return f"{DOWNLOAD_DIR}{self.uid}"

    def processed_bytes(self):
        if self.obj.downloaded_bytes != 0:
          return self.obj.downloaded_bytes
        else:
          return get_path_size(f"{DOWNLOAD_DIR}{self.uid}")

    def size_raw(self):
        return self.obj.size
=======
from bot.helper.ext_utils.fs_utils import get_path_size

class YoutubeDLDownloadStatus:
    def __init__(self, obj, listener, gid):
        self.__obj = obj
        self.__uid = listener.uid
        self.__gid = gid
        self.message = listener.message

    def gid(self):
        return self.__gid

    def path(self):
        return f"{DOWNLOAD_DIR}{self.__uid}"

    def processed_bytes(self):
        if self.__obj.downloaded_bytes != 0:
          return self.__obj.downloaded_bytes
        else:
          return get_path_size(f"{DOWNLOAD_DIR}{self.__uid}")

    def size_raw(self):
        return self.__obj.size
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9

    def size(self):
        return get_readable_file_size(self.size_raw())

    def status(self):
        return MirrorStatus.STATUS_DOWNLOADING

    def name(self):
<<<<<<< HEAD
        return self.obj.name

    def progress_raw(self):
        return self.obj.progress
=======
        return self.__obj.name

    def progress_raw(self):
        return self.__obj.progress
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9

    def progress(self):
        return f'{round(self.progress_raw(), 2)}%'

    def speed_raw(self):
        """
        :return: Download speed in Bytes/Seconds
        """
<<<<<<< HEAD
        return self.obj.download_speed
=======
        return self.__obj.download_speed
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9

    def speed(self):
        return f'{get_readable_file_size(self.speed_raw())}/s'

    def eta(self):
        try:
            seconds = (self.size_raw() - self.processed_bytes()) / self.speed_raw()
            return f'{get_readable_time(seconds)}'
        except:
            return '-'

    def download(self):
<<<<<<< HEAD
        return self.obj
=======
        return self.__obj
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
