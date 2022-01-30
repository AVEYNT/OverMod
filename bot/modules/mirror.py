import requests
<<<<<<< HEAD
import urllib
import pathlib
import os
import subprocess
import threading
import re
import random
import string
import time
import shutil

from telegram.ext import CommandHandler
from telegram import InlineKeyboardMarkup
from fnmatch import fnmatch

from bot import Interval, INDEX_URL, BUTTON_FOUR_NAME, BUTTON_FOUR_URL, BUTTON_FIVE_NAME, BUTTON_FIVE_URL, \
                BUTTON_SIX_NAME, BUTTON_SIX_URL, BLOCK_MEGA_FOLDER, BLOCK_MEGA_LINKS, VIEW_LINK, aria2, \
                dispatcher, DOWNLOAD_DIR, download_dict, download_dict_lock, SHORTENER, SHORTENER_API, \
                TAR_UNZIP_LIMIT, TG_SPLIT_SIZE
from bot.helper.ext_utils import fs_utils, bot_utils
from bot.helper.ext_utils.shortenurl import short_url
from bot.helper.ext_utils.exceptions import DirectDownloadLinkException, NotSupportedExtractionArchive
from bot.helper.mirror_utils.download_utils.aria2_download import AriaDownloadHelper
from bot.helper.mirror_utils.download_utils.mega_downloader import MegaDownloadHelper
from bot.helper.mirror_utils.download_utils.qbit_downloader import QbitTorrent
from bot.helper.mirror_utils.download_utils.direct_link_generator import direct_link_generator
from bot.helper.mirror_utils.download_utils.telegram_downloader import TelegramDownloadHelper
from bot.helper.mirror_utils.status_utils import listeners
from bot.helper.mirror_utils.status_utils.extract_status import ExtractStatus
from bot.helper.mirror_utils.status_utils.tar_status import TarStatus
from bot.helper.mirror_utils.status_utils.split_status import SplitStatus
from bot.helper.mirror_utils.status_utils.upload_status import UploadStatus
from bot.helper.mirror_utils.status_utils.tg_upload_status import TgUploadStatus
from bot.helper.mirror_utils.status_utils.gdownload_status import DownloadStatus
from bot.helper.mirror_utils.upload_utils import gdriveTools, pyrogramEngine
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.message_utils import *
from bot.helper.telegram_helper import button_build

ariaDlManager = AriaDownloadHelper()
ariaDlManager.start_listener()


class MirrorListener(listeners.MirrorListeners):
    def __init__(self, bot, update, pswd, isTar=False, extract=False, isZip=False, isQbit=False, isLeech=False):
        super().__init__(bot, update)
        self.isTar = isTar
=======

from re import match, search, split as resplit
from time import sleep, time
from os import path as ospath, remove as osremove, listdir, walk
from shutil import rmtree
from threading import Thread
from subprocess import run as srun
from pathlib import PurePath
from urllib.parse import quote
from telegram.ext import CommandHandler
from telegram import InlineKeyboardMarkup

from bot import Interval, INDEX_URL, BUTTON_FOUR_NAME, BUTTON_FOUR_URL, BUTTON_FIVE_NAME, BUTTON_FIVE_URL, \
                BUTTON_SIX_NAME, BUTTON_SIX_URL, BLOCK_MEGA_FOLDER, BLOCK_MEGA_LINKS, VIEW_LINK, aria2, QB_SEED, \
                dispatcher, DOWNLOAD_DIR, download_dict, download_dict_lock, TG_SPLIT_SIZE, LOGGER
from bot.helper.ext_utils.bot_utils import is_url, is_magnet, is_gdtot_link, is_mega_link, is_gdrive_link, get_content_type, get_mega_link_type
from bot.helper.ext_utils.fs_utils import get_base_name, get_path_size, split as fssplit, clean_download
from bot.helper.ext_utils.shortenurl import short_url
from bot.helper.ext_utils.exceptions import DirectDownloadLinkException, NotSupportedExtractionArchive
from bot.helper.mirror_utils.download_utils.aria2_download import add_aria2c_download
from bot.helper.mirror_utils.download_utils.mega_downloader import add_mega_download
from bot.helper.mirror_utils.download_utils.gd_downloader import add_gd_download
from bot.helper.mirror_utils.download_utils.qbit_downloader import add_qb_torrent
from bot.helper.mirror_utils.download_utils.direct_link_generator import direct_link_generator
from bot.helper.mirror_utils.download_utils.telegram_downloader import TelegramDownloadHelper
from bot.helper.mirror_utils.status_utils.extract_status import ExtractStatus
from bot.helper.mirror_utils.status_utils.zip_status import ZipStatus
from bot.helper.mirror_utils.status_utils.split_status import SplitStatus
from bot.helper.mirror_utils.status_utils.upload_status import UploadStatus
from bot.helper.mirror_utils.status_utils.tg_upload_status import TgUploadStatus
from bot.helper.mirror_utils.upload_utils.gdriveTools import GoogleDriveHelper
from bot.helper.mirror_utils.upload_utils.pyrogramEngine import TgUploader
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.message_utils import sendMessage, sendMarkup, delete_all_messages, update_all_messages
from bot.helper.telegram_helper.button_build import ButtonMaker


class MirrorListener:
    def __init__(self, bot, update, isZip=False, extract=False, isQbit=False, isLeech=False, pswd=None, tag=None):
        self.bot = bot
        self.update = update
        self.message = update.message
        self.uid = self.message.message_id
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
        self.extract = extract
        self.isZip = isZip
        self.isQbit = isQbit
        self.isLeech = isLeech
        self.pswd = pswd
