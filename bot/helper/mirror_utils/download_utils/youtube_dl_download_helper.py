<<<<<<< HEAD
from .download_helper import DownloadHelper
import time
from youtube_dl import YoutubeDL, DownloadError
from bot import download_dict_lock, download_dict
from ..status_utils.youtube_dl_download_status import YoutubeDLDownloadStatus
import logging
import re
import threading
=======
import random
import string
import logging

from yt_dlp import YoutubeDL, DownloadError
from threading import RLock
from time import time
from re import search

from bot import download_dict_lock, download_dict
from bot.helper.telegram_helper.message_utils import sendStatusMessage
from ..status_utils.youtube_dl_download_status import YoutubeDLDownloadStatus
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9

LOGGER = logging.getLogger(__name__)


class MyLogger:
    def __init__(self, obj):
        self.obj = obj

    def debug(self, msg):
<<<<<<< HEAD
        LOGGER.debug(msg)
        # Hack to fix changing changing extension
        match = re.search(r'.ffmpeg..Merging formats into..(.*?).$', msg)
        if match and not self.obj.is_playlist:
            newname = match.group(1)
            newname = newname.split("/")
            newname = newname[-1]
=======
        # Hack to fix changing extension
        match = search(r'.Merger..Merging formats into..(.*?).$', msg) # To mkv
        if not match and not self.obj.is_playlist:
            match = search(r'.ExtractAudio..Destination..(.*?)$', msg) # To mp3
        if match and not self.obj.is_playlist:
            newname = match.group(1)
            newname = newname.split("/")[-1]
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
            self.obj.name = newname

    @staticmethod
    def warning(msg):
        LOGGER.warning(msg)

    @staticmethod
    def error(msg):
<<<<<<< HEAD
        LOGGER.error(msg)


class YoutubeDLHelper(DownloadHelper):
    def __init__(self, listener):
        super().__init__()
        self.name = ""
        self.__start_time = time.time()
        self.__listener = listener
        self.__gid = ""
        self.opts = {
            'progress_hooks': [self.__onDownloadProgress],
            'logger': MyLogger(self),
            'usenetrc': True
        }
        self.__download_speed = 0
        self.downloaded_bytes = 0
        self.size = 0
        self.is_playlist = False
        self.last_downloaded = 0
        self.is_cancelled = False
        self.vid_id = ''
        self.__resource_lock = threading.RLock()
=======
        if msg != "ERROR: Cancelling...":
            LOGGER.error(msg)


class YoutubeDLHelper:
    def __init__(self, listener):
        self.name = ""
        self.is_playlist = False
        self.size = 0
        self.progress = 0
        self.downloaded_bytes = 0
        self._last_downloaded = 0
        self.__download_speed = 0
        self.__start_time = time()
        self.__listener = listener
        self.__gid = ""
        self.__is_cancelled = False
        self.__downloading = False
        self.__resource_lock = RLock()
        self.opts = {'progress_hooks': [self.__onDownloadProgress],
                     'logger': MyLogger(self),
                     'usenetrc': True,
                     'embedsubtitles': True,
                     'prefer_ffmpeg': True,
                     'cookiefile': 'cookies.txt'}
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9

    @property
    def download_speed(self):
        with self.__resource_lock:
            return self.__download_speed

<<<<<<< HEAD
    @property
    def gid(self):
        with self.__resource_lock:
            return self.__gid

    def __onDownloadProgress(self, d):
        if self.is_cancelled:
            raise ValueError("Cancelling Download..")
        if d['status'] == "finished":
            if self.is_playlist:
                self.last_downloaded = 0
        elif d['status'] == "downloading":
            with self.__resource_lock:
                self.__download_speed = d['speed']
                try:
                    tbyte = d['total_bytes']
                except KeyError:
                    tbyte = d['total_bytes_estimate']
                if self.is_playlist:
                    progress = d['downloaded_bytes'] / tbyte
                    chunk_size = d['downloaded_bytes'] - self.last_downloaded
                    self.last_downloaded = tbyte * progress
                    self.downloaded_bytes += chunk_size
                else:
                    self.size = tbyte
=======
    def __onDownloadProgress(self, d):
        self.__downloading = True
        if self.__is_cancelled:
            raise ValueError("Cancelling...")
        if d['status'] == "finished":
            if self.is_playlist:
                self._last_downloaded = 0
        elif d['status'] == "downloading":
            with self.__resource_lock:
                self.__download_speed = d['speed']
                if self.is_playlist:
                    downloadedBytes = d['downloaded_bytes']
                    chunk_size = downloadedBytes - self._last_downloaded
                    self._last_downloaded = downloadedBytes
                    self.downloaded_bytes += chunk_size
                else:
                    try:
                        self.size = d['total_bytes']
                    except KeyError:
                        if d.get('total_bytes_estimate'):
                            self.size = d['total_bytes_estimate']
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
                    self.downloaded_bytes = d['downloaded_bytes']
                try:
                    self.progress = (self.downloaded_bytes / self.size) * 100
                except ZeroDivisionError:
                    pass

    def __onDownloadStart(self):
        with download_dict_lock:
<<<<<<< HEAD
            download_dict[self.__listener.uid] = YoutubeDLDownloadStatus(self, self.__listener)
