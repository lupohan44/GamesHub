import logging
from version import *

'''Static Variables'''
GITHUB_URL = "https://github.com/lupohan44/SteamDBFreeGamesClaimer"
GITHUB_VERSION_URL = "https://raw.githubusercontent.com/lupohan44/SteamDBFreeGamesClaimer/main/version.py"
STEAM_DB_FREE_GAMES_URL = "https://steamdb.info/upcoming/free/"
CONFIG_PATH = "config.json5"
RECORD_PATH = "record.db"
FIRST_DELAY = 15
CANNOT_CHECK_UPDATE_WARNING_MSG = "Cannot check update from github!"
FOUND_NEW_VERSION_WARNING_MSG = "Found new version %s on github!"
NO_NEW_VERSION_MSG = "Current version is up to date!"
CONFIG_NOT_EXIST_ERROR_MSG = "Cannot read %s!" % CONFIG_PATH
TELEGRAM_REQUIRE_TOKEN_ERROR_MSG = "Cannot get token of telegram from %s!" % CONFIG_PATH
TELEGRAM_REQUIRE_CHAT_ID_ERROR_MSG = "Cannot get chat_id of telegram from %s!" % CONFIG_PATH
ASF_REQUIRE_IPC_ERROR_MSG = "Cannot get ipc of asf from %s!" % CONFIG_PATH
AT_LEAST_ENABLE_ONE_FUNCTION_ERROR_MSG = "Both telegram and asf are not enabled!"
CONFIG_FILE_NEEDS_TO_BE_UPDATED = "%s's format has been changed, please change it accordingly!" % CONFIG_PATH
GET_PAGE_SOURCE_ERROR_MSG = "Get page source error!"

# log format
LOG_FORMAT = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
LOG_FORMAT_WITHOUT_LEVEL_NAME = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
'''Static Variables END'''
