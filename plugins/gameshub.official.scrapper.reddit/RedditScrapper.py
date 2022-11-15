from urllib import request
from urllib.parse import urljoin
import praw
import requests

from peewee import *

from games_hub.api import *
from games_hub.logger import logger
from games_hub.message import *
from games_hub.utils import *

"""static variables"""
__name__ = "Reddit Scrapper"
__package__ = "gameshub.official.scrapper.reddit"
__version__ = "1.0.0"
config_example_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], "config.example.json5")
config_folder = os.path.join('plugins', __package__)
if not os.path.exists(config_folder):
    os.makedirs(config_folder, exist_ok=True)
record_path = os.path.join(config_folder, "record.db")
config_path = os.path.join(config_folder, "config.json5")
if not os.path.exists(config_path):
    shutil.copy(config_example_path, config_path)
SUBREDDIT_NAME = "freegames"
"""static variables END"""
db = SqliteDatabase(record_path)


class GameRecord(Model):
    game_id = CharField()
    source_url = CharField()

    class Meta:
        database = db


def save_game_records_to_db(games):
    if db.is_closed():
        db.connect()
    for game in games:
        game.save()


def get_game_record_from_db(source_url):
    if db.is_closed():
        db.connect()
    game = GameRecord.select().where(GameRecord.source_url == source_url)
    if len(game) != 0:
        return game
    return None


class Config:
    def __init__(self):
        self.client_id = ""
        self.client_secret = ""
        self.loop_delay = 3000


def process_free_game_information(game_url, source_url):
    if get_game_record_from_db(source_url) is not None:
        return
    if not game_url.startswith("https://store.steampowered.com/app/"):
        return
    app_id = game_url.split('/')[4]
    response = requests.get('https://store.steampowered.com/api/appdetails?appids=' + app_id)
    response_json = response.json()
    if app_id in response_json and 'success' in response_json[app_id] and response_json[app_id]['success']:
        data = response_json[app_id]['data']
        if not data['is_free']:
            return
        notify(__name__, GamePlatform.STEAM, data['name'], app_id,
               "https://store.steampowered.com/app/" + app_id, GameFreeType.KEEP_FOREVER,
               None, None, source_url, "!addlicense asf " + app_id)
        save_game_records_to_db([GameRecord(game_id=app_id, source_url=source_url)])


config = Config()


def parse_config():
    logger.info(PARSING_CONFIG_MSG % config_path)
    if not os.path.exists(config_path):
        raise Exception(CONFIG_NOT_EXIST_ERROR_MSG)
    config_json = load_json(config_path)
    if "client_id" in config_json:
        config.client_id = config_json["client_id"]
    if "client_secret" in config_json:
        config.client_secret = config_json["client_secret"]
    if "loop_delay" in config_json:
        config.loop_delay = config_json["loop_delay"]


logger.info(center_format_text())
logger.info(center_format_text(__name__))
logger.info(center_format_text("Scrap free games from Reddit"))
logger.info(center_format_text("https://www.reddit.com/r/freegames"))
logger.info(center_format_text("Author: lupohan44"))
logger.info(center_format_text())

parse_config()
db.create_tables([GameRecord])
reddit = praw.Reddit(
    client_id=config.client_id,
    client_secret=config.client_secret,
    user_agent='GamesHub'
)


@timer(delay=config.loop_delay)
def scrapper():
    try:
        subreddit = reddit.subreddit(SUBREDDIT_NAME)
        for submission in subreddit.new(limit=20):
            game_url = submission.url
            source_url = urljoin('https://www.reddit.com', submission.permalink)
            process_free_game_information(game_url, source_url)
    except Exception as e:
        logger.error(e)