<<<<<<< HEAD

    def onDownloadStarted(self):
        pass

    def onDownloadProgress(self):
        # We are handling this on our own!
        pass
=======
        self.tag = tag
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9

    def clean(self):
        try:
            aria2.purge()
            Interval[0].cancel()
            del Interval[0]
            delete_all_messages()
        except IndexError:
            pass

    def onDownloadComplete(self):
        with download_dict_lock:
            LOGGER.info(f"Download completed: {download_dict[self.uid].name()}")
            download = download_dict[self.uid]
<<<<<<< HEAD
            name = f"{download.name()}".replace('/', '')
            gid = download.gid()
            size = download.size_raw()
            if name == "None" or self.isQbit: # when pyrogram's media.file_name is of NoneType
                name = os.listdir(f'{DOWNLOAD_DIR}{self.uid}')[0]
            m_path = f'{DOWNLOAD_DIR}{self.uid}/{name}'
        if self.isTar:
            try:
                with download_dict_lock:
                    download_dict[self.uid] = TarStatus(name, m_path, size)
                if self.isZip:
                    pswd = self.pswd
                    path = m_path + ".zip"
                    LOGGER.info(f'Zip: orig_path: {m_path}, zip_path: {path}')
                    if pswd is not None:
                        subprocess.run(["7z", "a", f"-p{pswd}", path, m_path])
                    else:
                        subprocess.run(["7z", "a", path, m_path])
                else:
                    path = fs_utils.tar(m_path)
=======
            name = str(download.name()).replace('/', '')
            gid = download.gid()
            size = download.size_raw()
            if name == "None" or self.isQbit:
                name = listdir(f'{DOWNLOAD_DIR}{self.uid}')[-1]
            m_path = f'{DOWNLOAD_DIR}{self.uid}/{name}'
        if self.isZip:
            try:
                with download_dict_lock:
                    download_dict[self.uid] = ZipStatus(name, m_path, size)
                pswd = self.pswd
                path = m_path + ".zip"
                LOGGER.info(f'Zip: orig_path: {m_path}, zip_path: {path}')
                if pswd is not None:
                    if self.isLeech and int(size) > TG_SPLIT_SIZE:
                        path = m_path + ".zip"
                        srun(["7z", f"-v{TG_SPLIT_SIZE}b", "a", "-mx=0", f"-p{pswd}", path, m_path])
                    else:
                        srun(["7z", "a", "-mx=0", f"-p{pswd}", path, m_path])
                elif self.isLeech and int(size) > TG_SPLIT_SIZE:
                    path = m_path + ".zip"
                    srun(["7z", f"-v{TG_SPLIT_SIZE}b", "a", "-mx=0", path, m_path])
                else:
                    srun(["7z", "a", "-mx=0", path, m_path])
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
            except FileNotFoundError:
                LOGGER.info('File to archive not found!')
                self.onUploadError('Internal error occurred!!')
                return
<<<<<<< HEAD
            try:
                shutil.rmtree(m_path)
            except:
                os.remove(m_path)
        elif self.extract:
            try:
=======
            if not self.isQbit or not QB_SEED or self.isLeech:
                try:
                    rmtree(m_path)
                except:
                    osremove(m_path)
        elif self.extract:
            try:
                if ospath.isfile(m_path):
                    path = get_base_name(m_path)
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
                LOGGER.info(f"Extracting: {name}")
                with download_dict_lock:
                    download_dict[self.uid] = ExtractStatus(name, m_path, size)
                pswd = self.pswd
<<<<<<< HEAD
                if os.path.isdir(m_path):
                    for dirpath, subdir, files in os.walk(m_path, topdown=False):
                        for file in files:
                            suffixes = (".part1.rar", ".part01.rar", ".part001.rar", ".part0001.rar")
                            if (file.endswith(".rar") and "part" not in file) or file.endswith(suffixes):
                                m_path = os.path.join(dirpath, file)
                                if pswd is not None:
                                    result = subprocess.run(["7z", "x", f"-p{pswd}", m_path, f"-o{dirpath}"])
                                else:
                                    result = subprocess.run(["7z", "x", m_path, f"-o{dirpath}"])
                                if result.returncode != 0:
                                    LOGGER.warning('Unable to extract archive!')
                                break
                        for file in files:
                            if file.endswith(".rar") or fnmatch(file, "*.r[0-9]") or fnmatch(file, "*.r[0-9]*"):
                                del_path = os.path.join(dirpath, file)
                                os.remove(del_path)
                    path = f'{DOWNLOAD_DIR}{self.uid}/{name}'
                else:
                    path = fs_utils.get_base_name(m_path)
                    if pswd is not None:
                        result = subprocess.run(["pextract", m_path, pswd])
                    else:
                        result = subprocess.run(["extract", m_path])
                    if result.returncode == 0:
                        os.remove(m_path)
                        LOGGER.info(f"Deleting archive: {m_path}")
                    else:
                        LOGGER.warning('Unable to extract archive! Uploading anyway')
                        path = f'{DOWNLOAD_DIR}{self.uid}/{name}'
                LOGGER.info(f'got path: {path}')

