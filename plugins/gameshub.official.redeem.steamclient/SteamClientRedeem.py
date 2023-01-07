from steam.client import SteamClient
from steam.guard import *
from peewee import *

from games_hub.api import *
from games_hub.logger import logger
from games_hub.message import *
from games_hub.utils import *

"""static variables"""
__name__ = "SteamClient Redeem"
__package__ = "gameshub.official.redeem.steamclient"
__version__ = "1.0.0"
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


def get_available_game_record_from_db():
    if db.is_closed():
        db.connect()
    games = GameRecord.select()
    correct_games = []
    for game in games:
        if (game.start_time is None or game.start_time < datetime.datetime.utcnow() + datetime.timedelta(minutes=60)) \
                and (game.end_time is None or game.end_time > datetime.datetime.utcnow()):
            correct_games.append(game)
    if len(correct_games) != 0:
        return correct_games
    return None


def delete_game_record_from_db(game_ids):
    if db.is_closed():
        db.connect()
    for game_id in game_ids:
        GameRecord.delete().where(GameRecord.sub_id == game_id).execute()


class Config:
    def __init__(self):
        self.accounts = []
        self.redeem_type: List[GameFreeType] = []


def parse_config():
    logger.info(PARSING_CONFIG_MSG % config_path)
    if not os.path.exists(config_path):
        raise Exception(CONFIG_NOT_EXIST_ERROR_MSG)
    config_json = load_json(config_path)
    if "accounts" in config_json:
        config.accounts = config_json["accounts"]
    if "redeem_type" in config_json:
        for item in config_json["redeem_type"]:
            config.redeem_type.append(GameFreeType(item))


config = Config()


@receiver(game_platforms=[GamePlatform.STEAM], free_types=config.redeem_type)
def notify(
        notify_plugin: str,
        game_platform: GamePlatform,
        game_name: str,
        game_id: str,
        game_url: str,
        free_type: GameFreeType,
        start_time: typing.Optional[datetime.datetime],
        end_time: typing.Optional[datetime.datetime],
        source_url: str,
        extra_info: str = None
):
    game_record = GameRecord(game_name=game_name, sub_id=game_id, steam_url=game_url,
                             start_time=start_time, end_time=end_time)
    save_game_records_to_db([game_record])


logger.info(center_format_text())
logger.info(center_format_text(__name__))
logger.info(center_format_text("Redeem free steam games through SteamClient"))
logger.info(center_format_text("Author: lupohan44"))
logger.info(center_format_text())

parse_config()
db.create_tables([GameRecord])
steam_clients = []
for account in config.accounts:
    client = SteamClient()
    steam_authenticator = None
    if 'secrets' in account:
        steam_authenticator = SteamAuthenticator(account['secrets'])
    if steam_authenticator:
        logger.info("Logging in steam account %s with SteamGuard code" % account['username'])
        if client.login(account['username'], account['password'], two_factor_code=steam_authenticator.get_code()) != 1:
            raise Exception("Failed to login to Steam with 2fa code")
    else:
        logger.info("Logging in steam account %s" % account['username'])
        if client.cli_login(username=account['username'], password=account['password']) != 1:
            raise Exception("Failed to login to Steam with username and password")
    logger.info("Login to steam account %s successfully" % account['username'])
    steam_clients.append(client)
if len(steam_clients) == 0:
    raise Exception("No steam account configured")


@timer(60)
def redeem_games():
    try:
        games = get_available_game_record_from_db()
        if games is None:
            return
        games_id = []
        for game in games:
            games_id.append(game.sub_id)
            logger.info(REDEEM_GAME_MSG % (game.game_name, game.sub_id))
        for steam_client in steam_clients:
            steam_client.request_free_license(games_id)
        delete_game_record_from_db(games_id)
    except Exception as e:
        logger.error(e)
