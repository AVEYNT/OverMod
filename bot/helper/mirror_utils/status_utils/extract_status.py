<<<<<<< HEAD
from .status import Status
from bot.helper.ext_utils.bot_utils import get_readable_file_size, MirrorStatus


class ExtractStatus(Status):
=======
from bot.helper.ext_utils.bot_utils import get_readable_file_size, MirrorStatus


class ExtractStatus:
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
    def __init__(self, name, path, size):
        self.__name = name
        self.__path = path
        self.__size = size

    # The progress of extract function cannot be tracked. So we just return dummy values.
    # If this is possible in future,we should implement it

    def progress(self):
        return '0'

    def speed(self):
        return '0'

    def name(self):
        return self.__name

    def path(self):
        return self.__path

    def size(self):
        return get_readable_file_size(self.__size)

    def eta(self):
        return '0s'

    def status(self):
        return MirrorStatus.STATUS_EXTRACTING

    def processed_bytes(self):
        return 0
