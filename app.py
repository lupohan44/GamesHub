import getopt
import pkgutil
import sys
import traceback
from typing import Dict
from urllib import request

from packaging import version

from games_hub.api import run_schedule_and_send_notification
from games_hub.logger import logger
from games_hub.message import *
from games_hub.utils import *
from version import *


class UpdateChecking:
    def __init__(self):
        self.enable = True


class LogSetting:
    def __init__(self):
        self.screenshotEnabled = False


class Config:
    def __init__(self):
        self.update_checking = UpdateChecking()
        self.loop_delay = 3000


config = Config()


def parse_config() -> Dict:
    logger.info(PARSING_CONFIG_MSG % CONFIG_PATH)
    if not os.path.exists(CONFIG_PATH):
        raise Exception(CONFIG_NOT_EXIST_ERROR_MSG)

    config_json = load_json(CONFIG_PATH)
    if "update" in config_json:
        if "check_update" in config_json["update"]:
            config.update_checking.enable = config_json["update"]["check_update"]
    enabled_plugins = {}
    if "plugins" in config_json:
        for plugin_name in config_json["plugins"]:
            if config_json["plugins"][plugin_name]["enable"]:
                del config_json["plugins"][plugin_name]["enable"]
                enabled_plugins[plugin_name] = config_json["plugins"][plugin_name]
    return enabled_plugins


def check_update():
    logger.info("Checking for update...")
    local_version = VERSION
    try:
        response = None
        try:
            response = request.urlopen(GITHUB_VERSION_URL, timeout=5)
        except Exception:
            # try to use mirror
            response = request.urlopen(GITHUB_MIRROR_VERSION_URL, timeout=5)
        github_version_py = response.read().decode('utf-8')
        github_version = github_version_py.split("=")[1].strip().replace('"', '')
        if version.parse(local_version) < version.parse(github_version):
            logger.warning(FOUND_NEW_VERSION_MSG % github_version)
            logger.warning(GITHUB_URL)
        else:
            logger.info(NO_NEW_VERSION_MSG)
    except:
        logger.warning(CANNOT_CHECK_UPDATE_WARNING_MSG)


def print_help():
    print("Usage: python %s [options]" % os.path.basename(__file__))
    print("Options:")
    print("  -h, --help\t\t\tPrint this help message")
    print("  -c, --check-update\t\tCheck for update")
    print("  -v, --version\t\t\tPrint version information")


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hvc", ["help", "version", "check-update"])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_help()
            sys.exit()
        elif opt in ("-v", "--version"):
            print(VERSION)
            sys.exit()
        elif opt in ("-c", "--check-update"):
            check_update()
            sys.exit()
    logger.info(center_format_text())
    logger.info(center_format_text(PROJECT_NAME))
    logger.info(center_format_text("Author: lupohan44"))
    logger.info(center_format_text("Version: %s" % VERSION))
    logger.info(center_format_text())
    enabled_plugins = parse_config()
    if config.update_checking.enable:
        check_update()
    if len(enabled_plugins) == 0:
        raise Exception(NO_PLUGINS_ENABLE_ERROR_MSG)
    if not os.path.exists('plugins'):
        raise Exception(NO_PLUGINS_FOLDER_ERROR_MSG)
    # try to enable plugins
    folders_under_plugins = []
    for dirs in os.listdir("plugins"):
        if os.path.isdir(os.path.join("plugins", dirs)):
            folders_under_plugins.append(dirs)
    if len(folders_under_plugins) == 0:
        raise Exception(PLUGINS_FOLDER_EMPTY_ERROR_MSG)
    enabled_plugins_folders = []
    for plugin_name in enabled_plugins:
        if plugin_name in folders_under_plugins:
            enabled_plugins_folders.append(os.path.join("plugins", plugin_name))
    if len(enabled_plugins_folders) == 0:
        raise Exception(NO_PLUGINS_ENABLE_ERROR_MSG)
    total_plugin_count = 0
    for finder, name, _ in pkgutil.iter_modules(enabled_plugins_folders):
        logger.info(LOADING_PLUGINS_MSG % name)
        try:
            module = finder.find_module(name).load_module(name)
        except Exception:
            logger.info(CANNOT_LOAD_PLUGIN_WARNING_MSG % (name, traceback.format_exc()))
            try:
                del sys.modules[name]
            except:
                pass
        else:
            logger.info(PLUGIN_LOADED_MSG % name)
            total_plugin_count += 1
    if total_plugin_count == 0:
        raise Exception(NO_PLUGINS_ENABLE_ERROR_MSG)
    run_schedule_and_send_notification()


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except Exception as e:
        logger.error(e)
        raise e
