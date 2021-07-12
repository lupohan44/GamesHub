# SteamDBFreeGamesClaimer

This project is inspired by [SteamDB-FreeGames](https://github.com/azhuge233/SteamDB-FreeGames)

**Seems that SteamDB really don't want people scraping their site.**

## Features
:white_check_mark: Gather Steam free games from [SteamDB](https://steamdb.info/upcoming/free/).

:white_check_mark: Use telegram bot to send free games information. [(channel)](https://t.me/SteamFreeGameNotify)

:white_check_mark: Use ASF to redeem games
## Requirements

- python3
  - playwright
  - bs4(lxml)
  - python-telegram-bot

## Usage
1. Clone repository
   ```shell
   git clone https://github.com/lupohan44/SteamDBFreeGamesClaimer.git
   ```
2. Install requirements
   ```shell
   pip3 install -r requirements.txt
   playwright install
   ```
3. Copy [config.example.json5](config.example.json5) to config.json5, change settings in it according to the comment.
4. Run
   ```shell
   python3 app.py
   ```

## Known issue
1. Playwright does not support CentOS. ([issue](https://github.com/microsoft/playwright/issues/6219))

## Changelog
### 2021/7/12-2
1. Fix wrong requirements "telegram"
2. Support json5 (#2)
3. Change README.md

**Notice**: This upgrade change config.json to config.json5 and change record.json to record.json5

Run
```shell
pip3 uninstall telegram
```
should remove the wrong requirements
### 2021/7/12
1. Fix wrong requirements
2. Change loop delay default value to 600 seconds
3. Support MarkDown format in telegram notification
4. Support multiple chat_id in telegram
5. Change README.md

**Notice**: This upgrade change config.json
### 2021/7/11
1. Initial release