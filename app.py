import asyncio
import datetime
import logging
import os
import selectors
import time
from urllib import request

from telegram.ext import Updater
import json5
from ASF import IPC
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

'''Static Variables'''
STEAM_DB_FREE_GAMES_URL = "https://steamdb.info/upcoming/free/"
CONFIG_PATH = "config.json5"
RECORD_PATH = "record.json5"
FIRST_DELAY = 15
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

'''Global Variables'''
# the root logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# file Log
f_handler = logging.FileHandler("log.txt", encoding='utf-8')
f_handler.setLevel(logging.DEBUG)
f_handler.setFormatter(LOG_FORMAT)

# console Log
s_handler = logging.StreamHandler()
s_handler.setLevel(logging.INFO)
s_handler.setFormatter(LOG_FORMAT_WITHOUT_LEVEL_NAME)

# add handler to logger
logger.addHandler(f_handler)
logger.addHandler(s_handler)
logger.name = "SteamDBFreeGamesClaimer"

HTTP_HEADER = dict({})
'''Global Variables END'''


# class define
class TimeFormat:
    def __init__(self):
        self.utc_offset = 0
        self.format_str = "%Y/%m/%d %H:%M"


class Telegram:
    def __init__(self):
        self.enable = False
        self.token = ""
        self.chat_id_list = []
        self.markdown = False
        self.notification_message = "<b>{game}</b>\nSub ID: <i>{sub_id}</i>\nlink: <a href=\"{steam_url}\" >{" \
                                    "game}</a>\nfree type: {free_type}\nstart time: {start_time}\nend time: {" \
                                    "end_time}\n!addlicense asf {sub_id} "
        self.notification_free_type = []
        self.delay = 1


class ASF:
    def __init__(self):
        self.enable = False
        self.ipc = ""
        self.password = ""
        self.redeem_type_blacklist = []


class Config:
    def __init__(self):
        self.loop = True
        self.loop_delay = 600
        self.time_format = TimeFormat()
        self.telegram = Telegram()
        self.asf = ASF()


config = Config()


def load_json(path, method="r", init_str="{}"):
    if not os.path.exists(path):
        with open(path, "w", encoding='utf-8') as f:
            f.write(init_str)
    with open(path, method, encoding='utf-8') as f:
        data = json5.load(f)
    return data


def write_json(path, data, method="w"):
    with open(path, method, encoding='utf-8') as f:
        json5.dump(data, f, indent=4)


def get_url_single(url, headers=None, decode='utf-8'):
    if headers is not None:
        HTTP_HEADER.update(headers)
    req = request.Request(url, headers=HTTP_HEADER)
    if "https" in url:
        response = request.urlopen(req)
    else:
        response = request.urlopen(req)
    html = response.read().decode(decode)
    soup = BeautifulSoup(html, 'lxml')

    return soup


def playwright_get_url(url, delay=0, headless=True):
    with sync_playwright() as p:
        browser = p.webkit.launch(headless=headless)
        try:
            page = browser.new_page()
            page.goto(url=url)
            if delay != 0:
                time.sleep(delay)
            html = page.inner_html("*")
        except:
            raise Exception(GET_PAGE_SOURCE_ERROR_MSG)
        finally:
            browser.close()

        return BeautifulSoup(html, 'lxml')


def send_telegram_notification(msg_list):  # use telegram bot to send message
    if len(msg_list) != 0:
        try:
            tb = Updater(config.telegram.token)
            for msg in msg_list:
                for chat_id in config.telegram.chat_id_list:
                    tb.bot.send_message(chat_id=chat_id, text=msg,
                                        parse_mode="Markdown" if config.telegram.markdown else "HTML")
                    time.sleep(config.telegram.delay)
        except Exception as ex:
            logger.error("Send message error!")
            raise ex


def record(path, data):  # write data to json file
    if len(data) != 0:
        write_json(path=path, data=data)


def format_time(utc):  # format time
    utc_format = "%Y-%m-%dT%H:%M:%S+00:00"
    utc_date = datetime.datetime.strptime(utc, utc_format)
    cst_date = utc_date + datetime.timedelta(hours=config.time_format.utc_offset)
    return cst_date.strftime(config.time_format.format_str)


async def command(cmd):
    async with IPC(ipc=config.asf.ipc, password=config.asf.password) as asf:
        return await asf.Api.Command.post(body={
            'Command': cmd
        })