=======
                if ospath.isdir(m_path):
                    for dirpath, subdir, files in walk(m_path, topdown=False):
                        for file_ in files:
                            if search(r'\.part0*1.rar$', file_) or search(r'\.7z.0*1$', file_) \
                               or (file_.endswith(".rar") and not search(r'\.part\d+.rar$', file_)) \
                               or file_.endswith(".zip") or search(r'\.zip.0*1$', file_):
                                m_path = ospath.join(dirpath, file_)
                                if pswd is not None:
                                    result = srun(["7z", "x", f"-p{pswd}", m_path, f"-o{dirpath}", "-aot"])
                                else:
                                    result = srun(["7z", "x", m_path, f"-o{dirpath}", "-aot"])
                                if result.returncode != 0:
                                    LOGGER.error('Unable to extract archive!')
                        for file_ in files:
                            if file_.endswith(".rar") or search(r'\.r\d+$', file_) \
                               or search(r'\.7z.\d+$', file_) or search(r'\.z\d+$', file_) \
                               or search(r'\.zip.\d+$', file_) or file_.endswith(".zip"):
                                del_path = ospath.join(dirpath, file_)
                                osremove(del_path)
                    path = f'{DOWNLOAD_DIR}{self.uid}/{name}'
                else:
                    if pswd is not None:
                        result = srun(["bash", "pextract", m_path, pswd])
                    else:
                        result = srun(["bash", "extract", m_path])
                    if result.returncode == 0:
                        LOGGER.info(f"Extract Path: {path}")
                        osremove(m_path)
                        LOGGER.info(f"Deleting archive: {m_path}")
                    else:
                        LOGGER.error('Unable to extract archive! Uploading anyway')
                        path = f'{DOWNLOAD_DIR}{self.uid}/{name}'
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
            except NotSupportedExtractionArchive:
                LOGGER.info("Not any valid archive, uploading file as it is.")
                path = f'{DOWNLOAD_DIR}{self.uid}/{name}'
        else:
            path = f'{DOWNLOAD_DIR}{self.uid}/{name}'
<<<<<<< HEAD
        up_name = pathlib.PurePath(path).name
        up_path = f'{DOWNLOAD_DIR}{self.uid}/{up_name}'
        size = fs_utils.get_path_size(up_path)
        if self.isLeech:
            checked = False
            for dirpath, subdir, files in os.walk(f'{DOWNLOAD_DIR}{self.uid}', topdown=False):
                for file in files:
                    f_path = os.path.join(dirpath, file)
                    f_size = os.path.getsize(f_path)
=======
        up_name = PurePath(path).name
        up_path = f'{DOWNLOAD_DIR}{self.uid}/{up_name}'
        if self.isLeech and not self.isZip:
            checked = False
            for dirpath, subdir, files in walk(f'{DOWNLOAD_DIR}{self.uid}', topdown=False):
                for file_ in files:
                    f_path = ospath.join(dirpath, file_)
                    f_size = ospath.getsize(f_path)
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
                    if int(f_size) > TG_SPLIT_SIZE:
                        if not checked:
                            checked = True
                            with download_dict_lock:
                                download_dict[self.uid] = SplitStatus(up_name, up_path, size)
                            LOGGER.info(f"Splitting: {up_name}")
<<<<<<< HEAD
                        fs_utils.split(f_path, f_size, file, dirpath, TG_SPLIT_SIZE)
                        os.remove(f_path)
            LOGGER.info(f"Leech Name: {up_name}")
            tg = pyrogramEngine.TgUploader(up_name, self)
=======
                        fssplit(f_path, f_size, file_, dirpath, TG_SPLIT_SIZE)
                        osremove(f_path)
        if self.isLeech:
            size = get_path_size(f'{DOWNLOAD_DIR}{self.uid}')
            LOGGER.info(f"Leech Name: {up_name}")
            tg = TgUploader(up_name, self)
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
            tg_upload_status = TgUploadStatus(tg, size, gid, self)
            with download_dict_lock:
                download_dict[self.uid] = tg_upload_status
            update_all_messages()
            tg.upload()
        else:
<<<<<<< HEAD
            LOGGER.info(f"Upload Name: {up_name}")
            drive = gdriveTools.GoogleDriveHelper(up_name, self)
=======
            size = get_path_size(up_path)
            LOGGER.info(f"Upload Name: {up_name}")
            drive = GoogleDriveHelper(up_name, self)
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
            upload_status = UploadStatus(drive, size, gid, self)
            with download_dict_lock:
                download_dict[self.uid] = upload_status
            update_all_messages()
            drive.upload(up_name)

    def onDownloadError(self, error):
<<<<<<< HEAD
        error = error.replace('<', ' ')
        error = error.replace('>', ' ')
=======
        error = error.replace('<', ' ').replace('>', ' ')
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
        with download_dict_lock:
            try:
                download = download_dict[self.uid]
                del download_dict[self.uid]
<<<<<<< HEAD
                fs_utils.clean_download(download.path())
            except Exception as e:
                LOGGER.error(str(e))
            count = len(download_dict)
        if self.message.from_user.username:
            uname = f"@{self.message.from_user.username}"
        else:
            uname = f'<a href="tg://user?id={self.message.from_user.id}">{self.message.from_user.first_name}</a>'
        msg = f"{uname} unduhan Anda telah dihentikan karena: {error}"
=======
                clean_download(download.path())
            except Exception as e:
                LOGGER.error(str(e))
            count = len(download_dict)
        msg = f"{self.tag} your download has been stopped due to: {error}"
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
        sendMessage(msg, self.bot, self.update)
        if count == 0:
            self.clean()
        else:
            update_all_messages()

