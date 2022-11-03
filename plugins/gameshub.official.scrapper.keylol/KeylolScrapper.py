import re
from urllib import request, parse

import requests
from bs4 import BeautifulSoup
from peewee import *

from games_hub.api import *
from games_hub.logger import logger
from games_hub.message import *
from games_hub.utils import *

"""static variables"""
__name__ = "Keylol Scrapper"
__package__ = "gameshub.official.scrapper.keylol"
__version__ = "1.0.0"
config_example_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], "config.example.json5")
config_folder = os.path.join('plugins', __package__)
if not os.path.exists(config_folder):
    os.makedirs(config_folder, exist_ok=True)
record_path = os.path.join(config_folder, "record.db")
config_path = os.path.join(config_folder, "config.json5")
if not os.path.exists(config_path):
    shutil.copy(config_example_path, config_path)
cookies_file_path = os.path.join(config_folder, "cookies.txt")
KEYLOL_FREE_GAMES_HUB_URL = "https://keylol.com/t572814-1-1"
KEYLOL_ACCOUNT_INFO_URL = "https://keylol.com/home.php?mod=spacecp"
KEYLOL_RATE_PLUGIN_URL = 'https://keylol.com/forum.php?mod=misc&action=rate&tid={}&pid={}&infloat=yes&handlekey=rate' \
                         '&t={}&inajax=1&ajaxtarget=fwin_content_rate'
KEYLOL_RATE_POST_URL = 'https://keylol.com/forum.php?mod=misc&action=rate&ratesubmit=yes&infloat=yes&inajax=1'
KEYLOL_PLATFORMS = {
    "亚马逊": GamePlatform.AMAZON,
    "GOG": GamePlatform.GOG,
    "Steam": GamePlatform.STEAM,
    "Epic": GamePlatform.EPIC,
    "Uplay": GamePlatform.UPLAY,
    "Origin": GamePlatform.ORIGIN,
    "Windows商店": GamePlatform.WINDOWS_STORE,
    "Humble商店": GamePlatform.HUMBLE_BUNDLE,
    "Bethesda": GamePlatform.BETHESDA,
}
"""static variables END"""

if not os.path.exists(cookies_file_path):
    with open(cookies_file_path, 'w') as f:
        f.write("")
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
        self.loop_delay = 3000


def get_url(url):
    cookies = ''
    headers = {}
    with open(cookies_file_path, 'r') as f_cookies:
        cookies = f_cookies.read()
    if cookies != '':
        headers['Cookie'] = cookies.replace('\n', '')
    req = request.Request(url, headers=headers)
    response = request.urlopen(req)
    html = response.read().decode('utf-8')
    soup = BeautifulSoup(html, 'lxml')
    return soup


def verify_cookies():
    soup = get_url(KEYLOL_ACCOUNT_INFO_URL)
    selector = '#profilelist'
    account_info = soup.select(selector)
    if len(account_info) == 0:
        return False
    username = account_info[0].find_all('td')
    if len(username) == 0:
        return False
    username = username[0].text
    if username != "":
        return True
    return False


def get_main_post_content(soup):
    post_list = soup.find_all('div', id='postlist')
    if len(post_list) == 0:
        return None
    main_post = post_list[0]
    main_post_content = main_post.find_all('td', class_='t_f')
    if len(main_post_content) == 0:
        return None
    main_post_content = main_post_content[0]
    return main_post_content


def get_post_id(soup, index):
    post_list = soup.find_all('div', id='postlist')
    if len(post_list) == 0:
        return None
    post_list = post_list[0]
    post_ids = []
    divs = post_list.find_all('div')
    for div in divs:
        if 'id' in div.attrs:
            # id begin with post_
            if div.attrs['id'].startswith('post_'):
                post_ids.append(div.attrs['id'][5:])
    if len(post_ids) > index:
        return post_ids[index]
    return None


def process_keylol_result(soup):
    main_post_content = get_main_post_content(soup)
    if main_post_content is None:
        return None
    game_platform = GamePlatform.OTHER
    for child in main_post_content.children:
        if child.name == 'h1' and child.get('class') is not None and child.get('class')[0] == 'KyloStylisedHeader0':
            platform_text = child.text
            if platform_text in KEYLOL_PLATFORMS:
                game_platform = KEYLOL_PLATFORMS[platform_text]
            else:
                game_platform = GamePlatform.OTHER
            continue
        if child.name == 'div' and child.get('class') is not None and child.get('class')[0] == 'quote':
            a_tags = child.find_all('a')
            for a_tag in a_tags:
                href = a_tag.get('href')
                if href is not None and 'keylol.com' in href:
                    process_keylol_free_game_information(href, game_platform)


def process_keylol_amazon_free_game_information(source_url, soup):
    a_tags = soup.find_all('a')
    amazon_urls = []
    for a_tag in a_tags:
        href = a_tag.get('href')
        if href is not None and 'gaming.amazon.com/loot' in href:
            amazon_urls.append(href)
    for amazon_url in amazon_urls:
        amazon_soup = get_url(amazon_url)
        # TODO: need a way to bypass amazon's anti-scraping mechanism


