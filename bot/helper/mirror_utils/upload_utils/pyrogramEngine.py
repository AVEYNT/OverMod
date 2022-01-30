<<<<<<< HEAD
# Implement By - @anasty17 (https://github.com/SlamDevs/slam-mirrorbot/commit/d888a1e7237f4633c066f7c2bbfba030b83ad616)
# (c) https://github.com/SlamDevs/slam-mirrorbot
# All rights reserved

import os
import logging
import time

from pyrogram.errors import FloodWait
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata

from bot import app, DOWNLOAD_DIR, AS_DOCUMENT, AS_DOC_USERS, AS_MEDIA_USERS
from bot.helper.ext_utils.fs_utils import take_ss 

LOGGER = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

VIDEO_SUFFIXES = ("MKV", "MP4", "MOV", "WMV", "3GP", "MPG", "WEBM", "AVI", "FLV", "M4V")
AUDIO_SUFFIXES = ("MP3", "M4A", "M4B", "FLAC", "WAV", "AIF", "OGG", "AAC", "DTS", "MID", "AMR", "MKA")
IMAGE_SUFFIXES = ("JPG", "JPX", "PNG", "GIF", "WEBP", "CR2", "TIF", "BMP", "JXR", "PSD", "ICO", "HEIC")
=======
import logging

from os import remove as osremove, walk, path as ospath, rename as osrename
from time import time, sleep
from pyrogram.errors import FloodWait, RPCError
from PIL import Image
from threading import RLock

from bot import app, DOWNLOAD_DIR, AS_DOCUMENT, AS_DOC_USERS, AS_MEDIA_USERS, CUSTOM_FILENAME
from bot.helper.ext_utils.fs_utils import take_ss, get_media_info, get_video_resolution, get_path_size
from bot.helper.ext_utils.bot_utils import get_readable_file_size

LOGGER = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.ERROR)

VIDEO_SUFFIXES = ("MKV", "MP4", "MOV", "WMV", "3GP", "MPG", "WEBM", "AVI", "FLV", "M4V", "GIF")
AUDIO_SUFFIXES = ("MP3", "M4A", "M4B", "FLAC", "WAV", "AIF", "OGG", "AAC", "DTS", "MID", "AMR", "MKA")
IMAGE_SUFFIXES = ("JPG", "JPX", "PNG", "WEBP", "CR2", "TIF", "BMP", "JXR", "PSD", "ICO", "HEIC", "JPEG")
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9


class TgUploader:

    def __init__(self, name=None, listener=None):
