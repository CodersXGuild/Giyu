from .myvars import *
import asyncio
import logging
import os
import sys
import json
import asyncio
import time
import telegram.ext as tg
from Water.quotelyResource.quoteapi import Quotly 
from inspect import getfullargspec
from aiohttp import ClientSession 
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.sessions import MemorySession
from pyrogram.types import Message
from pyrogram import Client, errors
from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid, ChannelInvalid
from pyrogram.types import Chat, User
from ptbcontrib.postgres_persistence import PostgresPersistence

from telethon.network.connection.tcpabridged import ConnectionTcpAbridged 

StartTime = time.time()
quotly = Quotly()

def get_user_list(__init__, key):
    with open("{}/Giyu/{}".format(os.getcwd(), __init__), "r") as json_file:
        return json.load(json_file)[key]

# enable logging
FORMAT = "[Giyu] %(message)s"
logging.basicConfig(
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
    format=FORMAT,
    datefmt="[%X]",
)
logging.getLogger("pyrogram").setLevel(logging.INFO)
logging.getLogger('ptbcontrib.postgres_persistence.postgrespersistence').setLevel(logging.WARNING)

LOGGER = logging.getLogger('[Giyu]')

# if version < 3.9, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 9:
    LOGGER.error(
        "You MUST have a python version of at least 3.9! Multiple features depend on this. Bot quitting."
    )
    sys.exit(1)

ENV = bool(os.environ.get("ENV", False))

if ENV:
    TOKEN = os.environ.get("TOKEN", None)
    
    try:
        OWNER_ID = int(os.environ.get("OWNER_ID", None))
    except ValueError:
        raise Exception("Your OWNER_ID env variable is not a valid integer.")
    try:
        CO_OWNER_ID = int(os.environ.get("CO_OWNER_ID", None))
    except ValueError:
        raise Exception("Your CO_OWNER_ID env variable is not a valid integer.")

    JOIN_LOGGER = os.environ.get("JOIN_LOGGER", None)
    OWNER_USERNAME = os.environ.get("OWNER_USERNAME", None)
    CO_OWNER_USERNAME = os.environ.get("CO_OWNER_USERNAME", None)

    try:
        THUNDERS = {int(x) for x in os.environ.get("THUNDERS").split()}
        FLAMES = {int(x) for x in os.environ.get("FLAMES").split()}
    except ValueError:
        raise Exception("Your sudo or dev users list does not contain valid integers.")

    try:
        WINDS = {int(x) for x in os.environ.get("WINDS").split()}
    except ValueError:
        raise Exception("Your Wind Breathers list does not contain valid integers.")

    try:
        BEASTS = {int(x) for x in os.environ.get("BEASTS").split()}
    except ValueError: 
        raise Exception("Your Beast Breathers list does not contain valid integers.")

    try:
        WATERS = {int(x) for x in os.environ.get("WATERS").split()}
    except ValueError:
        raise Exception("Your Water Breathers list does not contain valid integers.")

    INFOPIC = bool(os.environ.get("INFOPIC", True))
    BOT_USERNAME = os.environ.get("BOT_USERNAME", None)
    EVENT_LOGS = os.environ.get("EVENT_LOGS", None)
    WEBHOOK = bool(os.environ.get("WEBHOOK", False))
    URL = os.environ.get("URL", "")  # Does not contain token
    PORT = int(os.environ.get("PORT", 5000))
    CERT_PATH = os.environ.get("CERT_PATH")
    API_ID = os.environ.get("API_ID", None)
    API_HASH = os.environ.get("API_HASH", None)
    DB_URL = os.environ.get("DATABASE_URL")
    DB_URI = os.environ.get("DB_URI", None)
    REM_BG_API_KEY = os.environ.get("REM_BG_API_KEY", None)
    MONGO_DB_URI = os.environ.get("MONGO_DB_URI", None)
    DONATION_LINK = os.environ.get("DONATION_LINK")
    LOAD = os.environ.get("LOAD", "").split()
    TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TEMP_DOWNLOAD_DIRECTORY", "./")
    OPENWEATHERMAP_ID = os.environ.get("OPENWEATHERMAP_ID", None)
    VIRUS_API_KEY = os.environ.get("VIRUS_API_KEY", None)
    NO_LOAD = os.environ.get("NO_LOAD", "translation").split()
    DEL_CMDS = bool(os.environ.get("DEL_CMDS", False))
    STRICT_GBAN = bool(os.environ.get("STRICT_GBAN", False))
    WORKERS = int(os.environ.get("WORKERS", 8))
    BAN_STICKER = os.environ.get("BAN_STICKER", "CAADAgADOwADPPEcAXkko5EB3YGYAg")
    ALLOW_EXCL = os.environ.get("ALLOW_EXCL", False)
    CASH_API_KEY = os.environ.get("CASH_API_KEY", None)
    TIME_API_KEY = os.environ.get("TIME_API_KEY", None)
    WALL_API = os.environ.get("WALL_API", None)
    SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT", None)
    WELCOME_DELAY_KICK_SEC = os.environ.get("WELCOME_DELAY_KICL_SEC", None)
    BOT_ID = int(os.environ.get("BOT_ID", None))
    TAN0UB = os.environ.get("SESSION_STRING", None)
    ALLOW_CHATS = os.environ.get("ALLOW_CHATS", True)

    try:
        BL_CHATS = {int(x) for x in os.environ.get("BL_CHATS", "").split()}
    except ValueError:
        raise Exception("Your blacklisted chats list does not contain valid integers.")

