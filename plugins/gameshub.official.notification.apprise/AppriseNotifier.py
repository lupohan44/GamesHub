import datetime
from typing import List

import apprise

from games_hub.api import receiver
from games_hub.logger import logger
from games_hub.message import *
from games_hub.types import *
from games_hub.utils import *

"""static variables"""
__name__ = "Apprise Notifier"
__package__ = "gameshub.official.notification.apprise"
config_folder = os.path.split(os.path.realpath(__file__))[0]
config_path = os.path.join(config_folder, "config.json5")
config_example_path = os.path.join(config_folder, "config.example.json5")
if not os.path.exists(config_path):
    config_folder = os.path.join('plugins', __package__)
    if not os.path.exists(config_folder):
        os.mkdir(config_folder)
    config_path = os.path.join(config_folder, "config.json5")
    shutil.copy(config_example_path, config_path)
"""static variables END"""


class TimeFormat:
    def __init__(self):
        self.utc_offset = 0
        self.format_str = "%Y/%m/%d %H:%M"


class Notification:
    def __init__(self):
        self.servers = ""
        self.notification_free_type: List[GameFreeType] = []
        self.game_platforms: List[GamePlatform] = []
        self.title = ""
        self.body = ""


class Config:
    def __init__(self):
        self.time_format = TimeFormat()
        self.notifications: List[Notification] = []


def parse_config():
    logger.info(PARSING_CONFIG_MSG % config_path)
    if not os.path.exists(config_path):
        raise Exception(CONFIG_NOT_EXIST_ERROR_MSG)
    config_json = load_json(config_path)
    if "time_format" in config_json:
        if "utc_offset" in config_json["time_format"]:
            config.time_format.utc_offset = config_json["time_format"]["utc_offset"]
        if "format_str" in config_json["time_format"]:
            config.time_format.format_str = config_json["time_format"]["format_str"]
    if "notifications" in config_json:
        for notification_json in config_json["notifications"]:
            notification = Notification()
            if "servers" in notification_json:
                notification.servers = notification_json["servers"]
            if "notification_free_type" in notification_json:
                for free_type in notification_json["notification_free_type"]:
                    notification.notification_free_type.append(GameFreeType[free_type])
            if "game_platforms" in notification_json:
                for game_platform in notification_json["game_platforms"]:
                    notification.game_platforms.append(GamePlatform[game_platform])
            if "title" in notification_json:
                notification.title = notification_json["title"]
            if "body" in notification_json:
                notification.body = notification_json["body"]
            config.notifications.append(notification)


def format_time(utc_date: datetime.datetime, offset: int, format_str: str):  # format time
    cst_date = utc_date + datetime.timedelta(hours=offset)
    return cst_date.strftime(format_str)


config = Config()

for notification in config.notifications:
    @receiver(game_platforms=notification.game_platforms, free_types=notification.notification_free_type)
    def notify(
            notify_plugin: str,
            game_platform: GamePlatform,
            game_name: str,
            game_id: str,
            game_url: str,
            free_type: GameFreeType,
            start_time: datetime.datetime,
            end_time: datetime.datetime,
            source_url: str,
            extra_info: str = None
    ):
        def format_str(s: str):
            return s.format(
                notify_plugin=notify_plugin,
                game_platform=game_platform.value,
                game_name=game_name,
                game_id=game_id,
                game_url=game_url,
                free_type=free_type.value,
                start_time=format_time(start_time, config.time_format.utc_offset, config.time_format.format_str),
                end_time=format_time(end_time, config.time_format.utc_offset, config.time_format.format_str),
                source_url=source_url,
                extra_info=extra_info
            )

        title = format_str(notification.title)
        body = format_str(notification.body)
        apprise_obj = apprise.Apprise()
        apprise_obj.add(notification.servers)
        apprise_obj.notify(title=title, body=body)


logger.info(center_format_text())
logger.info(center_format_text("Apprise Notifier"))
logger.info(center_format_text("Send notification to Apprise supported platforms"))
logger.info(center_format_text("Author: lupohan44"))
logger.info(center_format_text())

parse_config()
