import datetime
import threading
import time
from functools import wraps
import typing

import schedule
from typing import List

from games_hub.logger import logger
from games_hub.message import *
from games_hub.types import *

_receiver_list = []
_receiver_list_mutex = threading.Lock()
_notification_list = []
_notification_list_mutex = threading.Lock()
_schedule_list = []


def timer(
        delay: int = 3000
):
    """
    timer decorator, execute function every delay seconds

    example:
    @timer(delay=3000) # execute every 3000s
    """

    def decorator(
            func: typing.Callable
    ):
        @wraps(func)
        def wrapper():
            schedule.every(delay).seconds.do(func)
            _schedule_list.append(func)

        return wrapper()

    return decorator


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
    with _notification_list_mutex:
        _notification_list.append({
            "notify_plugin": notify_plugin,
            "game_platform": game_platform,
            "game_name": game_name,
            "game_id": game_id,
            "game_url": game_url,
            "free_type": free_type,
            "start_time": start_time,
            "end_time": end_time,
            "source_url": source_url,
            "extra_info": extra_info})


def receiver(
        game_platforms: typing.Optional[List[GamePlatform]] = None,
        free_types: typing.Optional[List[GameFreeType]] = None,
):
    """
    receiver decorator, receive desired game info

    example:
    @receiver() # receiver notification of all free types from game platforms information
    @receiver(game_platforms=[GamePlatform.STEAM]) # receiver notification of all free types from steam
    @receiver(free_types=[GameFreeType.FREE]) # receiver notification of free type from all game platforms
    """

    def decorator(
            func: typing.Callable
    ):
        @wraps(func)
        def wrapper():
            with _receiver_list_mutex:
                _receiver_list.append({
                    "handler": func,
                    "game_platforms": game_platforms,
                    "free_types": free_types
                })

        return wrapper()

    return decorator


def run_schedule_and_send_notification():
    for schedule_func in _schedule_list:
        schedule_func()
    while True:
        try:
            schedule.run_pending()
            send_notifications()
            time.sleep(1)
        except KeyboardInterrupt:
            logger.info(USER_INTERRUPT_EXIT_MSG)
            break


def send_notifications():
    notification = None
    with _notification_list_mutex:
        if len(_notification_list) == 0:
            return
        notification = _notification_list.pop()
    if notification is None:
        return

    def notify_receiver(func):
        try:
            func(notify_plugin=notification['notify_plugin'],
                 game_platform=notification['game_platform'],
                 game_name=notification['game_name'],
                 game_id=notification['game_id'],
                 game_url=notification['game_url'],
                 free_type=notification['free_type'],
                 start_time=notification['start_time'],
                 end_time=notification['end_time'],
                 source_url=notification['source_url'],
                 extra_info=notification['extra_info'])
        except Exception as e:
            logger.error(SEND_NOTIFICATION_ERROR_MSG, e)
    _receiver_list_copy = []
    with _receiver_list_mutex:
        _receiver_list_copy = _receiver_list.copy()
    for receiver_func in _receiver_list_copy:
        if receiver_func['game_platforms'] is None or len(receiver_func['game_platforms']) == 0:
            if receiver_func['free_types'] is None or len(receiver_func['free_types']) == 0:
                notify_receiver(receiver_func['handler'])
            else:
                for free_type in receiver_func['free_types']:
                    if notification['free_type'] == free_type:
                        notify_receiver(receiver_func['handler'])
        for game_platform in receiver_func['game_platforms']:
            if notification['game_platform'] == game_platform:
                if receiver_func['free_types'] is None or len(receiver_func['free_types']) == 0:
                    notify_receiver(receiver_func['handler'])
                else:
                    for free_type in receiver_func['free_types']:
                        if notification['free_type'] == free_type:
                            notify_receiver(receiver_func['handler'])
