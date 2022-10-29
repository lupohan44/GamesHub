import asyncio

from ASF import IPC
from peewee import *

from games_hub.api import *
from games_hub.logger import logger
from games_hub.message import *
from games_hub.utils import *

"""static variables"""
__name__ = "ASF Redeem"
__package__ = "gameshub.official.redeem.asf"
config_folder = os.path.split(os.path.realpath(__file__))[0]
record_path = os.path.join(config_folder, "record.db")
config_path = os.path.join(config_folder, "config.json5")
config_example_path = os.path.join(config_folder, "config.example.json5")
if not os.path.exists(config_path):
    config_folder = os.path.join('plugins', __package__)
    if not os.path.exists(config_folder):
        os.mkdir(config_folder)
    record_path = os.path.join(config_folder, "record.db")
    config_path = os.path.join(config_folder, "config.json5")
    shutil.copy(config_example_path, config_path)
"""static variables END"""

db = SqliteDatabase(record_path)


class GameRecord(Model):
    game_name = CharField()
    sub_id = CharField()  # IntegerField() might be better
    steam_url = CharField()
    start_time = DateTimeField()
    end_time = DateTimeField()

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
        if game.start_time < datetime.datetime.utcnow() + datetime.timedelta(minutes=60) \
                and game.end_time > datetime.datetime.utcnow():
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
        self.ipc = "http://127.0.0.1:1242"
        self.ipc_password = ""
        self.redeem_type: List[GameFreeType] = []
        self.redeem_command = "!addlicense asf {game_ids}"


def parse_config():
    logger.info(PARSING_CONFIG_MSG % config_path)
    if not os.path.exists(config_path):
        raise Exception(CONFIG_NOT_EXIST_ERROR_MSG)
    config_json = load_json(config_path)
    if "ipc" in config_json:
        config.ipc = config_json["ipc"]
    if "ipc_password" in config_json:
        config.ipc_password = config_json["ipc_password"]
    if "redeem_type" in config_json:
        for item in config_json["redeem_type"]:
            config.redeem_type.append(GameFreeType(item))
    if "redeem_command" in config_json:
        config.redeem_command = config_json["redeem_command"]


config = Config()


@receiver(game_platforms=[GamePlatform.STEAM], free_types=config.redeem_type)
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
    game_record = GameRecord(game_name=game_name, sub_id=game_id, steam_url=game_url,
                             start_time=start_time, end_time=end_time)
    save_game_records_to_db([game_record])


async def command(cmd):
    async with IPC(ipc=config.ipc, password=config.ipc_password) as asf:
        return await asf.Api.Command.post(body={
            'Command': cmd
        })


logger.info(center_format_text())
logger.info(center_format_text("ASF Redeem"))
logger.info(center_format_text("Redeem free steam games through ASF"))
logger.info(center_format_text("Author: lupohan44"))
logger.info(center_format_text())

parse_config()
db.create_tables([GameRecord])


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
        cmd = config.redeem_command.format(game_ids=",".join(games_id))
        asyncio.run(command(cmd))
        logger.info(REDEEM_GAME_SUCCESS_MSG % cmd)
        delete_game_record_from_db(games_id)
    except Exception as e:
        logger.error(e)
