from epicstore_api import EpicGamesStoreAPI, OfferData
from peewee import *
import datetime

from games_hub.api import *
from games_hub.logger import logger
from games_hub.message import *
from games_hub.utils import *

"""static variables"""
__name__ = "EpicGamesStore Scraper"
__package__ = "gameshub.official.scraper.epic"
__version__ = "1.0.2"
config_example_path = os.path.join(GAMESHUB_SRC_DIR, os.path.split(os.path.realpath(__file__))[0], "config.example.json5")
config_folder = os.path.join(GAMESHUB_CONFIG_DIR, 'plugins', __package__)
if not os.path.exists(config_folder):
    os.makedirs(config_folder, exist_ok=True)
record_path = os.path.join(config_folder, "record.db")
config_path = os.path.join(config_folder, "config.json5")
if not os.path.exists(config_path):
    shutil.copy(config_example_path, config_path)
"""static variables END"""
db = SqliteDatabase(record_path)


class GameRecord(Model):
    game_id = CharField()
    begin_time = DateTimeField()
    end_time = DateTimeField()

    class Meta:
        database = db


def save_game_records_to_db(games):
    if db.is_closed():
        db.connect()
    for game in games:
        game.save()


def get_game_record_from_db(game_id, begin_time: datetime.datetime = None, end_time: datetime.datetime = None):
    if db.is_closed():
        db.connect()
    game = GameRecord.select().where(GameRecord.game_id == game_id)
    if len(game) != 0:
        for g in game:
            if g.begin_time == begin_time and g.end_time == end_time:
                return g
    return None


class Config:
    def __init__(self):
        self.loop_delay = 3000


config = Config()


def parse_config():
    logger.info(PARSING_CONFIG_MSG % config_path)
    if not os.path.exists(config_path):
        raise Exception(CONFIG_NOT_EXIST_ERROR_MSG)
    config_json = load_json(config_path)
    if "loop_delay" in config_json:
        config.loop_delay = config_json["loop_delay"]


logger.info(center_format_text())
logger.info(center_format_text(__name__))
logger.info(center_format_text("Scrap epic games store free games"))
logger.info(center_format_text("Author: lupohan44"))
logger.info(center_format_text())

parse_config()
db.create_tables([GameRecord])


@timer(delay=config.loop_delay)
def scraper():
    try:
        logger.info("Getting free games from epic games store...")
        api = EpicGamesStoreAPI()
        free_games = api.get_free_games().get('data').get('Catalog').get('searchStore').get('elements')
        new_free_games_count = 0
        for free_game in free_games:
            if free_game['productSlug'] != '[]':
                games_free_type = GameFreeType.KEEP_FOREVER
                if free_game.get('expiryDate') is not None:
                    games_free_type = GameFreeType.LIMITED_TIME
                game_id = free_game['id'] + '@' + free_game['namespace']
                start_time = datetime.datetime.strptime(free_game.get('promotions').get('promotionalOffers')[0].
                                                        get('promotionalOffers')[0].get('startDate'),
                                                        '%Y-%m-%dT%H:%M:%S.%fZ')
                end_time = datetime.datetime.strptime(free_game.get('promotions').get('promotionalOffers')[0].
                                                      get('promotionalOffers')[0].get('endDate'),
                                                      '%Y-%m-%dT%H:%M:%S.%fZ')

                if get_game_record_from_db(game_id, start_time, end_time) is not None:
                    continue
                if free_game['productSlug'] is not None:
                    game_url = "https://store.epicgames.com/p/" + free_game['productSlug']
                else:
                    game_url = "https://store.epicgames.com/p/" + free_game.get('offerMappings')[0].get('pageSlug')
                notify(__name__, GamePlatform.EPIC, free_game['title'], free_game['id'] + '@' + free_game['namespace'],
                       game_url, games_free_type, start_time, end_time, game_url, None)
                new_free_games_count += 1
                save_game_records_to_db([GameRecord(game_id=game_id, begin_time=start_time, end_time=end_time)])
        logger.info("Got %d new free games from epic games store" % new_free_games_count)
    except Exception as e:
        logger.error(e)