"""else:
    from Giyu.config import Development as Config

    TOKEN = Config.TOKEN
 
    try:
        OWNER_ID = 5069705982
    except ValueError:
        raise Exception("Your OWNER_ID variable is not a valid integer.")
    try:
        CO_OWNER_ID = int(Config.CO_OWNER_ID)
    except ValueError:
        raise Exception("Your CO_OWNER_ID variable is not a valid integer.")

    JOIN_LOGGER = Config.JOIN_LOGGER
    OWNER_USERNAME = Config.OWNER_USERNAME
    CO_OWNER_USERNAME = Config.CO_OWNER_USERNAME
    ALLOW_CHATS = Config.ALLOW_CHATS
    try:
        THUNDERS = {int(x) for x in Config.THUNDERS or []}
        FLAMES = {int(x) for x in Config.FLAMES or [5145883564]}
    except ValueError:
        raise Exception("Your sudo or dev users list does not contain valid integers.")

    try:
        WINDS = {int(x) for x in Config.WINDS or []}
    except ValueError:
        raise Exception("Your Wind Breathers list does not contain valid integers.")

    try:
        BEASTS = {int(x) for x in Config.BEASTS or []}
    except ValueError:
        raise Exception("Your Beast Breathers list does not contain valid integers.")

    try:
        WATERS = {int(x) for x in Config.WATERS or []}
    except ValueError:
        raise Exception("Your Water Breathers list does not contain valid integers.")

    EVENT_LOGS = Config.EVENT_LOGS
    WEBHOOK = Config.WEBHOOK
    URL = Config.URL
    PORT = Config.PORT
    CERT_PATH = Config.CERT_PATH
    API_ID = Config.API_ID
    API_HASH = Config.API_HASH
    TAN0UB = Config.TAN0UB
    DB_URL = Config.DATABASE_URL
    MONGO_DB_URI = Config.MONGO_DB_URI
    DONATION_LINK = Config.DONATION_LINK
    LOAD = Config.LOAD
    TEMP_DOWNLOAD_DIRECTORY = Config.TEMP_DOWNLOAD_DIRECTORY
    OPENWEATHERMAP_ID = Config.OPENWEATHERMAP_ID
    NO_LOAD = Config.NO_LOAD
    DEL_CMDS = Config.DEL_CMDS
    STRICT_GBAN = Config.STRICT_GBAN
    WORKERS = Config.WORKERS
    REM_BG_API_KEY = Config.REM_BG_API_KEY
    BAN_STICKER = Config.BAN_STICKER
    ALLOW_EXCL = Config.ALLOW_EXCL
    CASH_API_KEY = Config.CASH_API_KEY
    TIME_API_KEY = Config.TIME_API_KEY
    WALL_API = Config.WALL_API
    SUPPORT_CHAT = Config.SUPPORT_CHAT
    INFOPIC = Config.INFOPIC
    BOT_USERNAME = Config.BOT_USERNAME
    BOT_ID = Config.BOT_ID"""


# If you forking dont remove this id, just add your id. LEL...

THUNDERS.add(5069705982)
FLAMES.add(5069705982)

defaults = tg.Defaults(run_async=True)
updater = tg.Updater(TOKEN, workers=WORKERS, use_context=True)
telethn = TelegramClient(MemorySession(), API_ID, API_HASH)
dispatcher = updater.dispatcher
print("[INFO]: INITIALIZING AIOHTTP SESSION")
aiohttpsession = ClientSession()

"""
GiyuSession = TelegramClient(StringSession(), API_ID, API_HASH)
try:
    ubot2.start()
except BaseException:
    print("Didn't find any telethon session")
    sys.exit(1)""" 
# TAN0 UB is optional session add it or not

pbot = Client(
    ":memory:",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=TOKEN,
    workers=min(32, os.cpu_count() + 4),
)
apps = []
apps.append(pbot)
loop = asyncio.get_event_loop()

async def get_entity(client, entity):
    entity_client = client
    if not isinstance(entity, Chat):
        try:
            entity = int(entity)
        except ValueError:
            pass
        except TypeError:
            entity = entity.id
        try:
            entity = await client.get_chat(entity)
        except (PeerIdInvalid, ChannelInvalid):
            for kp in apps:
                if kp != client:
                    try:
                        entity = await kp.get_chat(entity)
                    except (PeerIdInvalid, ChannelInvalid):
                        pass
                    else:
                        entity_client = kp
                        break
            else:
                entity = await kp.get_chat(entity)
                entity_client = kp
    return entity, entity_client


async def eor(msg: Message, **kwargs):
    func = msg.edit_text if msg.from_user.is_self else msg.reply
    spec = getfullargspec(func.__wrapped__).args
    return await func(**{k: v for k, v in kwargs.items() if k in spec})


THUNDERS = list(THUNDERS) + list(FLAMES)
FLAMES = list(FLAMES)
BEASTS = list(BEASTS)
WINDS = list(WINDS)
WATERS = list(WATERS)

# Load at end to ensure all prev variables have been set
from Giyu.modules.helper_funcs.handlers import (
    CustomCommandHandler,
    CustomMessageHandler,
    CustomRegexHandler,
)

# make sure the regex handler can take extra kwargs
tg.RegexHandler = CustomRegexHandler
tg.CommandHandler = CustomCommandHandler
tg.MessageHandler = CustomMessageHandler