<<<<<<< HEAD
    def onUploadStarted(self):
        pass

    def onUploadProgress(self):
        pass

    def onUploadComplete(self, link: str, size, files, folders, typ):
        if self.isLeech:
            if self.message.from_user.username:
                uname = f"@{self.message.from_user.username}"
            else:
                uname = f'<a href="tg://user?id={self.message.from_user.id}">{self.message.from_user.first_name}</a>'
            count = len(files)
            if self.message.chat.type == 'private':
                msg = f'<b>Nama:</b> <code>{link}</code>\n'
                msg += f'<b>Jumlah File:</b> {count}'
                sendMessage(msg, self.bot, self.update)
            else:
                chat_id = str(self.message.chat.id)[4:]
                msg = f"<b>Nama:</b> <a href='https://t.me/c/{chat_id}/{self.uid}'>{link}</a>\n"
                msg += f'<b>Jumlah File:</b> {count}\n'
                msg += f'Pengguna: {uname}\n\n'
=======
    def onUploadComplete(self, link: str, size, files, folders, typ, name: str):
        if self.isLeech:
            count = len(files)
            msg = f'<b>Name: </b><code>{name}</code>\n\n'
            msg += f'<b>Size: </b>{size}\n'
            msg += f'<b>Total Files: </b>{count}'
            if typ != 0:
                msg += f'\n<b>Corrupted Files: </b>{typ}'
            if self.message.chat.type == 'private':
                sendMessage(msg, self.bot, self.update)
            else:
                chat_id = str(self.message.chat.id)[4:]
                msg += f'\n<b>cc: </b>{self.tag}\n\n'
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
                fmsg = ''
                for index, item in enumerate(list(files), start=1):
                    msg_id = files[item]
                    link = f"https://t.me/c/{chat_id}/{msg_id}"
                    fmsg += f"{index}. <a href='{link}'>{item}</a>\n"
<<<<<<< HEAD
                    if len(fmsg) > 3900:
                        sendMessage(msg + fmsg, self.bot, self.update)
                        fmsg = ''
                if fmsg != '':
                    sendMessage(msg + fmsg, self.bot, self.update)
            with download_dict_lock:
                try:
                    fs_utils.clean_download(download_dict[self.uid].path())
                except FileNotFoundError:
                    pass
                del download_dict[self.uid]
                count = len(download_dict)
            if count == 0:
                self.clean()
            else:
                update_all_messages()
            return
        with download_dict_lock:
            msg = f'<b>🗂Nama: </b><code>{download_dict[self.uid].name()}</code>\n<b>💾Ukuran: </b><code>{size}</code>'
            if os.path.isdir(f'{DOWNLOAD_DIR}/{self.uid}/{download_dict[self.uid].name()}'):
                msg += '\n<b>🔬Tipe: </b><code>Folder</code>'
                msg += f'\n<b>🗃SubFolder: </b><code>{folders}</code>'
                msg += f'\n<b>📄File: </b><code>{files}</code>'
            else:
                msg += f'\n<b>🔬Tipe: </b><code>{typ}</code>'
            buttons = button_build.ButtonMaker()
            if SHORTENER is not None and SHORTENER_API is not None:
                surl = short_url(link)
                buttons.buildbutton("🔹 Tautan Drive", surl)
            else:
                buttons.buildbutton("🔹 Tautan Drive", link)
            LOGGER.info(f'Done Uploading {download_dict[self.uid].name()}')
            if INDEX_URL is not None:
                url_path = requests.utils.quote(f'{download_dict[self.uid].name()}')
                share_url = f'{INDEX_URL}/{url_path}'
                if os.path.isdir(f'{DOWNLOAD_DIR}/{self.uid}/{download_dict[self.uid].name()}'):
                    share_url += '/'
                    if SHORTENER is not None and SHORTENER_API is not None:
                        siurl = short_url(share_url)
                        buttons.buildbutton("🔸 Tautan Indeks", siurl)
                    else:
                        buttons.buildbutton("🔸 Tautan Indeks", share_url)
                else:
                    share_urls = f'{INDEX_URL}/{url_path}?a=view'
                    if SHORTENER is not None and SHORTENER_API is not None:
                        siurl = short_url(share_url)
                        buttons.buildbutton("🔸 Tautan Indeks", siurl)
                        if VIEW_LINK:
                            siurls = short_url(share_urls)
                            buttons.buildbutton("♦️ Lihat Tautan", siurls)
                    else:
                        buttons.buildbutton("🔸 Tautan Indeks", share_url)
                        if VIEW_LINK:
                            buttons.buildbutton("♦️ Lihat Tautan", share_urls)
=======
                    if len(fmsg.encode('utf-8') + msg.encode('utf-8')) > 4000:
                        sendMessage(msg + fmsg, self.bot, self.update)
                        sleep(1.5)
                        fmsg = ''
                if fmsg != '':
                    sendMessage(msg + fmsg, self.bot, self.update)
            try:
                clean_download(f'{DOWNLOAD_DIR}{self.uid}')
            except FileNotFoundError:
                pass
            with download_dict_lock:
                del download_dict[self.uid]
                dcount = len(download_dict)
            if dcount == 0:
                self.clean()
            else:
                update_all_messages()
        else:
            msg = f'<b>Name: </b><code>{name}</code>\n\n<b>Size: </b>{size}'
            msg += f'\n\n<b>Type: </b>{typ}'
            if ospath.isdir(f'{DOWNLOAD_DIR}{self.uid}/{name}'):
                msg += f'\n<b>SubFolders: </b>{folders}'
                msg += f'\n<b>Files: </b>{files}'
            msg += f'\n\n<b>cc: </b>{self.tag}'
            buttons = ButtonMaker()
            link = short_url(link)
            buttons.buildbutton("☁️ Drive Link", link)
            LOGGER.info(f'Done Uploading {name}')
            if INDEX_URL is not None:
                url_path = requests.utils.quote(f'{name}')
                share_url = f'{INDEX_URL}/{url_path}'
                if ospath.isdir(f'{DOWNLOAD_DIR}/{self.uid}/{name}'):
                    share_url += '/'
                    share_url = short_url(share_url)
                    buttons.buildbutton("⚡ Index Link", share_url)
                else:
                    share_url = short_url(share_url)
                    buttons.buildbutton("⚡ Index Link", share_url)
                    if VIEW_LINK:
                        share_urls = f'{INDEX_URL}/{url_path}?a=view'
                        share_urls = short_url(share_urls)
                        buttons.buildbutton("🌐 View Link", share_urls)
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
            if BUTTON_FOUR_NAME is not None and BUTTON_FOUR_URL is not None:
                buttons.buildbutton(f"{BUTTON_FOUR_NAME}", f"{BUTTON_FOUR_URL}")
            if BUTTON_FIVE_NAME is not None and BUTTON_FIVE_URL is not None:
                buttons.buildbutton(f"{BUTTON_FIVE_NAME}", f"{BUTTON_FIVE_URL}")
            if BUTTON_SIX_NAME is not None and BUTTON_SIX_URL is not None:
                buttons.buildbutton(f"{BUTTON_SIX_NAME}", f"{BUTTON_SIX_URL}")