<<<<<<< HEAD
        self.__listener = listener
        self.name = name
        self.__app = app
        self.total_bytes = 0
        self.uploaded_bytes = 0
        self.last_uploaded = 0
        self.start_time = time.time()
        self.is_cancelled = False
        self.chat_id = listener.message.chat.id
        self.message_id = listener.uid
        self.user_id = listener.message.from_user.id
        self.as_doc = AS_DOCUMENT
        self.thumb = f"Thumbnails/{self.user_id}.jpg"
        self.sent_msg = self.__app.get_messages(self.chat_id, self.message_id)

    def upload(self):
        msgs_dict = {}
        path = f"{DOWNLOAD_DIR}{self.message_id}"
        self.user_settings()
        for dirpath, subdir, files in sorted(os.walk(path)):
            for file in sorted(files):
                if self.is_cancelled:
                    return
                up_path = os.path.join(dirpath, file)
                self.upload_file(up_path, file, dirpath)
                if self.is_cancelled:
                    return
                msgs_dict[file] = self.sent_msg.message_id
                self.last_uploaded = 0
        LOGGER.info(f"Leech Done: {self.name}")
        self.__listener.onUploadComplete(self.name, None, msgs_dict, None, None)

    def upload_file(self, up_path, file, dirpath):
        cap_mono = f"<code>{file}</code>"
        notMedia = False
        thumb = self.thumb
        try:
            if not self.as_doc:
                duration = 0
                if file.upper().endswith(VIDEO_SUFFIXES):
                    metadata = extractMetadata(createParser(up_path))
                    if metadata.has("duration"):
                        duration = metadata.get("duration").seconds
                    if thumb is None:
                        thumb = take_ss(up_path)
                    if self.is_cancelled:
                        return
                    if not file.upper().endswith(("MKV", "MP4")):
                        file = os.path.splitext(file)[0] + '.mp4'
                        new_path = os.path.join(dirpath, file)
                        os.rename(up_path, new_path)
                        up_path = new_path
                    self.sent_msg = self.sent_msg.reply_video(video=up_path,
=======
        self.name = name
        self.uploaded_bytes = 0
        self._last_uploaded = 0
        self.__listener = listener
        self.__start_time = time()
        self.__is_cancelled = False
        self.__as_doc = AS_DOCUMENT
        self.__thumb = f"Thumbnails/{listener.message.from_user.id}.jpg"
        self.__sent_msg = ''
        self.__msgs_dict = {}
        self.__corrupted = 0
        self.__resource_lock = RLock()
        self.__user_settings()

    def upload(self):
        path = f"{DOWNLOAD_DIR}{self.__listener.uid}"
        size = get_readable_file_size(get_path_size(path))
        for dirpath, subdir, files in sorted(walk(path)):
            for file_ in sorted(files):
                if self.__is_cancelled:
                    return
                if file_.endswith('.torrent'):
                    continue
                up_path = ospath.join(dirpath, file_)
                fsize = ospath.getsize(up_path)
                if fsize == 0:
                    LOGGER.error(f"{up_path} size is zero, telegram don't upload zero size files")
                    self.__corrupted += 1
                    continue
                self.__upload_file(up_path, file_, dirpath)
                if self.__is_cancelled:
                    return
                self.__msgs_dict[file_] = self.__sent_msg.message_id
                self._last_uploaded = 0
                sleep(1)
        if len(self.__msgs_dict) <= self.__corrupted:
            return self.__listener.onUploadError('Files Corrupted. Check logs')
        LOGGER.info(f"Leech Completed: {self.name}")
        self.__listener.onUploadComplete(None, size, self.__msgs_dict, None, self.__corrupted, self.name)

    def __upload_file(self, up_path, file_, dirpath):
        if self.__sent_msg == '':
            self.__sent_msg = app.get_messages(self.__listener.message.chat.id, self.__listener.uid)
        else:
            self.__sent_msg = app.get_messages(self.__sent_msg.chat.id, self.__sent_msg.message_id)
        if CUSTOM_FILENAME is not None:
            cap_mono = f"{CUSTOM_FILENAME} <code>{file_}</code>"
            file_ = f"{CUSTOM_FILENAME} {file_}"
            new_path = ospath.join(dirpath, file_)
            osrename(up_path, new_path)
            up_path = new_path
        else:
            cap_mono = f"<code>{file_}</code>"
        notMedia = False
        thumb = self.__thumb
        try:
            if not self.__as_doc:
                duration = 0
                if file_.upper().endswith(VIDEO_SUFFIXES):
                    duration = get_media_info(up_path)[0]
                    if thumb is None:
                        thumb = take_ss(up_path)
                        if self.__is_cancelled:
                            if self.__thumb is None and thumb is not None and ospath.lexists(thumb):
                                osremove(thumb)
                            return
                    if thumb is not None:
                        img = Image.open(thumb)
                        width, height = img.size
                    else:
                        width, height = get_video_resolution(up_path)
                    if not file_.upper().endswith(("MKV", "MP4")):
                        file_ = ospath.splitext(file_)[0] + '.mp4'
                        new_path = ospath.join(dirpath, file_)
                        osrename(up_path, new_path)
                        up_path = new_path
                    self.__sent_msg = self.__sent_msg.reply_video(video=up_path,
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
                                                              quote=True,
                                                              caption=cap_mono,
                                                              parse_mode="html",
                                                              duration=duration,
<<<<<<< HEAD
                                                              width=480,
                                                              height=320,
                                                              thumb=thumb,
                                                              supports_streaming=True,
                                                              disable_notification=True,
                                                              progress=self.upload_progress)
                    if self.thumb is None and thumb is not None and os.path.lexists(thumb):
                        os.remove(thumb)
                elif file.upper().endswith(AUDIO_SUFFIXES):
                    metadata = extractMetadata(createParser(up_path))
                    if metadata.has("duration"):
                        duration = metadata.get('duration').seconds
                    title = metadata.get("title") if metadata.has("title") else None
                    artist = metadata.get("artist") if metadata.has("artist") else None
                    self.sent_msg = self.sent_msg.reply_audio(audio=up_path,
=======
                                                              width=width,
                                                              height=height,
                                                              thumb=thumb,
                                                              supports_streaming=True,
                                                              disable_notification=True,
                                                              progress=self.__upload_progress)
                elif file_.upper().endswith(AUDIO_SUFFIXES):
                    duration , artist, title = get_media_info(up_path)
                    self.__sent_msg = self.__sent_msg.reply_audio(audio=up_path,
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
                                                              quote=True,
                                                              caption=cap_mono,
                                                              parse_mode="html",
                                                              duration=duration,
                                                              performer=artist,
                                                              title=title,
                                                              thumb=thumb,
                                                              disable_notification=True,
<<<<<<< HEAD
                                                              progress=self.upload_progress)
                elif file.upper().endswith(IMAGE_SUFFIXES):
                    self.sent_msg = self.sent_msg.reply_photo(photo=up_path,
=======
                                                              progress=self.__upload_progress)
                elif file_.upper().endswith(IMAGE_SUFFIXES):
                    self.__sent_msg = self.__sent_msg.reply_photo(photo=up_path,
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
                                                              quote=True,
                                                              caption=cap_mono,
                                                              parse_mode="html",
                                                              disable_notification=True,
<<<<<<< HEAD
                                                              progress=self.upload_progress)
                else:
                    notMedia = True
            if self.as_doc or notMedia:
                if file.upper().endswith(VIDEO_SUFFIXES) and thumb is None:
                    thumb = take_ss(up_path)
                if self.is_cancelled:
                    return
                self.sent_msg = self.sent_msg.reply_document(document=up_path,
=======
                                                              progress=self.__upload_progress)
                else:
                    notMedia = True
            if self.__as_doc or notMedia:
                if file_.upper().endswith(VIDEO_SUFFIXES) and thumb is None:
                    thumb = take_ss(up_path)
                    if self.__is_cancelled:
                        if self.__thumb is None and thumb is not None and ospath.lexists(thumb):
                            osremove(thumb)
                        return
                self.__sent_msg = self.__sent_msg.reply_document(document=up_path,
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
                                                             quote=True,
                                                             thumb=thumb,
                                                             caption=cap_mono,
                                                             parse_mode="html",
                                                             disable_notification=True,
<<<<<<< HEAD
                                                             progress=self.upload_progress)
                if self.thumb is None and thumb is not None and os.path.lexists(thumb):
                    os.remove(thumb)
            if not self.is_cancelled:
                os.remove(up_path)
        except FloodWait as f:
            LOGGER.info(f)
            time.sleep(f.x)
    def upload_progress(self, current, total):
        if self.is_cancelled:
            self.__app.stop_transmission()
            return
        chunk_size = current - self.last_uploaded
        self.last_uploaded = current
        self.uploaded_bytes += chunk_size

    def user_settings(self):
        if self.user_id in AS_DOC_USERS:
            self.as_doc = True
        elif self.user_id in AS_MEDIA_USERS:
            self.as_doc = False
        if not os.path.lexists(self.thumb):
            self.thumb = None

    def speed(self):
        try:
            return self.uploaded_bytes / (time.time() - self.start_time)
        except ZeroDivisionError:
            return 0

    def cancel_download(self):
        self.is_cancelled = True
        LOGGER.info(f"Cancelling Upload: {self.name}")
        self.__listener.onUploadError('unggahan Anda telah dihentikan!')
=======
                                                             progress=self.__upload_progress)
        except FloodWait as f:
            LOGGER.warning(str(f))
            sleep(f.x)
        except RPCError as e:
            LOGGER.error(f"RPCError: {e} File: {up_path}")
            self.__corrupted += 1
        except Exception as err:
            LOGGER.error(f"{err} File: {up_path}")
            self.__corrupted += 1
        if self.__thumb is None and thumb is not None and ospath.lexists(thumb):
            osremove(thumb)
        if not self.__is_cancelled:
            osremove(up_path)

    def __upload_progress(self, current, total):
        if self.__is_cancelled:
            app.stop_transmission()
            return
        with self.__resource_lock:
            chunk_size = current - self._last_uploaded
            self._last_uploaded = current
            self.uploaded_bytes += chunk_size

    def __user_settings(self):
        if self.__listener.message.from_user.id in AS_DOC_USERS:
            self.__as_doc = True
        elif self.__listener.message.from_user.id in AS_MEDIA_USERS:
            self.__as_doc = False
        if not ospath.lexists(self.__thumb):
            self.__thumb = None

    @property
    def speed(self):
        with self.__resource_lock:
            try:
                return self.uploaded_bytes / (time() - self.__start_time)
            except ZeroDivisionError:
                return 0

    def cancel_download(self):
        self.__is_cancelled = True
        LOGGER.info(f"Cancelling Upload: {self.name}")
        self.__listener.onUploadError('your upload has been stopped!')
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
