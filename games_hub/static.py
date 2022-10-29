import logging

'''Static Variables'''
PROJECT_NAME = "GamesHub"
GITHUB_URL = "https://github.com/lupohan44/GamesHub"
GITHUB_VERSION_URL = "https://raw.githubusercontent.com/lupohan44/GamesHub/main/version.py"
GITHUB_MIRROR_VERSION_URL = "https://ghproxy.com/" + GITHUB_VERSION_URL
STEAM_DB_FREE_GAMES_URL = "https://steamdb.info/upcoming/free/"
CONFIG_PATH = "config.json5"

# log format
LOG_FORMAT = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
LOG_FORMAT_WITHOUT_LEVEL_NAME = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
'''Static Variables END'''