<<<<<<< HEAD
            if self.message.from_user.username:
                uname = f"@{self.message.from_user.username}"
            else:
                uname = f'<a href="tg://user?id={self.message.from_user.id}">{self.message.from_user.first_name}</a>'
            if uname is not None:
                msg += f'\n\n👤Penggunna: {uname}'
                msg += f'\n🗂File anda masuk database kami \n🚫Jangan sebar tautan indeks'
            try:
                fs_utils.clean_download(download_dict[self.uid].path())
            except FileNotFoundError:
                pass
            del download_dict[self.uid]
            count = len(download_dict)
        sendMarkup(msg, self.bot, self.update, InlineKeyboardMarkup(buttons.build_menu(2)))
        if count == 0:
            self.clean()
        else:
            update_all_messages()
=======
            if self.isQbit and QB_SEED and not self.extract:
                if self.isZip:
                    try:
                        osremove(f'{DOWNLOAD_DIR}{self.uid}/{name}')
                    except:
                        pass
                return sendMarkup(msg, self.bot, self.update, InlineKeyboardMarkup(buttons.build_menu(2)))
            else:
                try:
                    clean_download(f'{DOWNLOAD_DIR}{self.uid}')
                except FileNotFoundError:
                    pass
                with download_dict_lock:
                    del download_dict[self.uid]
                    count = len(download_dict)
                sendMarkup(msg, self.bot, self.update, InlineKeyboardMarkup(buttons.build_menu(2)))
                if count == 0:
                    self.clean()
                else:
                    update_all_messages()
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9

    def onUploadError(self, error):
        e_str = error.replace('<', '').replace('>', '')
        with download_dict_lock:
            try:
<<<<<<< HEAD
                fs_utils.clean_download(download_dict[self.uid].path())
=======
                clean_download(download_dict[self.uid].path())
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
            except FileNotFoundError:
                pass
            del download_dict[self.message.message_id]
            count = len(download_dict)
<<<<<<< HEAD
        if self.message.from_user.username:
            uname = f"@{self.message.from_user.username}"
        else:
            uname = f'<a href="tg://user?id={self.message.from_user.id}">{self.message.from_user.first_name}</a>'
        if uname is not None:
            men = f'{uname} '
        sendMessage(men + e_str, self.bot, self.update)
=======
        sendMessage(f"{self.tag} {e_str}", self.bot, self.update)
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
        if count == 0:
            self.clean()
        else:
            update_all_messages()

<<<<<<< HEAD
def _mirror(bot, update, isTar=False, extract=False, isZip=False, isQbit=False, isLeech=False):
    mesg = update.message.text.split('\n')
    message_args = mesg[0].split(' ')
    name_args = mesg[0].split('|')
    qbitsel = False
    try:
        link = message_args[1]
        if link == "s":
            qbitsel = True
            link = message_args[2]
=======
def _mirror(bot, update, isZip=False, extract=False, isQbit=False, isLeech=False, pswd=None):
    mesg = update.message.text.split('\n')
    message_args = mesg[0].split(' ', maxsplit=1)
    name_args = mesg[0].split('|', maxsplit=1)
    qbitsel = False
    try:
        link = message_args[1]
        if link.startswith("s ") or link == "s":
            qbitsel = True
            message_args = mesg[0].split(' ', maxsplit=2)
            link = message_args[2].strip()
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
        if link.startswith("|") or link.startswith("pswd: "):
            link = ''
    except IndexError:
        link = ''
    try:
        name = name_args[1]
<<<<<<< HEAD
        name = name.strip()
        if name.startswith("pswd: "):
            name = ''
    except IndexError:
        name = ''
    try:
        ussr = urllib.parse.quote(mesg[1], safe='')
        pssw = urllib.parse.quote(mesg[2], safe='')
    except:
        ussr = ''
        pssw = ''
    if ussr != '' and pssw != '':
        link = link.split("://", maxsplit=1)
        link = f'{link[0]}://{ussr}:{pssw}@{link[1]}'
    pswd = re.search('(?<=pswd: )(.*)', update.message.text)
    if pswd is not None:
      pswd = pswd.groups()
      pswd = " ".join(pswd)
    if link != '':
        LOGGER.info(link)
    link = link.strip()
