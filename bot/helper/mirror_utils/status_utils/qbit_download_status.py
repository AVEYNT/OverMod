<<<<<<< HEAD
# Implement By - @anasty17 (https://github.com/breakdowns/slam-tg-mirror-bot/commit/0bfba523f095ab1dccad431d72561e0e002e7a59)
# (c) https://github.com/breakdowns/slam-aria-mirror-bot
# All rights reserved

from bot import DOWNLOAD_DIR, LOGGER, get_client
from bot.helper.ext_utils.bot_utils import MirrorStatus, get_readable_file_size, get_readable_time
from .status import Status
from time import sleep


class QbDownloadStatus(Status):

    def __init__(self, gid, listener, qbhash, client):
        super().__init__()
        self.__gid = gid
        self.__hash = qbhash
        self.client = client
        self.__uid = listener.uid
        self.listener = listener
        self.message = listener.message

=======
from bot import DOWNLOAD_DIR, LOGGER
from bot.helper.ext_utils.bot_utils import MirrorStatus, get_readable_file_size, get_readable_time
from time import sleep

def get_download(client, hash_):
    try:
        return client.torrents_info(torrent_hashes=hash_)[0]
    except:
        pass


class QbDownloadStatus:

    def __init__(self, listener, client, gid, hash_, select):
        self.__gid = gid
        self.__hash = hash_
        self.__select = select
        self.__client = client
        self.__listener = listener
        self.__uid = listener.uid
        self.__info = get_download(client, hash_)
        self.message = listener.message

    def __update(self):
        self.__info = get_download(self.__client, self.__hash)
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9

    def progress(self):
        """
        Calculates the progress of the mirror (upload or download)
        :return: returns progress in percentage
        """
<<<<<<< HEAD
        return f'{round(self.torrent_info().progress*100,2)}%'
=======
        return f'{round(self.__info.progress*100, 2)}%'
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9

    def size_raw(self):
        """
        Gets total size of the mirror file/folder
        :return: total size of mirror
        """
<<<<<<< HEAD
        return self.torrent_info().size

    def processed_bytes(self):
        return self.torrent_info().downloaded

    def speed(self):
        return f"{get_readable_file_size(self.torrent_info().dlspeed)}/s"

    def name(self):
        return self.torrent_info().name
=======
        if self.__select:
            return self.__info.size
        else:
            return self.__info.total_size

    def processed_bytes(self):
        return self.__info.downloaded

    def speed(self):
        return f"{get_readable_file_size(self.__info.dlspeed)}/s"

    def name(self):
        self.__update()
        return self.__info.name
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9

    def path(self):
        return f"{DOWNLOAD_DIR}{self.__uid}"

    def size(self):
<<<<<<< HEAD
        return get_readable_file_size(self.torrent_info().size)

    def eta(self):
        return get_readable_time(self.torrent_info().eta)

    def status(self):
        download = self.torrent_info().state
        if download == "queuedDL":
            return MirrorStatus.STATUS_WAITING
        elif download in ["metaDL", "checkingResumeData"]:
            return MirrorStatus.STATUS_DOWNLOADING + " (Metadata)"
        elif download == "pausedDL":
            return MirrorStatus.STATUS_PAUSE
=======
        return get_readable_file_size(self.__info.size)

    def eta(self):
        return get_readable_time(self.__info.eta)

    def status(self):
        download = self.__info.state
        if download in ["queuedDL", "queuedUP"]:
            return MirrorStatus.STATUS_WAITING
        elif download in ["metaDL", "checkingResumeData"]:
            return MirrorStatus.STATUS_DOWNLOADING + " (Metadata)"
        elif download in ["pausedDL", "pausedUP"]:
            return MirrorStatus.STATUS_PAUSE
        elif download in ["checkingUP", "checkingDL"]:
            return MirrorStatus.STATUS_CHECKING
        elif download in ["stalledUP", "uploading", "forcedUP"]:
            return MirrorStatus.STATUS_SEEDING
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
        else:
            return MirrorStatus.STATUS_DOWNLOADING

    def torrent_info(self):
<<<<<<< HEAD
        return self.client.torrents_info(torrent_hashes=self.__hash)[0]
=======
        return self.__info
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9

    def download(self):
        return self

    def uid(self):
        return self.__uid

    def gid(self):
        return self.__gid

<<<<<<< HEAD
    def cancel_download(self):
        LOGGER.info(f"Membatalkan Unduh: {self.name()}")
        self.client.torrents_pause(torrent_hashes=self.__hash)
        sleep(0.3)
        self.listener.onDownloadError('Unduh dihentikan oleh pengguna!')
        self.client.torrents_delete(torrent_hashes=self.__hash)
=======
    def client(self):
        return self.__client

    def listener(self):
        return self.__listener

    def cancel_download(self):
        self.__update()
        if self.status() == MirrorStatus.STATUS_SEEDING:
            LOGGER.info(f"Cancelling Seed: {self.name()}")
            self.__client.torrents_pause(torrent_hashes=self.__hash)
        else:
            LOGGER.info(f"Cancelling Download: {self.name()}")
            self.__client.torrents_pause(torrent_hashes=self.__hash)
            sleep(0.3)
            self.__listener.onDownloadError('Download stopped by user!')
            self.__client.torrents_delete(torrent_hashes=self.__hash, delete_files=True)
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
