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
   playwright install || python3 -m playwright install
   ```
3. Copy [config.example.json5](config.example.json5) to config.json5, change settings in it according to the comment.
4. Run
   ```shell
   python3 app.py
   ```

## Known issue
1. Playwright does not support CentOS. ([issue](https://github.com/microsoft/playwright/issues/6219))

## [Changelog](ChangeLog.md)