=======
        name = name.split(' pswd: ')[0]
        name = name.strip()
    except IndexError:
        name = ''
    link = resplit(r"pswd:| \|", link)[0]
    link = link.strip()
    pswdMsg = mesg[0].split(' pswd: ')
    if len(pswdMsg) > 1:
        pswd = pswdMsg[1]

    if update.message.from_user.username:
        tag = f"@{update.message.from_user.username}"
    else:
        tag = update.message.from_user.mention_html(update.message.from_user.first_name)

>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
    reply_to = update.message.reply_to_message
    if reply_to is not None:
        file = None
        media_array = [reply_to.document, reply_to.video, reply_to.audio]
        for i in media_array:
            if i is not None:
                file = i
                break
<<<<<<< HEAD
        if (
            not bot_utils.is_url(link)
            and not bot_utils.is_magnet(link)
            or len(link) == 0
        ):
            if file is None:
                reply_text = reply_to.text
                reply_text = re.split('\n ', reply_text)[0]
                if bot_utils.is_url(reply_text) or bot_utils.is_magnet(reply_text):
                    link = reply_text

            elif isQbit:
                file_name = str(time.time()).replace(".", "") + ".torrent"
                file.get_file().download(custom_path=f"{file_name}")
                link = f"{file_name}"
            elif file.mime_type != "application/x-bittorrent":
                listener = MirrorListener(bot, update, pswd, isTar, extract, isZip, isLeech=isLeech)
=======

        if not reply_to.from_user.is_bot:
            if reply_to.from_user.username:
                tag = f"@{reply_to.from_user.username}"
            else:
                tag = reply_to.from_user.mention_html(reply_to.from_user.first_name)

        if (
            not is_url(link)
            and not is_magnet(link)
            or len(link) == 0
        ):

            if file is None:
                reply_text = reply_to.text
                if is_url(reply_text) or is_magnet(reply_text):
                    link = reply_text.strip()
            elif isQbit:
                file_name = str(time()).replace(".", "") + ".torrent"
                link = file.get_file().download(custom_path=file_name)
            elif file.mime_type != "application/x-bittorrent":
                listener = MirrorListener(bot, update, isZip, extract, isQbit, isLeech, pswd, tag)
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
                tg_downloader = TelegramDownloadHelper(listener)
                ms = update.message
                tg_downloader.add_download(ms, f'{DOWNLOAD_DIR}{listener.uid}/', name)
                return
            else:
                link = file.get_file().file_path
<<<<<<< HEAD
    if bot_utils.is_url(link) and not bot_utils.is_magnet(link) and not os.path.exists(link) and isQbit:
        resp = requests.get(link)
        if resp.status_code == 200:
            file_name = str(time.time()).replace(".", "") + ".torrent"
            open(file_name, "wb").write(resp.content)
            link = f"{file_name}"
        else:
            sendMessage("KESALAHAN: tautan mendapat respons HTTP:" + resp.status_code, bot, update)
            return

    elif not bot_utils.is_url(link) and not bot_utils.is_magnet(link):
        sendMessage('Tidak ada sumber unduhan yang disediakan', bot, update)
        return
    elif not os.path.exists(link) and not bot_utils.is_mega_link(link) and not bot_utils.is_gdrive_link(link) and not bot_utils.is_magnet(link):
        try:
            link = direct_link_generator(link)
        except DirectDownloadLinkException as e:
            LOGGER.info(e)
            if "ERROR:" in str(e):
                sendMessage(f"{e}", bot, update)
                return
            if "Youtube" in str(e):
                sendMessage(f"{e}", bot, update)
                return

    listener = MirrorListener(bot, update, pswd, isTar, extract, isZip, isQbit, isLeech)

    if bot_utils.is_gdrive_link(link):
        if not isTar and not extract and not isLeech:
            sendMessage(f"Gunakan /{BotCommands.CloneCommand} untuk mengkloning file/folder Google Drive\nGunakan /{BotCommands.TarMirrorCommand} untuk membuat tar folder Google Drive\nGunakan /{BotCommands.UnzipMirrorCommand} untuk mengekstrak arsip file Google Drive", bot, update)
            return
        res, size, name, files = gdriveTools.GoogleDriveHelper().clonehelper(link)
        if res != "":
            sendMessage(res, bot, update)
            return
        if TAR_UNZIP_LIMIT is not None:
            result = bot_utils.check_limit(size, TAR_UNZIP_LIMIT)
            if result:
                msg = f'Gagal, batas Tar/Unzip adalah {TAR_UNZIP_LIMIT}.\nUkuran File/Folder Anda adalah{get_readable_file_size(size)}.'
                sendMessage(msg, bot, update)
                return
        LOGGER.info(f"Download Name : {name}")
        drive = gdriveTools.GoogleDriveHelper(name, listener)
        gid = ''.join(random.SystemRandom().choices(string.ascii_letters + string.digits, k=12))
        download_status = DownloadStatus(drive, size, listener, gid)
        with download_dict_lock:
            download_dict[listener.uid] = download_status
        sendStatusMessage(update, bot)
        drive.download(link)

    elif bot_utils.is_mega_link(link):
        if BLOCK_MEGA_LINKS:
            sendMessage("Tautan mega diblokir!", bot, update)
            return
        link_type = bot_utils.get_mega_link_type(link)
        if link_type == "folder" and BLOCK_MEGA_FOLDER:
            sendMessage("Folder mega diblokir!", bot, update)
        else:
            mega_dl = MegaDownloadHelper()
            mega_dl.add_download(link, f'{DOWNLOAD_DIR}{listener.uid}/', listener)

    elif isQbit and (bot_utils.is_magnet(link) or os.path.exists(link)):
        qbit = QbitTorrent()
        qbit.add_torrent(link, f'{DOWNLOAD_DIR}{listener.uid}/', listener, qbitsel)

    else:
        ariaDlManager.add_download(link, f'{DOWNLOAD_DIR}{listener.uid}/', listener, name)
        sendStatusMessage(update, bot)

