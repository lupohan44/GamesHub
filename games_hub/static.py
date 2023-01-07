import logging
import os
from pathlib import Path


'''Static Variables'''
PROJECT_NAME = "GamesHub"
GITHUB_URL = "https://github.com/lupohan44/GamesHub"
GITHUB_VERSION_URL = "https://raw.githubusercontent.com/lupohan44/GamesHub/main/version.py"
GITHUB_MIRROR_VERSION_URL = "https://ghproxy.com/" + GITHUB_VERSION_URL
# If set to true, GamesHub will store config in the current working directory as opposed to the src directory
GAMESHUB_CONF_DIR_CWD = os.environ.get("GAMESHUB_CONF_DIR_CWD", False) == "true"
GAMESHUB_SRC_DIR = Path(__file__).parent.parent
GAMESHUB_CONFIG_DIR = os.getcwd() if GAMESHUB_CONF_DIR_CWD else GAMESHUB_SRC_DIR

GAMESHUB_CONFIG_FILE = os.path.join(GAMESHUB_CONFIG_DIR, "config.json5")
# log format
LOG_FORMAT = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
LOG_FORMAT_WITHOUT_LEVEL_NAME = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
'''Static Variables END'''
