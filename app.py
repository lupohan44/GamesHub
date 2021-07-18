import asyncio
import datetime
import os
import selectors
import time
from urllib import request

from telegram.ext import Updater
import json5
from ASF import IPC
from bs4 import BeautifulSoup
from packaging import version
from playwright.sync_api import sync_playwright
from peewee import *
from static import *

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

db = SqliteDatabase(RECORD_PATH)
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
        self.loop_delay = 3000
        self.time_format = TimeFormat()
        self.telegram = Telegram()
        self.asf = ASF()


class GameRecord(Model):
    game_name = CharField()
    sub_id = CharField()  # IntegerField() might be better
    steam_url = CharField()
    start_time = TimeField()
    end_time = TimeField()

    class Meta:
        database = db


config = Config()


def save_game_records_to_db(games):
    if db.is_closed():
        db.connect()
    for game in games:
        game.save()


def get_game_record_from_db(game_name, start_time, end_time):
    if db.is_closed():
        db.connect()
    game = GameRecord.select().where(GameRecord.game_name == game_name and GameRecord.start_time == start_time
                                     and GameRecord.end_time == end_time)
    if len(game) != 0:
        return game
    return None


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
    return utc_date, cst_date.strftime(config.time_format.format_str)


async def command(cmd):
    async with IPC(ipc=config.asf.ipc, password=config.asf.password) as asf:
        return await asf.Api.Command.post(body={
            'Command': cmd
        })


def process_steamdb_result(steamdb_result):
    game_records = list([])
    telegram_push_message = list([])
    asf_redeem_list = list([])

    # go through all the free games
    for each_tr in steamdb_result.select(".app"):
        if "hidden" in each_tr.attrs.keys():
            continue

        tds = each_tr.find_all("td")
        start_datetime = datetime.datetime(year=2020, month=1, day=1)
        end_datetime = datetime.datetime(year=2020, month=1, day=1)
        '''get basic info'''
        if len(tds) == 5:  # steamdb add a install button in table column
            free_type = tds[2].contents[0]
            start_time_str = str(tds[3].get("data-time"))
            end_time_str = str(tds[4].get("data-time"))
        else:
            if len(tds[3].contents) == 1:
                free_type = tds[3].contents[0]
            else:
                free_type = tds[3].contents[2].contents[0] + "Forever"
            start_time_str = str(tds[4].get("data-time"))
            end_time_str = str(tds[5].get("data-time"))

        if start_time_str == str(None):
            start_time_str = "N/A"
        else:
            start_datetime, start_time_str = format_time(start_time_str)
        if end_time_str == str(None):
            end_time_str = "N/A"
        else:
            end_datetime, end_time_str = format_time(end_time_str)

        game_name = str(tds[1].find("b").contents[0])
        sub_id = str(tds[1].contents[1].get('href').split('/')[2])
        # remove the url variables
        steam_url = str(tds[0].contents[1].get('href')).split("?")[0]
        '''get basic info end'''

        logger.info("Found free game: " + game_name)
        # record information

        '''new free games notify'''
        # check if this game exists in previous records
        if get_game_record_from_db(game_name, start_datetime, end_datetime) is None:
            game_records.append(GameRecord(game_name=game_name, sub_id=sub_id, steam_url=steam_url,
                                           start_time=start_datetime, end_time=end_datetime))
            # new free game
            '''get game details'''
            # try to get game's name on Steam store page
            steam_soup = get_url_single(url=steam_url)
            name = steam_soup.select(".apphub_AppName")
            if len(name) > 0:
                game_name = steam_soup.select(".apphub_AppName")[0].contents[0]
            '''get game details end'''

            notification_str = config.telegram. \
                notification_message.format(game=game_name, sub_id=sub_id, steam_url=steam_url,
                                            start_time=start_time_str, end_time=end_time_str,
                                            free_type=free_type)
            if ("ALL" in config.telegram.notification_free_type) or (
                    free_type in config.telegram.notification_free_type):
                telegram_push_message.append(notification_str)
        # always redeem free games
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
    if len(game_records) > 0:
        logger.info("Writing records...")
        save_game_records_to_db(game_records)
    else:
        logger.info("No records were written!")


def parse_config():
    logger.info("parsing %s" % CONFIG_PATH)
    if not os.path.exists(CONFIG_PATH):
        raise Exception(CONFIG_NOT_EXIST_ERROR_MSG)

    config_json = load_json(CONFIG_PATH)
    if "loop" in config_json:
        config.loop = config_json["loop"]
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


def check_update():
    logger.info("Checking for update...")
    local_version = VERSION
    try:
        github_version = {"VERSION": ""}
        req = request.Request(GITHUB_VERSION_URL)
        response = request.urlopen(req)
        github_version_py = response.read().decode('utf-8')
        exec(github_version_py, github_version)
        if version.parse(local_version) < version.parse(github_version["VERSION"]):
            logger.warning(FOUND_NEW_VERSION_WARNING_MSG % github_version["VERSION"])
            logger.warning(GITHUB_URL)
        else:
            logger.info(NO_NEW_VERSION_MSG)
    except:
        logger.warning(CANNOT_CHECK_UPDATE_WARNING_MSG)


def main():
    logger.info("#####################################################################################")
    logger.info("################################# SteamDBFreeGamesClaimer ###########################")
    logger.info("#################################### Author: lupohan44 ##############################")
    logger.info("###################################### Version: %s ###############################" % VERSION)
    logger.info("#####################################################################################")
    check_update()
    db.create_tables([GameRecord])
    while config.loop:
        parse_config()
        if (not config.telegram.enable) and (not config.asf.enable):
            raise Exception(AT_LEAST_ENABLE_ONE_FUNCTION_ERROR_MSG)

        logger.info("Loading steamdb page...")
        html = playwright_get_url(url=STEAM_DB_FREE_GAMES_URL, delay=FIRST_DELAY, headless=True)

        # start analysing page source
        logger.info("Start processing steamdb data...")
        process_steamdb_result(steamdb_result=html)
        if config.loop:
            logger.info("Sleep %s seconds till next loop..." % config.loop_delay)
            time.sleep(config.loop_delay)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(e)
        exit(1)
