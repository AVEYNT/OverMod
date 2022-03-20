import asyncio
import os
import subprocess
import time

import psutil
from bot import botStartTime
from bot.helper.ext_utils import formatter

async def bot_sys_stats():
    bot_uptime = int(time.time() - botStartTime)
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    process = psutil.Process(os.getpid())
    stats = f"""
Over Modular @AVEYNT
------------------
UPTIME: {formatter.get_readable_time(bot_uptime)}
BOT: {round(process.memory_info()[0] / 1024 ** 2)} MB
CPU: {cpu}%
RAM: {mem}%
DISK: {disk}%
"""
    return stats