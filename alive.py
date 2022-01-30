<<<<<<< HEAD
# Implement By - @anasty17 (https://github.com/breakdowns/slam-tg-mirror-bot/commit/0bfba523f095ab1dccad431d72561e0e002e7a59)
# (c) https://github.com/breakdowns/slam-aria-mirror-bot
# All rights reserved

import time
import requests
import os

BASE_URL = os.environ.get('BASE_URL_OF_BOT', None)
try:
    if len(BASE_URL) == 0:
        BASE_URL = None
except:
    BASE_URL = None
PORT = os.environ.get('PORT', None)
if PORT is not None and BASE_URL is not None:
    while True:
        time.sleep(600)
        status = requests.get(BASE_URL).status_code
=======
from time import sleep
from requests import get as rget
from os import environ
from logging import error as logerror

BASE_URL = environ.get('BASE_URL_OF_BOT', None)
try:
    if len(BASE_URL) == 0:
        raise TypeError
    BASE_URL = BASE_URL.rstrip("/")
except TypeError:
    BASE_URL = None
PORT = environ.get('PORT', None)
if PORT is not None and BASE_URL is not None:
    while True:
        try:
            rget(BASE_URL).status_code
            sleep(600)
        except Exception as e:
            logerror(f"alive.py: {e}")
            sleep(2)
            continue
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