=======
            download_dict[self.__listener.uid] = YoutubeDLDownloadStatus(self, self.__listener, self.__gid)
        sendStatusMessage(self.__listener.update, self.__listener.bot)
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9

    def __onDownloadComplete(self):
        self.__listener.onDownloadComplete()

<<<<<<< HEAD
    def onDownloadError(self, error):
        self.__listener.onDownloadError(error)

    def extractMetaData(self, link, qual, name):
        if "hotstar" in link or "sonyliv" in link:
            self.opts['geo_bypass_country'] = 'IN'

        with YoutubeDL(self.opts) as ydl:
            try:
                result = ydl.extract_info(link, download=False)
                name = ydl.prepare_filename(result) if name == "" else name
                # noobway hack for changing extension after converting to mp3
                if qual == "audio":
                  name = name.replace(".mp4", ".mp3").replace(".webm", ".mp3")
            except DownloadError as e:
                self.onDownloadError(str(e))
                return
        if result.get('direct'):
            return None
        if 'entries' in result:
            video = result['entries'][0]
            for v in result['entries']:
                if v and v.get('filesize'):
                    self.size += float(v['filesize'])
            # For playlists, ydl.prepare-filename returns the following format: <Playlist Name>-<Id of playlist>.NA
            self.name = name.split(f"-{result['id']}")[0]
            self.vid_id = video.get('id')
            self.is_playlist = True
        else:
            video = result
            if video.get('filesize'):
                self.size = float(video.get('filesize'))
            self.name = name
            self.vid_id = video.get('id')
        return video
=======
    def __onDownloadError(self, error):
        self.__listener.onDownloadError(error)

    def extractMetaData(self, link, name, get_info=False):

        if get_info:
            self.opts['playlist_items'] = '0'
        with YoutubeDL(self.opts) as ydl:
            try:
                result = ydl.extract_info(link, download=False)
                if get_info:
                    return result
                realName = ydl.prepare_filename(result)
            except Exception as e:
                if get_info:
                    raise e
                self.__onDownloadError(str(e))
                return

        if 'entries' in result:
            for v in result['entries']:
                try:
                    self.size += v['filesize_approx']
                except:
                    pass
            self.is_playlist = True
            if name == "":
                self.name = str(realName).split(f" [{result['id']}]")[0]
            else:
                self.name = name
        else:
            ext = realName.split('.')[-1]
            if name == "":
                self.name = str(realName).split(f" [{result['id']}]")[0] + '.' + ext
            else:
                self.name = f"{name}.{ext}"
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9

    def __download(self, link):
        try:
            with YoutubeDL(self.opts) as ydl:
                try:
                    ydl.download([link])
                except DownloadError as e:
<<<<<<< HEAD
                    self.onDownloadError(str(e))
                    return
            self.__onDownloadComplete()
        except ValueError:
            LOGGER.info("Download Cancelled by User!")
            self.onDownloadError("Download Cancelled by User!")

    def add_download(self, link, path, qual, name):
        pattern = '^.*(youtu\.be\/|youtube.com\/)(playlist?)'
        if re.match(pattern, link):
            self.opts['ignoreerrors'] = True
        self.__onDownloadStart()
        self.extractMetaData(link, qual, name)
        LOGGER.info(f"Downloading with YT-DL: {link}")
        self.__gid = f"{self.vid_id}{self.__listener.uid}"
        if qual == "audio":
          self.opts['format'] = 'bestaudio/best'
          self.opts['postprocessors'] = [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '320',}]
        else:
          self.opts['format'] = qual
=======
                    if not self.__is_cancelled:
                        self.__onDownloadError(str(e))
                    return
            if self.__is_cancelled:
                raise ValueError
            self.__onDownloadComplete()
        except ValueError:
            self.__onDownloadError("Download Stopped by User!")

    def add_download(self, link, path, name, qual, playlist):
        if playlist:
            self.opts['ignoreerrors'] = True
        if "hotstar" in link or "sonyliv" in link:
            self.opts['geo_bypass_country'] = 'IN'
        self.__gid = ''.join(random.SystemRandom().choices(string.ascii_letters + string.digits, k=10))
        self.__onDownloadStart()
        if qual.startswith('ba/b'):
            audio_info = qual.split('-')
            qual = audio_info[0]
            if len(audio_info) == 2:
                rate = audio_info[1]
            else:
                rate = 320
            self.opts['postprocessors'] = [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': f'{rate}'}]
        self.opts['format'] = qual
        LOGGER.info(f"Downloading with YT-DLP: {link}")
        self.extractMetaData(link, name)
        if self.__is_cancelled:
            return
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
        if not self.is_playlist:
            self.opts['outtmpl'] = f"{path}/{self.name}"
        else:
            self.opts['outtmpl'] = f"{path}/{self.name}/%(title)s.%(ext)s"
        self.__download(link)

    def cancel_download(self):
<<<<<<< HEAD
        self.is_cancelled = True
=======
        self.__is_cancelled = True
        LOGGER.info(f"Cancelling Download: {self.name}")
        if not self.__downloading:
            self.__onDownloadError("Download Cancelled by User!")

>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
