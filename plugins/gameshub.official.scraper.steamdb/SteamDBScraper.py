from urllib import request
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from peewee import *
from playwright.sync_api import *

from games_hub.api import *
from games_hub.logger import logger
from games_hub.message import *
from games_hub.utils import *

"""static variables"""
__name__ = "SteamDB Scraper"
__package__ = "gameshub.official.scraper.steamdb"
__version__ = "1.0.2"
config_example_path = os.path.join(GAMESHUB_SRC_DIR, os.path.split(os.path.realpath(__file__))[0], "config.example.json5")
config_folder = os.path.join(GAMESHUB_CONFIG_DIR, 'plugins', __package__)
if not os.path.exists(config_folder):
    os.makedirs(config_folder, exist_ok=True)
record_path = os.path.join(config_folder, "record.db")
config_path = os.path.join(config_folder, "config.json5")
log_folder = os.path.join(config_folder, "logs")
if not os.path.exists(config_path):
    shutil.copy(config_example_path, config_path)
STEAM_DB_FREE_GAMES_URL = "https://steamdb.info/upcoming/free/"
"""static variables END"""

http_header = dict({})
db = SqliteDatabase(record_path)


class GameRecord(Model):
    game_name = CharField()
    sub_id = CharField()  # IntegerField() might be better
    steam_url = CharField()
    start_time = DateTimeField(null=True)
    end_time = DateTimeField(null=True)

    class Meta:
        database = db


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


class LogSetting:
    def __init__(self):
        self.screenshotEnabled = False


class Config:
    def __init__(self):
        self.log_setting = LogSetting()
        self.browser = "webkit"
        self.headless = True
        self.first_delay = 15
        self.loop_delay = 3000


def get_url_single(url, headers=None, decode='utf-8'):
    if headers is not None:
        http_header.update(headers)
    req = request.Request(url, headers=http_header)
    response = request.urlopen(req)
    html = response.read().decode(decode)
    soup = BeautifulSoup(html, 'lxml')

    return soup


def playwright_get_url(url, delay=0, browser="webkit", headless=True):
    with sync_playwright() as p:
        browser = p[browser].launch(headless=headless)
        # browser = p.webkit.launch(headless=headless)
        try:
            page = browser.new_page()
            page.goto(url=url)
            if config.log_setting.screenshotEnabled:
                # Create log folder if not exists
                if not os.path.exists(log_folder):
                    os.makedirs(log_folder)
            delay_remaining = delay
            while delay_remaining > 0:
                time.sleep(3)
                if config.log_setting.screenshotEnabled:
                    page.screenshot(path=os.path.join(log_folder, ("screenshot-%s.png" %
                                                                   (time.strftime("%Y-%m-%d-%H-%M-%S",
                                                                                  time.localtime())))))
                delay_remaining = delay_remaining - 3
            html = page.inner_html("*")
        except:
            raise Exception(GET_PAGE_SOURCE_ERROR_MSG)
        finally:
            browser.close()

        return BeautifulSoup(html, 'lxml')


def process_steamdb_result(steamdb_result):
    game_records = list([])
    telegram_push_message = list([])
    asf_redeem_list = list([])

    # go through all the free games
    for each_tr in steamdb_result.select(".app"):
        if "hidden" in each_tr.attrs.keys():
            continue
        steamdb_url = "N/A"

        tds = each_tr.find_all("td")
        start_datetime = None
        end_datetime = None
        '''get basic info'''
        tds_length = len(tds)
        if len(tds[tds_length - 3].contents) == 1:
            free_type = tds[tds_length - 3].contents[0]
        else:
            free_type = tds[tds_length - 3].contents[2].contents[0] + "Forever"
        start_time_str = str(tds[tds_length - 2].get("data-time"))
        end_time_str = str(tds[tds_length - 1].get("data-time"))
        steamdb_url = urljoin(STEAM_DB_FREE_GAMES_URL, str(tds[tds_length - 5].contents[1].get("href")))

        if start_time_str != str(None):
            utc_format = "%Y-%m-%dT%H:%M:%S+00:00"
            start_datetime = datetime.datetime.strptime(start_time_str, utc_format)
        if end_time_str != str(None):
            utc_format = "%Y-%m-%dT%H:%M:%S+00:00"
            end_datetime = datetime.datetime.strptime(end_time_str, utc_format)

        game_name = str(tds[tds_length - 5].find("b").contents[0])
        sub_id = str(tds[tds_length - 5].contents[1].get('href').split('/')[2])
        # remove the url variables
        steam_url = str(tds[tds_length - 6].contents[1].get('href')).split("?")[0]
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
            free_type_enum = GameFreeType.KEEP_FOREVER
            if free_type.lower() == "Weekend".lower():
                free_type_enum = GameFreeType.LIMITED_TIME
            notify(__name__, GamePlatform.STEAM, game_name, sub_id, steam_url, free_type_enum, start_datetime,
                   end_datetime, steamdb_url, "!addlicense asf " + sub_id)
    # refresh the record
    if len(game_records) > 0:
        logger.info("Writing records...")
        save_game_records_to_db(game_records)
    else:
        logger.info("No records were written!")


config = Config()


def parse_config():
    logger.info(PARSING_CONFIG_MSG % config_path)
    if not os.path.exists(config_path):
        raise Exception(CONFIG_NOT_EXIST_ERROR_MSG)
    config_json = load_json(config_path)
    if "log" in config_json:
        if "screenshot" in config_json["log"]:
            config.log_setting.screenshotEnabled = config_json["log"]["screenshot"]
    if "browser" in config_json:
        config.browser = config_json["browser"]
    if "headless" in config_json:
        config.headless = config_json["headless"]
    if "first_delay" in config_json:
        config.first_delay = config_json["first_delay"]
    if "loop_delay" in config_json:
        config.loop_delay = config_json["loop_delay"]
    if "headers" in config_json:
        http_header.update(config_json["headers"])


logger.info(center_format_text())
logger.info(center_format_text("SteamDB Free Games Scraper"))
logger.info(center_format_text("Scrap free games from SteamDB"))
logger.info(center_format_text("Author: lupohan44"))
logger.info(center_format_text())

parse_config()
db.create_tables([GameRecord])


@timer(delay=config.loop_delay)
def scraper():
    try:
        logger.info("Loading steamdb page...")
        html = playwright_get_url(url=STEAM_DB_FREE_GAMES_URL, delay=config.first_delay, browser=config.browser,
                                  headless=config.headless)

        # start analysing page source
        logger.info("Start processing steamdb data...")
        process_steamdb_result(steamdb_result=html)
    except Exception as e:
        logger.error(e)