=======

    if len(mesg) > 1:
        try:
            ussr = quote(mesg[1], safe='')
            pssw = quote(mesg[2], safe='')
            link = link.split("://", maxsplit=1)
            link = f'{link[0]}://{ussr}:{pssw}@{link[1]}'
        except IndexError:
            pass

    if not is_url(link) and not is_magnet(link) and not ospath.exists(link):
        help_msg = "<b>Send link along with command line:</b>"
        help_msg += "\n<code>/command</code> {link} |newname pswd: mypassword [𝚣𝚒𝚙/𝚞𝚗𝚣𝚒𝚙]"
        help_msg += "\n\n<b>By replying to link or file:</b>"
        help_msg += "\n<code>/command</code> |newname pswd: mypassword [𝚣𝚒𝚙/𝚞𝚗𝚣𝚒𝚙]"
        help_msg += "\n\n<b>Direct link authorization:</b>"
        help_msg += "\n<code>/command</code> {link} |newname pswd: mypassword\nusername\npassword"
        help_msg += "\n\n<b>Qbittorrent selection:</b>"
        help_msg += "\n<code>/qbcommand</code> <b>s</b> {link} or by replying to {file}"
        return sendMessage(help_msg, bot, update)

    LOGGER.info(link)
    gdtot_link = is_gdtot_link(link)

    if not is_mega_link(link) and not isQbit and not is_magnet(link) \
       and not ospath.exists(link) and not is_gdrive_link(link) and not link.endswith('.torrent'):
        content_type = get_content_type(link)
        if content_type is None or match(r'text/html|text/plain', content_type):
            try:
                link = direct_link_generator(link)
                LOGGER.info(f"Generated link: {link}")
            except DirectDownloadLinkException as e:
                LOGGER.info(str(e))
                if str(e).startswith('ERROR:'):
                    return sendMessage(str(e), bot, update)
    elif isQbit and not is_magnet(link) and not ospath.exists(link):
        if link.endswith('.torrent'):
            content_type = None
        else:
            content_type = get_content_type(link)
        if content_type is None or match(r'application/x-bittorrent|application/octet-stream', content_type):
            try:
                resp = requests.get(link, timeout=10)
                if resp.status_code == 200:
                    file_name = str(time()).replace(".", "") + ".torrent"
                    open(file_name, "wb").write(resp.content)
                    link = f"{file_name}"
                else:
                    return sendMessage(f"ERROR: link got HTTP response: {resp.status_code}", bot, update)
            except Exception as e:
                error = str(e).replace('<', ' ').replace('>', ' ')
                if error.startswith('No connection adapters were found for'):
                    link = error.split("'")[1]
                else:
                    LOGGER.error(str(e))
                    return sendMessage(tag + " " + error, bot, update)
        else:
            msg = "Qb commands for torrents only. if you are trying to dowload torrent then report."
            return sendMessage(msg, bot, update)

    listener = MirrorListener(bot, update, isZip, extract, isQbit, isLeech, pswd, tag)

    if is_gdrive_link(link):
        if not isZip and not extract and not isLeech:
            gmsg = f"Use /{BotCommands.CloneCommand} to clone Google Drive file/folder\n\n"
            gmsg += f"Use /{BotCommands.ZipMirrorCommand} to make zip of Google Drive folder\n\n"
            gmsg += f"Use /{BotCommands.UnzipMirrorCommand} to extracts Google Drive archive file"
            return sendMessage(gmsg, bot, update)
        Thread(target=add_gd_download, args=(link, listener, gdtot_link)).start()

    elif is_mega_link(link):
        if BLOCK_MEGA_LINKS:
            sendMessage("Mega links are blocked!", bot, update)
            return
        link_type = get_mega_link_type(link)
        if link_type == "folder" and BLOCK_MEGA_FOLDER:
            sendMessage("Mega folder are blocked!", bot, update)
        else:
            Thread(target=add_mega_download, args=(link, f'{DOWNLOAD_DIR}{listener.uid}/', listener)).start()

    elif isQbit and (is_magnet(link) or ospath.exists(link)):
        Thread(target=add_qb_torrent, args=(link, f'{DOWNLOAD_DIR}{listener.uid}', listener, qbitsel)).start()

    else:
        Thread(target=add_aria2c_download, args=(link, f'{DOWNLOAD_DIR}{listener.uid}', listener, name)).start()
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9

def mirror(update, context):
    _mirror(context.bot, update)

<<<<<<< HEAD
def tar_mirror(update, context):
    _mirror(context.bot, update, True)

=======
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
def unzip_mirror(update, context):
    _mirror(context.bot, update, extract=True)

def zip_mirror(update, context):
<<<<<<< HEAD
    _mirror(context.bot, update, True, isZip=True)
=======
    _mirror(context.bot, update, True)
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9

def qb_mirror(update, context):
    _mirror(context.bot, update, isQbit=True)

<<<<<<< HEAD
def qb_tar_mirror(update, context):
    _mirror(context.bot, update, True, isQbit=True)

=======
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
def qb_unzip_mirror(update, context):
    _mirror(context.bot, update, extract=True, isQbit=True)

def qb_zip_mirror(update, context):
<<<<<<< HEAD
    _mirror(context.bot, update, True, isZip=True, isQbit=True)
