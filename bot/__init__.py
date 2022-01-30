import logging
<<<<<<< HEAD
import os
import threading
import time
import random
import string
import subprocess
import requests

import aria2p
import qbittorrentapi as qba
import telegram.ext as tg
from dotenv import load_dotenv
from pyrogram import Client
from telegraph import Telegraph

import psycopg2
from psycopg2 import Error

import socket
import faulthandler
=======
import socket
import faulthandler

from telegram.ext import Updater as tgUpdater
from qbittorrentapi import Client as qbClient
from aria2p import API as ariaAPI, Client as ariaClient
from os import remove as osremove, path as ospath, environ
from requests import get as rget
from json import loads as jsnloads
from subprocess import Popen, run as srun, check_output
from time import sleep, time
from threading import Thread, Lock
from pyrogram import Client
from dotenv import load_dotenv

>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
faulthandler.enable()

socket.setdefaulttimeout(600)

<<<<<<< HEAD
botStartTime = time.time()
if os.path.exists('log.txt'):
    with open('log.txt', 'r+') as f:
        f.truncate(0)
=======
botStartTime = time()
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
                    level=logging.INFO)

LOGGER = logging.getLogger(__name__)

<<<<<<< HEAD
CONFIG_FILE_URL = os.environ.get('CONFIG_FILE_URL', None)
if CONFIG_FILE_URL is not None:
    res = requests.get(CONFIG_FILE_URL)
    if res.status_code == 200:
        with open('config.env', 'wb+') as f:
            f.write(res.content)
            f.close()
    else:
        logging.error(res.status_code)

load_dotenv('config.env')

SERVER_PORT = os.environ.get('SERVER_PORT', None)
PORT = os.environ.get('PORT', SERVER_PORT)
web = subprocess.Popen([f"gunicorn wserver:start_server --bind 0.0.0.0:{PORT} --worker-class aiohttp.GunicornWebWorker"], shell=True)
time.sleep(1)
alive = subprocess.Popen(["python3", "alive.py"])
subprocess.run(["mkdir", "-p", "qBittorrent/config"])
subprocess.run(["cp", "qBittorrent.conf", "qBittorrent/config/qBittorrent.conf"])
subprocess.run(["qbittorrent-nox", "-d", "--profile=."])
=======
load_dotenv('config.env', override=True)

def getConfig(name: str):
    return environ[name]

try:
    NETRC_URL = getConfig('NETRC_URL')
    if len(NETRC_URL) == 0:
        raise KeyError
    try:
        res = rget(NETRC_URL)
        if res.status_code == 200:
            with open('.netrc', 'wb+') as f:
                f.write(res.content)
                f.close()
        else:
            logging.error(f"Failed to download .netrc {res.status_code}")
    except Exception as e:
        logging.error(f"NETRC_URL: {e}")
except KeyError:
    pass
try:
    SERVER_PORT = getConfig('SERVER_PORT')
    if len(SERVER_PORT) == 0:
        raise KeyError
except KeyError:
    SERVER_PORT = 80

PORT = environ.get('PORT', SERVER_PORT)
web = Popen([f"gunicorn wserver:start_server --bind 0.0.0.0:{PORT} --worker-class aiohttp.GunicornWebWorker"], shell=True)
alive = Popen(["python3", "alive.py"])
nox = Popen(["qbittorrent-nox", "--profile=."])
if not ospath.exists('.netrc'):
    srun(["touch", ".netrc"])
srun(["cp", ".netrc", "/root/.netrc"])
srun(["chmod", "600", ".netrc"])
srun(["chmod", "+x", "aria.sh"])
a2c = Popen(["./aria.sh"], shell=True)
sleep(1)

>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
Interval = []
DRIVES_NAMES = []
DRIVES_IDS = []
INDEX_URLS = []

<<<<<<< HEAD
def getConfig(name: str):
    return os.environ[name]

