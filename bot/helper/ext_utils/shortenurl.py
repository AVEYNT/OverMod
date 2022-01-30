# Implemented by https://github.com/junedkh

<<<<<<< HEAD
import requests
import random
import base64
import pyshorteners
from urllib.parse import quote
from urllib3 import disable_warnings
from bot import SHORTENER, SHORTENER_API


def short_url(longurl):
    if "shorte.st" in SHORTENER:
        disable_warnings()
        return requests.get(f'http://api.shorte.st/stxt/{SHORTENER_API}/{longurl}', verify=False).text
    elif "linkvertise" in SHORTENER:
        url = quote(base64.b64encode(longurl.encode("utf-8")))
=======
import random

from requests import get as rget, post as rpost
from base64 import b64encode
from urllib.parse import quote
from urllib3 import disable_warnings

from bot import LOGGER, SHORTENER, SHORTENER_API


def short_url(longurl):
    if SHORTENER is None and SHORTENER_API is None:
        return longurl

    if "shorte.st" in SHORTENER:
        disable_warnings()
        link = rget(f'http://api.shorte.st/stxt/{SHORTENER_API}/{longurl}', verify=False).text
    elif "linkvertise" in SHORTENER:
        url = quote(b64encode(longurl.encode("utf-8")))
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
        linkvertise = [
            f"https://link-to.net/{SHORTENER_API}/{random.random() * 1000}/dynamic?r={url}",
            f"https://up-to-down.net/{SHORTENER_API}/{random.random() * 1000}/dynamic?r={url}",
            f"https://direct-link.net/{SHORTENER_API}/{random.random() * 1000}/dynamic?r={url}",
            f"https://file-link.net/{SHORTENER_API}/{random.random() * 1000}/dynamic?r={url}"]
<<<<<<< HEAD
        return random.choice(linkvertise)
    elif "bitly.com" in SHORTENER:
        s = pyshorteners.Shortener(api_key=SHORTENER_API)
        return s.bitly.short(longurl)
    elif "ouo.io" in SHORTENER:
        disable_warnings()
        return requests.get(f'http://ouo.io/api/{SHORTENER_API}?s={longurl}', verify=False).text
    else:
        return requests.get(f'https://{SHORTENER}/api?api={SHORTENER_API}&url={longurl}&format=text').text
=======
        link = random.choice(linkvertise)
    elif "bitly.com" in SHORTENER:
        shorten_url = "https://api-ssl.bit.ly/v4/shorten"
        params = {"long_url": longurl}
        headers = {"Authorization": f"Bearer {SHORTENER_API}"}
        response = rpost(shorten_url, json=params, headers=headers).json()
        link = response["link"]
    elif "ouo.io" in SHORTENER:
        disable_warnings()
        link = rget(f'http://ouo.io/api/{SHORTENER_API}?s={longurl}', verify=False).text
    else:
        link = rget(f'https://{SHORTENER}/api?api={SHORTENER_API}&url={quote(longurl)}&format=text').text

    if len(link) == 0:
        LOGGER.error("Something is Wrong with the url shortener")
        return longurl
    return link
>>>>>>> 2aaacf0bec6285ef29ff9bbb699762804dca37c9
