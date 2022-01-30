<<<<<<< HEAD
from .status import Status
from bot.helper.ext_utils.bot_utils import MirrorStatus, get_readable_file_size, get_readable_time


class CloneStatus(Status):
    def __init__(self, obj, size, update, gid):
        self.cobj = obj
        self.__csize = size
        self.message = update.message
        self.__cgid = gid

    def processed_bytes(self):
        return self.cobj.transferred_size

    def size_raw(self):
        return self.__csize

    def size(self):
        return get_readable_file_size(self.__csize)
=======
from bot.helper.ext_utils.bot_utils import MirrorStatus, get_readable_file_size, get_readable_time


class CloneStatus:
    def __init__(self, obj, size, update, gid):
        self.__obj = obj
        self.__size = size
        self.message = update.message
        self.__gid = gid

    def processed_bytes(self):
        return self.__obj.transferred_size

    def size_raw(self):
        return self.__size

    def size(self):
        return get_readable_file_size(self.__size)
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9

    def status(self):
        return MirrorStatus.STATUS_CLONING

    def name(self):
<<<<<<< HEAD
        return self.cobj.name

    def gid(self) -> str:
        return self.__cgid

    def progress_raw(self):
        try:
            return self.cobj.transferred_size / self.__csize * 100
=======
        return self.__obj.name

    def gid(self) -> str:
        return self.__gid

    def progress_raw(self):
        try:
            return self.__obj.transferred_size / self.__size * 100
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
        except ZeroDivisionError:
            return 0

    def progress(self):
        return f'{round(self.progress_raw(), 2)}%'

    def speed_raw(self):
        """
        :return: Download speed in Bytes/Seconds
        """
<<<<<<< HEAD
        return self.cobj.cspeed()
=======
        return self.__obj.cspeed()
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9

    def speed(self):
        return f'{get_readable_file_size(self.speed_raw())}/s'

    def eta(self):
        try:
<<<<<<< HEAD
            seconds = (self.__csize - self.cobj.transferred_size) / self.speed_raw()
=======
            seconds = (self.__size - self.__obj.transferred_size) / self.speed_raw()
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
            return f'{get_readable_time(seconds)}'
        except ZeroDivisionError:
            return '-'

    def download(self):
<<<<<<< HEAD
        return self.cobj
=======
        return self.__obj
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