=======
    _mirror(context.bot, update, True, isQbit=True)
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9

def leech(update, context):
    _mirror(context.bot, update, isLeech=True)

<<<<<<< HEAD
def tar_leech(update, context):
    _mirror(context.bot, update, True, isLeech=True)

=======
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
def unzip_leech(update, context):
    _mirror(context.bot, update, extract=True, isLeech=True)

def zip_leech(update, context):
<<<<<<< HEAD
    _mirror(context.bot, update, True, isZip=True, isLeech=True)
=======
    _mirror(context.bot, update, True, isLeech=True)
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9

def qb_leech(update, context):
    _mirror(context.bot, update, isQbit=True, isLeech=True)

<<<<<<< HEAD
def qb_tar_leech(update, context):
    _mirror(context.bot, update, True, isQbit=True, isLeech=True)

=======
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
def qb_unzip_leech(update, context):
    _mirror(context.bot, update, extract=True, isQbit=True, isLeech=True)

def qb_zip_leech(update, context):
<<<<<<< HEAD
    _mirror(context.bot, update, True, isZip=True, isQbit=True, isLeech=True)

mirror_handler = CommandHandler(BotCommands.MirrorCommand, mirror,
                                filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
tar_mirror_handler = CommandHandler(BotCommands.TarMirrorCommand, tar_mirror,
                                    filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
unzip_mirror_handler = CommandHandler(BotCommands.UnzipMirrorCommand, unzip_mirror,
                                      filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
zip_mirror_handler = CommandHandler(BotCommands.ZipMirrorCommand, zip_mirror,
                                    filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
qb_mirror_handler = CommandHandler(BotCommands.QbMirrorCommand, qb_mirror,
                                filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
qb_tar_mirror_handler = CommandHandler(BotCommands.QbTarMirrorCommand, qb_tar_mirror,
                                    filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
qb_unzip_mirror_handler = CommandHandler(BotCommands.QbUnzipMirrorCommand, qb_unzip_mirror,
                                      filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
qb_zip_mirror_handler = CommandHandler(BotCommands.QbZipMirrorCommand, qb_zip_mirror,
                                    filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
leech_handler = CommandHandler(BotCommands.LeechCommand, leech,
                                filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
tar_leech_handler = CommandHandler(BotCommands.TarLeechCommand, tar_leech,
=======
    _mirror(context.bot, update, True, isQbit=True, isLeech=True)

mirror_handler = CommandHandler(BotCommands.MirrorCommand, mirror,
                                filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
unzip_mirror_handler = CommandHandler(BotCommands.UnzipMirrorCommand, unzip_mirror,
                                filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
zip_mirror_handler = CommandHandler(BotCommands.ZipMirrorCommand, zip_mirror,
                                filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
qb_mirror_handler = CommandHandler(BotCommands.QbMirrorCommand, qb_mirror,
                                filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
qb_unzip_mirror_handler = CommandHandler(BotCommands.QbUnzipMirrorCommand, qb_unzip_mirror,
                                filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
qb_zip_mirror_handler = CommandHandler(BotCommands.QbZipMirrorCommand, qb_zip_mirror,
                                filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
leech_handler = CommandHandler(BotCommands.LeechCommand, leech,
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
                                filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
unzip_leech_handler = CommandHandler(BotCommands.UnzipLeechCommand, unzip_leech,
                                filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
zip_leech_handler = CommandHandler(BotCommands.ZipLeechCommand, zip_leech,
                                filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
qb_leech_handler = CommandHandler(BotCommands.QbLeechCommand, qb_leech,
                                filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
<<<<<<< HEAD
qb_tar_leech_handler = CommandHandler(BotCommands.QbTarLeechCommand, qb_tar_leech,
                                filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
=======
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
qb_unzip_leech_handler = CommandHandler(BotCommands.QbUnzipLeechCommand, qb_unzip_leech,
                                filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
qb_zip_leech_handler = CommandHandler(BotCommands.QbZipLeechCommand, qb_zip_leech,
                                filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
<<<<<<< HEAD
dispatcher.add_handler(mirror_handler)
dispatcher.add_handler(tar_mirror_handler)
dispatcher.add_handler(unzip_mirror_handler)
dispatcher.add_handler(zip_mirror_handler)
dispatcher.add_handler(qb_mirror_handler)
dispatcher.add_handler(qb_tar_mirror_handler)
dispatcher.add_handler(qb_unzip_mirror_handler)
dispatcher.add_handler(qb_zip_mirror_handler)
dispatcher.add_handler(leech_handler)
dispatcher.add_handler(tar_leech_handler)
dispatcher.add_handler(unzip_leech_handler)
dispatcher.add_handler(zip_leech_handler)
dispatcher.add_handler(qb_leech_handler)
dispatcher.add_handler(qb_tar_leech_handler)
=======

dispatcher.add_handler(mirror_handler)
dispatcher.add_handler(unzip_mirror_handler)
dispatcher.add_handler(zip_mirror_handler)
dispatcher.add_handler(qb_mirror_handler)
dispatcher.add_handler(qb_unzip_mirror_handler)
dispatcher.add_handler(qb_zip_mirror_handler)
dispatcher.add_handler(leech_handler)
dispatcher.add_handler(unzip_leech_handler)
dispatcher.add_handler(zip_leech_handler)
dispatcher.add_handler(qb_leech_handler)
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
dispatcher.add_handler(qb_unzip_leech_handler)
dispatcher.add_handler(qb_zip_leech_handler)