def process_steamdb_result(previous, steamdb_result):
    result = list([])
    telegram_push_message = list([])
    asf_redeem_list = list([])

    # go through all the free games
    for each_tr in steamdb_result.select(".app"):
        if "hidden" in each_tr.attrs.keys():
            continue

        tds = each_tr.find_all("td")
        td_len = len(tds)

        '''get basic info'''
        if td_len == 5:  # steamdb add a install button in table column
            free_type = tds[2].contents[0]
            start_time = str(tds[3].get("data-time"))
            end_time = str(tds[4].get("data-time"))
        else:
            if len(tds[3].contents) == 1:
                free_type = tds[3].contents[0]
            else:
                free_type = tds[3].contents[2].contents[0] + "Forever"
            start_time = str(tds[4].get("data-time"))
            end_time = str(tds[5].get("data-time"))

        if start_time == str(None):
            start_time = "None"
        else:
            start_time = format_time(start_time)
        if end_time == str(None):
            end_time = "None"
        else:
            end_time = format_time(end_time)

        game_name = str(tds[1].find("b").contents[0])
        sub_id = str(tds[1].contents[1].get('href').split('/')[2])
        # remove the url variables
        steam_url = str(tds[0].contents[1].get('href')).split("?")[0]
        '''get basic info end'''

        logger.info("Found free game: " + game_name)
        # record information
        d = dict({})
        d["Name"] = game_name
        d["ID"] = sub_id
        d["URL"] = steam_url
        d["Start_time"] = start_time
        d["End_time"] = end_time
        result.append(d)

        '''new free games notify'''
        # check if this game exists in previous records
        is_new_game = True
        for each in previous:
            if sub_id == each["ID"] and start_time == each["Start_time"]:
                is_new_game = False
                break

        if is_new_game:
            '''get game details'''
            # try to get game's name on Steam store page
            steam_soup = get_url_single(url=steam_url)
            name = steam_soup.select(".apphub_AppName")
            if len(name) > 0:
                game_name = steam_soup.select(".apphub_AppName")[0].contents[0]
            '''get game details end'''

            notification_str = config.telegram. \
                notification_message.format(game=game_name, sub_id=sub_id, steam_url=steam_url,
                                            start_time=start_time, end_time=end_time,
                                            free_type=free_type)
            if ("ALL" in config.telegram.notification_free_type) or (
                    free_type in config.telegram.notification_free_type):
                telegram_push_message.append(notification_str)
            if free_type not in config.asf.redeem_type_blacklist:
                asf_redeem_list.append(sub_id)

    # do the telegram notify job
    if config.telegram.enable:
        send_telegram_notification(telegram_push_message)
    # redeem in ASF
    if config.asf.enable:
        sub_ids_str = ','.join(asf_redeem_list)
        try:
            selector = selectors.SelectSelector()
            loop = asyncio.SelectorEventLoop(selector)
            loop.run_until_complete(command("!addlicense asf %s" % sub_ids_str))
        finally:
            loop.close()

    # refresh the record
    if len(result) > 0:
        logger.info("Writing records...")
        record(RECORD_PATH, result)
    else:
        logger.info("No records were written!")


def parse_config():
    logger.info("parsing %s" % CONFIG_PATH)
    if not os.path.exists(CONFIG_PATH):
        raise Exception(CONFIG_NOT_EXIST_ERROR_MSG)

    config_json = load_json(CONFIG_PATH)
    if "loop" in config_json and config_json["loop"]:
        config.loop = True
    if "loop_delay" in config_json:
        config.loop_delay = config_json["loop_delay"]

    if "headers" in config_json:
        HTTP_HEADER.update(config_json["headers"])
    if "time_format" in config_json:
        if "format_str" in config_json["time_format"]:
            config.time_format.format_str = config_json["time_format"]["format_str"]
        if "utc_offset" in config_json["time_format"]:
            config.time_format.utc_offset = config_json["time_format"]["utc_offset"]
    if "telegram" in config_json:
        config.telegram.enable = True
        if "token" not in config_json["telegram"]:
            raise Exception(TELEGRAM_REQUIRE_TOKEN_ERROR_MSG)
        if "chat_id" not in config_json["telegram"]:
            raise Exception(TELEGRAM_REQUIRE_CHAT_ID_ERROR_MSG)
        if type(config_json["telegram"]["chat_id"]) != list:
            raise Exception(CONFIG_FILE_NEEDS_TO_BE_UPDATED)
        config.telegram.token = config_json["telegram"]["token"]
        config.telegram.chat_id_list = config_json["telegram"]["chat_id"]
        if "format" in config_json["telegram"]:
            if "markdown" in config_json["telegram"]["format"]:
                config.telegram.markdown = config_json["telegram"]["format"]["markdown"]
            if "message" in config_json["telegram"]["format"]:
                config.telegram.notification_message = config_json["telegram"]["format"]["message"]
        if "notification_free_type" in config_json["telegram"]:
            config.telegram.notification_free_type = config_json["telegram"]["notification_free_type"]
        if "delay" in config_json["telegram"]:
            config.telegram.delay = config_json["telegram"]["delay"]
    if "asf" in config_json:
        config.asf.enable = True
        if "ipc" not in config_json["asf"]:
            raise Exception(ASF_REQUIRE_IPC_ERROR_MSG)
        config.asf.ipc = config_json["asf"]["ipc"]
        if "ipc_password" in config_json["asf"]:
            config.asf.password = config_json["asf"]["ipc_password"]
        if "redeem_type_blacklist" in config_json["asf"]:
            config.asf.redeem_type_blacklist = config_json["asf"]["redeem_type_blacklist"]


def main():
    logger.info("------------------- Start job -------------------")
    while config.loop:
        parse_config()
        if (not config.telegram.enable) and (not config.asf.enable):
            raise Exception(AT_LEAST_ENABLE_ONE_FUNCTION_ERROR_MSG)

        logger.info("Loading previous records...")
        previous = load_json(path=RECORD_PATH, init_str="[]")

        logger.info("Loading steamdb page...")
        html = playwright_get_url(url=STEAM_DB_FREE_GAMES_URL, delay=FIRST_DELAY, headless=True)

        # start analysing page source
        logger.info("Start processing steamdb data...")
        process_steamdb_result(previous=previous, steamdb_result=html)
        if config.loop:
            time.sleep(config.loop_delay)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(e)
        exit(1)