def say_thank_you(keylol_url):
    try:
        headers = {}
        with open(cookies_file_path, 'r') as f_cookies:
            cookies = f_cookies.read().replace('\n', '')
            headers['Cookie'] = cookies
        regex = re.compile(r't(\d+)')
        tid = regex.findall(keylol_url)[0]
        pid = get_post_id(get_url(keylol_url), 0)
        rate_url = KEYLOL_RATE_PLUGIN_URL.format(tid, pid, int(time.time()))
        soup = get_url(rate_url)
        referer = soup.find_all('input', attrs={'name': 'referer'})
        if len(referer) == 0:
            return
        referer = referer[0].get('value')
        form_hash = soup.find_all('input', attrs={'name': 'formhash'})
        if len(form_hash) == 0:
            return
        form_hash = form_hash[0].get('value')
        data = {
            'formhash': form_hash,
            'tid': tid,
            'pid': pid,
            'referer': referer,
            'handlekey': 'rate',
            'score1': '+1',
            'reason': '谢谢分享 (来自GamesHub)'
        }
        req = request.Request(KEYLOL_RATE_POST_URL,
                              data=parse.urlencode(data).encode('utf-8'), headers=headers)
        request.urlopen(req)
    except Exception as e:
        logger.error('Failed to say thank you to {}'.format(keylol_url))
        logger.error(e)


def process_keylol_steam_free_game_information(source_url, soup):
    say_thank_you(source_url)
    if get_game_record_from_db(source_url) is not None:
        return
    a_tags = soup.find_all('a')
    steam_urls = []
    for a_tag in a_tags:
        href = a_tag.get('href')
        if href is not None and 'store.steampowered.com/app' in href:
            steam_urls.append(href)
    app_ids = []
    for steam_url in steam_urls:
        app_id = steam_url.split('/')[4]
        if app_id not in app_ids:
            app_ids.append(app_id)
    # if the game type is dlc, sometimes thread author will provide game url as well
    final_app_info = {}
    for app_id in app_ids:
        response = requests.get('https://store.steampowered.com/api/appdetails?appids=' + app_id)
        response_json = response.json()
        if app_id in response_json and 'success' in response_json[app_id] and response_json[app_id]['success']:
            data = response_json[app_id]['data']
            if not data['is_free']:
                continue
            if 'type' in data and data['type'] == 'game':
                final_app_info = {
                    'type': 'game',
                    'app_id': app_id,
                    'name': data['name'],
                    'url': 'https://store.steampowered.com/app/' + app_id,
                }
            elif 'type' in data and data['type'] == 'dlc':
                final_app_info = {
                    'type': 'dlc',
                    'app_id': app_id,
                    'name': data['name'],
                    'url': 'https://store.steampowered.com/app/' + app_id,
                }
                break
    if len(final_app_info) == 0:
        return
    notify(__name__, GamePlatform.STEAM, final_app_info['name'], final_app_info['app_id'],
           "https://store.steampowered.com/app/" + final_app_info['app_id'], GameFreeType.KEEP_FOREVER,
           None, None, source_url, "!addlicense asf " + final_app_info['app_id'])
    save_game_records_to_db([GameRecord(game_id=final_app_info['app_id'], source_url=source_url)])


def process_keylol_free_game_information(url, game_platform: GamePlatform):
    soup = get_url(url)
    main_post_content = get_main_post_content(soup)
    if game_platform == GamePlatform.AMAZON:
        process_keylol_amazon_free_game_information(url, main_post_content)
    elif game_platform == GamePlatform.STEAM:
        process_keylol_steam_free_game_information(url, main_post_content)


config = Config()


def parse_config():
    logger.info(PARSING_CONFIG_MSG % config_path)
    if not os.path.exists(config_path):
        raise Exception(CONFIG_NOT_EXIST_ERROR_MSG)
    config_json = load_json(config_path)
    if "loop_delay" in config_json:
        config.loop_delay = config_json["loop_delay"]


logger.info(center_format_text())
logger.info(center_format_text("Keylol Free Games Scraper"))
logger.info(center_format_text("Scrap free games from Keylol"))
logger.info(center_format_text("https://keylol.com/"))
logger.info(center_format_text("Author: lupohan44"))
logger.info(center_format_text())

parse_config()
db.create_tables([GameRecord])
if not verify_cookies():
    logger.error("Cookies verification failed, please check your cookies in file cookies.txt")
    raise Exception("Cookies are invalid")


@timer(delay=config.loop_delay)
def scrapper():
    try:
        logger.info("Loading keylol page...")
        soup = get_url(url=KEYLOL_FREE_GAMES_HUB_URL)
        logger.info("Processing keylol page...")
        process_keylol_result(soup)
    except Exception as e:
        logger.error(e)