def mktable():
    try:
        conn = psycopg2.connect(DB_URI)
        cur = conn.cursor()
        sql = "CREATE TABLE users (uid bigint, sudo boolean DEFAULT FALSE);"
        cur.execute(sql)
        conn.commit()
        logging.info("Table Created!")
    except Error as e:
        logging.error(e)
        exit(1)

=======
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
try:
    if bool(getConfig('_____REMOVE_THIS_LINE_____')):
        logging.error('The README.md file there to be read! Exiting now!')
        exit()
except KeyError:
    pass

<<<<<<< HEAD
aria2 = aria2p.API(
    aria2p.Client(
=======
aria2 = ariaAPI(
    ariaClient(
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
        host="http://localhost",
        port=6800,
        secret="",
    )
)

<<<<<<< HEAD

def get_client() -> qba.TorrentsAPIMixIn:
    qb_client = qba.Client(host="localhost", port=8090, username="admin", password="adminadmin")
    try:
        qb_client.auth_log_in()
        #qb_client.application.set_preferences({"disk_cache":64, "incomplete_files_ext":True, "max_connec":3000, "max_connec_per_torrent":300, "async_io_threads":8, "preallocate_all":True, "upnp":True, "dl_limit":-1, "up_limit":-1, "dht":True, "pex":True, "lsd":True, "encryption":0, "queueing_enabled":True, "max_active_downloads":15, "max_active_torrents":50, "dont_count_slow_torrents":True, "bittorrent_protocol":0, "recheck_completed_torrents":True, "enable_multi_connections_from_same_ip":True, "slow_torrent_dl_rate_threshold":100,"slow_torrent_inactive_timer":600})
        return qb_client
    except qba.LoginFailed as e:
        logging.error(str(e))
        return None

=======
def get_client():
    return qbClient(host="localhost", port=8090)

trackers = check_output(["curl -Ns https://raw.githubusercontent.com/XIU2/TrackersListCollection/master/all.txt https://ngosang.github.io/trackerslist/trackers_all_http.txt https://newtrackon.com/api/all | awk '$0'"], shell=True).decode('utf-8')
trackerslist = set(trackers.split("\n"))
trackerslist.remove("")
trackerslist = "\n\n".join(trackerslist)
get_client().application.set_preferences({"add_trackers": f"{trackerslist}"})
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9

DOWNLOAD_DIR = None
BOT_TOKEN = None

<<<<<<< HEAD
download_dict_lock = threading.Lock()
status_reply_dict_lock = threading.Lock()
=======
download_dict_lock = Lock()
status_reply_dict_lock = Lock()
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
# Key: update.effective_chat.id
# Value: telegram.Message
status_reply_dict = {}
# Key: update.message.message_id
# Value: An object of Status
download_dict = {}
<<<<<<< HEAD
# Stores list of users and chats the bot is authorized to use in
=======
# key: rss_title
# value: [rss_feed, last_link, last_title, filter]
rss_dict = {}

>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
AUTHORIZED_CHATS = set()
SUDO_USERS = set()
AS_DOC_USERS = set()
AS_MEDIA_USERS = set()
<<<<<<< HEAD
if os.path.exists('authorized_chats.txt'):
=======
if ospath.exists('authorized_chats.txt'):
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
    with open('authorized_chats.txt', 'r+') as f:
        lines = f.readlines()
        for line in lines:
            AUTHORIZED_CHATS.add(int(line.split()[0]))
<<<<<<< HEAD
if os.path.exists('sudo_users.txt'):
=======
if ospath.exists('sudo_users.txt'):
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
    with open('sudo_users.txt', 'r+') as f:
        lines = f.readlines()
        for line in lines:
            SUDO_USERS.add(int(line.split()[0]))
try:
    achats = getConfig('AUTHORIZED_CHATS')
    achats = achats.split(" ")
    for chats in achats:
        AUTHORIZED_CHATS.add(int(chats))
except:
    pass
try:
    schats = getConfig('SUDO_USERS')
    schats = schats.split(" ")
    for chats in schats:
        SUDO_USERS.add(int(chats))
except:
    pass
try:
    BOT_TOKEN = getConfig('BOT_TOKEN')
    parent_id = getConfig('GDRIVE_FOLDER_ID')
    DOWNLOAD_DIR = getConfig('DOWNLOAD_DIR')
    if not DOWNLOAD_DIR.endswith("/"):
        DOWNLOAD_DIR = DOWNLOAD_DIR + '/'
    DOWNLOAD_STATUS_UPDATE_INTERVAL = int(getConfig('DOWNLOAD_STATUS_UPDATE_INTERVAL'))
    OWNER_ID = int(getConfig('OWNER_ID'))
    AUTO_DELETE_MESSAGE_DURATION = int(getConfig('AUTO_DELETE_MESSAGE_DURATION'))
    TELEGRAM_API = getConfig('TELEGRAM_API')
    TELEGRAM_HASH = getConfig('TELEGRAM_HASH')
except KeyError as e:
    LOGGER.error("One or more env variables missing! Exiting now")
    exit(1)
<<<<<<< HEAD
=======

LOGGER.info("Generating BOT_STRING_SESSION")
app = Client('pyrogram', api_id=int(TELEGRAM_API), api_hash=TELEGRAM_HASH, bot_token=BOT_TOKEN, no_updates=True)

try:
    USER_STRING_SESSION = getConfig('USER_STRING_SESSION')
    if len(USER_STRING_SESSION) == 0:
        raise KeyError
except KeyError:
    USER_STRING_SESSION = None

if USER_STRING_SESSION is not None:
    rss_session = Client(USER_STRING_SESSION, api_id=int(TELEGRAM_API), api_hash=TELEGRAM_HASH)
else:
    rss_session = None

def aria2c_init():
    try:
        logging.info("Initializing Aria2c")
        link = "https://releases.ubuntu.com/21.10/ubuntu-21.10-desktop-amd64.iso.torrent"
        dire = DOWNLOAD_DIR.rstrip("/")
        aria2.add_uris([link], {'dir': dire})
        sleep(3)
        downloads = aria2.get_downloads()
        sleep(30)
        for download in downloads:
            aria2.remove([download], force=True, files=True)
    except Exception as e:
        logging.error(f"Aria2c initializing error: {e}")
        pass

if not ospath.isfile(".restartmsg"):
    sleep(1)
    Thread(target=aria2c_init).start()
    sleep(1.5)

>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
try:
    DB_URI = getConfig('DATABASE_URL')
    if len(DB_URI) == 0:
        raise KeyError
except KeyError:
    DB_URI = None
<<<<<<< HEAD
if DB_URI is not None:
    try:
        conn = psycopg2.connect(DB_URI)
        cur = conn.cursor()
        sql = "SELECT * from users;"
        cur.execute(sql)
        rows = cur.fetchall()  #returns a list ==> (uid, sudo)
        for row in rows:
            AUTHORIZED_CHATS.add(row[0])
            if row[1]:
                SUDO_USERS.add(row[0])
    except Error as e:
        if 'relation "users" does not exist' in str(e):
            mktable()
        else:
            LOGGER.error(e)
            exit(1)
    finally:
        cur.close()
        conn.close()

LOGGER.info("Generating USER_SESSION_STRING")
app = Client('OverMod', api_id=int(TELEGRAM_API), api_hash=TELEGRAM_HASH, bot_token=BOT_TOKEN)

# Generate Telegraph Token
sname = ''.join(random.SystemRandom().choices(string.ascii_letters, k=8))
LOGGER.info("Generating TELEGRAPH_TOKEN using '" + sname + "' name")
telegraph = Telegraph()
telegraph.create_account(short_name=sname)
telegraph_token = telegraph.get_access_token()

try:
    TG_SPLIT_SIZE = getConfig('TG_SPLIT_SIZE')
    if len(TG_SPLIT_SIZE) == 0 or int(TG_SPLIT_SIZE) > 2097152000:
=======
try:
    TG_SPLIT_SIZE = getConfig('TG_SPLIT_SIZE')
    if len(TG_SPLIT_SIZE) == 0 or int(TG_SPLIT_SIZE) > 2097151000:
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
        raise KeyError
    else:
        TG_SPLIT_SIZE = int(TG_SPLIT_SIZE)
except KeyError:
<<<<<<< HEAD
    TG_SPLIT_SIZE = 2097152000
=======
    TG_SPLIT_SIZE = 2097151000
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
try:
    STATUS_LIMIT = getConfig('STATUS_LIMIT')
    if len(STATUS_LIMIT) == 0:
        raise KeyError
    else:
        STATUS_LIMIT = int(STATUS_LIMIT)
except KeyError:
    STATUS_LIMIT = None
try:
    MEGA_API_KEY = getConfig('MEGA_API_KEY')
<<<<<<< HEAD
=======
    if len(MEGA_API_KEY) == 0:
        raise KeyError
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
except KeyError:
    logging.warning('MEGA API KEY not provided!')
    MEGA_API_KEY = None
try:
    MEGA_EMAIL_ID = getConfig('MEGA_EMAIL_ID')
    MEGA_PASSWORD = getConfig('MEGA_PASSWORD')
    if len(MEGA_EMAIL_ID) == 0 or len(MEGA_PASSWORD) == 0:
        raise KeyError
except KeyError:
    logging.warning('MEGA Credentials not provided!')
    MEGA_EMAIL_ID = None
    MEGA_PASSWORD = None
try:
    UPTOBOX_TOKEN = getConfig('UPTOBOX_TOKEN')
<<<<<<< HEAD
except KeyError:
    logging.warning('UPTOBOX_TOKEN not provided!')
    UPTOBOX_TOKEN = None
try:
    INDEX_URL = getConfig('INDEX_URL')
    if len(INDEX_URL) == 0:
        INDEX_URL = None
        INDEX_URLS.append(None)
=======
    if len(UPTOBOX_TOKEN) == 0:
        raise KeyError
except KeyError:
    UPTOBOX_TOKEN = None
try:
    INDEX_URL = getConfig('INDEX_URL').rstrip("/")
    if len(INDEX_URL) == 0:
        raise KeyError
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
    else:
        INDEX_URLS.append(INDEX_URL)
except KeyError:
    INDEX_URL = None
    INDEX_URLS.append(None)
try:
<<<<<<< HEAD
    TORRENT_DIRECT_LIMIT = getConfig('TORRENT_DIRECT_LIMIT')
    if len(TORRENT_DIRECT_LIMIT) == 0:
        TORRENT_DIRECT_LIMIT = None
=======
    SEARCH_API_LINK = getConfig('SEARCH_API_LINK').rstrip("/")
    if len(SEARCH_API_LINK) == 0:
        raise KeyError
except KeyError:
    SEARCH_API_LINK = None
try:
    RSS_COMMAND = getConfig('RSS_COMMAND')
    if len(RSS_COMMAND) == 0:
        raise KeyError
except KeyError:
    RSS_COMMAND = None
try:
    TORRENT_DIRECT_LIMIT = getConfig('TORRENT_DIRECT_LIMIT')
    if len(TORRENT_DIRECT_LIMIT) == 0:
        raise KeyError
    else:
        TORRENT_DIRECT_LIMIT = float(TORRENT_DIRECT_LIMIT)
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
except KeyError:
    TORRENT_DIRECT_LIMIT = None
try:
    CLONE_LIMIT = getConfig('CLONE_LIMIT')
    if len(CLONE_LIMIT) == 0:
<<<<<<< HEAD
        CLONE_LIMIT = None
=======
        raise KeyError
    else:
        CLONE_LIMIT = float(CLONE_LIMIT)
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
except KeyError:
    CLONE_LIMIT = None
try:
    MEGA_LIMIT = getConfig('MEGA_LIMIT')
    if len(MEGA_LIMIT) == 0:
<<<<<<< HEAD
        MEGA_LIMIT = None
except KeyError:
    MEGA_LIMIT = None
try:
    TAR_UNZIP_LIMIT = getConfig('TAR_UNZIP_LIMIT')
    if len(TAR_UNZIP_LIMIT) == 0:
        TAR_UNZIP_LIMIT = None
except KeyError:
    TAR_UNZIP_LIMIT = None
=======
        raise KeyError
    else:
        MEGA_LIMIT = float(MEGA_LIMIT)
except KeyError:
    MEGA_LIMIT = None
try:
    ZIP_UNZIP_LIMIT = getConfig('ZIP_UNZIP_LIMIT')
    if len(ZIP_UNZIP_LIMIT) == 0:
        raise KeyError
    else:
        ZIP_UNZIP_LIMIT = float(ZIP_UNZIP_LIMIT)
except KeyError:
    ZIP_UNZIP_LIMIT = None
try:
    RSS_CHAT_ID = getConfig('RSS_CHAT_ID')
    if len(RSS_CHAT_ID) == 0:
        raise KeyError
    else:
        RSS_CHAT_ID = int(RSS_CHAT_ID)
except KeyError:
    RSS_CHAT_ID = None
try:
    RSS_DELAY = getConfig('RSS_DELAY')
    if len(RSS_DELAY) == 0:
        raise KeyError
    else:
        RSS_DELAY = int(RSS_DELAY)
except KeyError:
    RSS_DELAY = 900
try:
    QB_TIMEOUT = getConfig('QB_TIMEOUT')
    if len(QB_TIMEOUT) == 0:
        raise KeyError
    else:
        QB_TIMEOUT = int(QB_TIMEOUT)
except KeyError:
    QB_TIMEOUT = None
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
try:
    BUTTON_FOUR_NAME = getConfig('BUTTON_FOUR_NAME')
    BUTTON_FOUR_URL = getConfig('BUTTON_FOUR_URL')
    if len(BUTTON_FOUR_NAME) == 0 or len(BUTTON_FOUR_URL) == 0:
        raise KeyError
except KeyError:
    BUTTON_FOUR_NAME = None
    BUTTON_FOUR_URL = None
try:
    BUTTON_FIVE_NAME = getConfig('BUTTON_FIVE_NAME')
    BUTTON_FIVE_URL = getConfig('BUTTON_FIVE_URL')
    if len(BUTTON_FIVE_NAME) == 0 or len(BUTTON_FIVE_URL) == 0:
        raise KeyError
except KeyError:
    BUTTON_FIVE_NAME = None
    BUTTON_FIVE_URL = None
try:
    BUTTON_SIX_NAME = getConfig('BUTTON_SIX_NAME')
    BUTTON_SIX_URL = getConfig('BUTTON_SIX_URL')
    if len(BUTTON_SIX_NAME) == 0 or len(BUTTON_SIX_URL) == 0:
        raise KeyError
except KeyError:
    BUTTON_SIX_NAME = None
    BUTTON_SIX_URL = None
try:
    STOP_DUPLICATE = getConfig('STOP_DUPLICATE')
    STOP_DUPLICATE = STOP_DUPLICATE.lower() == 'true'
except KeyError:
    STOP_DUPLICATE = False
try:
    VIEW_LINK = getConfig('VIEW_LINK')
    VIEW_LINK = VIEW_LINK.lower() == 'true'
except KeyError:
    VIEW_LINK = False
try:
    IS_TEAM_DRIVE = getConfig('IS_TEAM_DRIVE')
    IS_TEAM_DRIVE = IS_TEAM_DRIVE.lower() == 'true'
except KeyError:
    IS_TEAM_DRIVE = False
try:
    USE_SERVICE_ACCOUNTS = getConfig('USE_SERVICE_ACCOUNTS')
    USE_SERVICE_ACCOUNTS = USE_SERVICE_ACCOUNTS.lower() == 'true'
except KeyError:
    USE_SERVICE_ACCOUNTS = False
try:
    BLOCK_MEGA_FOLDER = getConfig('BLOCK_MEGA_FOLDER')
    BLOCK_MEGA_FOLDER = BLOCK_MEGA_FOLDER.lower() == 'true'
except KeyError:
    BLOCK_MEGA_FOLDER = False
try:
    BLOCK_MEGA_LINKS = getConfig('BLOCK_MEGA_LINKS')
    BLOCK_MEGA_LINKS = BLOCK_MEGA_LINKS.lower() == 'true'
except KeyError:
    BLOCK_MEGA_LINKS = False
try:
<<<<<<< HEAD
=======
    WEB_PINCODE = getConfig('WEB_PINCODE')
    WEB_PINCODE = WEB_PINCODE.lower() == 'true'
except KeyError:
    WEB_PINCODE = False
try:
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
    SHORTENER = getConfig('SHORTENER')
    SHORTENER_API = getConfig('SHORTENER_API')
    if len(SHORTENER) == 0 or len(SHORTENER_API) == 0:
        raise KeyError
except KeyError:
    SHORTENER = None
    SHORTENER_API = None
try:
    IGNORE_PENDING_REQUESTS = getConfig("IGNORE_PENDING_REQUESTS")
    IGNORE_PENDING_REQUESTS = IGNORE_PENDING_REQUESTS.lower() == 'true'
except KeyError:
    IGNORE_PENDING_REQUESTS = False
try:
<<<<<<< HEAD
    BASE_URL = getConfig('BASE_URL_OF_BOT')
=======
    BASE_URL = getConfig('BASE_URL_OF_BOT').rstrip("/")
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
    if len(BASE_URL) == 0:
        raise KeyError
except KeyError:
    logging.warning('BASE_URL_OF_BOT not provided!')
    BASE_URL = None
try:
    IS_VPS = getConfig('IS_VPS')
    IS_VPS = IS_VPS.lower() == 'true'
except KeyError:
    IS_VPS = False
try:
    AS_DOCUMENT = getConfig('AS_DOCUMENT')
    AS_DOCUMENT = AS_DOCUMENT.lower() == 'true'
except KeyError:
    AS_DOCUMENT = False
try:
<<<<<<< HEAD
    RECURSIVE_SEARCH = getConfig('RECURSIVE_SEARCH')
    RECURSIVE_SEARCH = RECURSIVE_SEARCH.lower() == 'true'
except KeyError:
    RECURSIVE_SEARCH = False
try:
    TOKEN_PICKLE_URL = getConfig('TOKEN_PICKLE_URL')
    if len(TOKEN_PICKLE_URL) == 0:
        TOKEN_PICKLE_URL = None
    else:
        res = requests.get(TOKEN_PICKLE_URL)
=======
    EQUAL_SPLITS = getConfig('EQUAL_SPLITS')
    EQUAL_SPLITS = EQUAL_SPLITS.lower() == 'true'
except KeyError:
    EQUAL_SPLITS = False
try:
    QB_SEED = getConfig('QB_SEED')
    QB_SEED = QB_SEED.lower() == 'true'
except KeyError:
    QB_SEED = False
try:
    CUSTOM_FILENAME = getConfig('CUSTOM_FILENAME')
    if len(CUSTOM_FILENAME) == 0:
        raise KeyError
except KeyError:
    CUSTOM_FILENAME = None
try:
    PHPSESSID = getConfig('PHPSESSID')
    CRYPT = getConfig('CRYPT')
    if len(PHPSESSID) == 0 or len(CRYPT) == 0:
        raise KeyError
except KeyError:
    PHPSESSID = None
    CRYPT = None
try:
    TOKEN_PICKLE_URL = getConfig('TOKEN_PICKLE_URL')
    if len(TOKEN_PICKLE_URL) == 0:
        raise KeyError
    try:
        res = rget(TOKEN_PICKLE_URL)
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
        if res.status_code == 200:
            with open('token.pickle', 'wb+') as f:
                f.write(res.content)
                f.close()
        else:
<<<<<<< HEAD
            logging.error(res.status_code)
            raise KeyError
=======
            logging.error(f"Failed to download token.pickle, link got HTTP response: {res.status_code}")
    except Exception as e:
        logging.error(f"TOKEN_PICKLE_URL: {e}")
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
except KeyError:
    pass
try:
    ACCOUNTS_ZIP_URL = getConfig('ACCOUNTS_ZIP_URL')
    if len(ACCOUNTS_ZIP_URL) == 0:
<<<<<<< HEAD
        ACCOUNTS_ZIP_URL = None
    else:
        res = requests.get(ACCOUNTS_ZIP_URL)
        if res.status_code == 200:
            with open('accounts.zip', 'wb+') as f:
                f.write(res.content)
                f.close()
        else:
            logging.error(res.status_code)
            raise KeyError
        subprocess.run(["unzip", "-q", "-o", "accounts.zip"])
        os.remove("accounts.zip")
=======
        raise KeyError
    else:
        try:
            res = rget(ACCOUNTS_ZIP_URL)
            if res.status_code == 200:
                with open('accounts.zip', 'wb+') as f:
                    f.write(res.content)
                    f.close()
            else:
                logging.error(f"Failed to download accounts.zip, link got HTTP response: {res.status_code}")
        except Exception as e:
            logging.error(f"ACCOUNTS_ZIP_URL: {e}")
            raise KeyError
        srun(["unzip", "-q", "-o", "accounts.zip"])
        srun(["chmod", "-R", "777", "accounts"])
        osremove("accounts.zip")
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
except KeyError:
    pass
try:
    MULTI_SEARCH_URL = getConfig('MULTI_SEARCH_URL')
    if len(MULTI_SEARCH_URL) == 0:
<<<<<<< HEAD
        MULTI_SEARCH_URL = None
    else:
        res = requests.get(MULTI_SEARCH_URL)
=======
        raise KeyError
    try:
        res = rget(MULTI_SEARCH_URL)
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
        if res.status_code == 200:
            with open('drive_folder', 'wb+') as f:
                f.write(res.content)
                f.close()
        else:
<<<<<<< HEAD
            logging.error(res.status_code)
            raise KeyError
=======
            logging.error(f"Failed to download drive_folder, link got HTTP response: {res.status_code}")
    except Exception as e:
        logging.error(f"MULTI_SEARCH_URL: {e}")
except KeyError:
    pass
try:
    YT_COOKIES_URL = getConfig('YT_COOKIES_URL')
    if len(YT_COOKIES_URL) == 0:
        raise KeyError
    try:
        res = rget(YT_COOKIES_URL)
        if res.status_code == 200:
            with open('cookies.txt', 'wb+') as f:
                f.write(res.content)
                f.close()
        else:
            logging.error(f"Failed to download cookies.txt, link got HTTP response: {res.status_code}")
    except Exception as e:
        logging.error(f"YT_COOKIES_URL: {e}")
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
except KeyError:
    pass

DRIVES_NAMES.append("Main")
DRIVES_IDS.append(parent_id)
<<<<<<< HEAD
if os.path.exists('drive_folder'):
=======
if ospath.exists('drive_folder'):
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
    with open('drive_folder', 'r+') as f:
        lines = f.readlines()
        for line in lines:
            try:
                temp = line.strip().split()
                DRIVES_IDS.append(temp[1])
                DRIVES_NAMES.append(temp[0].replace("_", " "))
            except:
                pass
            try:
                INDEX_URLS.append(temp[2])
            except IndexError as e:
                INDEX_URLS.append(None)
<<<<<<< HEAD

updater = tg.Updater(token=BOT_TOKEN)
bot = updater.bot
dispatcher = updater.dispatcher
=======
try:
    SEARCH_PLUGINS = getConfig('SEARCH_PLUGINS')
    if len(SEARCH_PLUGINS) == 0:
        raise KeyError
    SEARCH_PLUGINS = jsnloads(SEARCH_PLUGINS)
except KeyError:
    SEARCH_PLUGINS = None

updater = tgUpdater(token=BOT_TOKEN)
bot = updater.bot
dispatcher = updater.dispatcher
job_queue = updater.job_queue
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
