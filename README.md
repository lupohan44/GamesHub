# SteamDBFreeGamesClaimer

[![project](https://img.shields.io/badge/lupohan44-SteamDBFreeGamesClaimer-brightgreen)](https://github.com/lupohan44/SteamDBFreeGamesClaimer) [![GitHub license](https://img.shields.io/github/license/lupohan44/SteamDBFreeGamesClaimer)](https://github.com/lupohan44/SteamDBFreeGamesClaimer/blob/main/LICENSE) [![GitHub stars](https://img.shields.io/github/stars/lupohan44/SteamDBFreeGamesClaimer)](https://github.com/lupohan44/SteamDBFreeGamesClaimer/stargazers)

[![docker](https://img.shields.io/badge/Docker-lupohan44%2Fsteamdb__free__games__claimer-blue?logo=docker)](https://hub.docker.com/r/lupohan44/steamdb_free_games_claimer) [![Build Status](https://api.travis-ci.com/lupohan44/SteamDBFreeGamesClaimer.svg)](https://travis-ci.com/github/lupohan44/SteamDBFreeGamesClaimer)

This project is inspired by [SteamDB-FreeGames](https://github.com/azhuge233/SteamDB-FreeGames)

**Seems that SteamDB really don't want people scraping their site.**

## Features
:white_check_mark: Gather Steam free games from [SteamDB](https://steamdb.info/upcoming/free/).

:white_check_mark: Use telegram bot to send free games information. [(channel)](https://t.me/SteamFreeGameNotify)

:white_check_mark: Use ASF to redeem games
## Requirements

- python3
  - [requirements.txt](requirements.txt)

## Usage
### Direct run
1. Clone repository
   ```shell
   git clone https://github.com/lupohan44/SteamDBFreeGamesClaimer.git
   ```
2. Go into SteamDBFreeGamesClaimer directory
   ```shell
   cd SteamDBFreeGamesClaimer
   ```
3. Install requirements
   ```shell
   pip3 install -r requirements.txt
   playwright install webkit || python3 -m playwright install webkit
   ```
4. Copy [config.example.json5](config.example.json5) to config.json5, change settings in it according to the comment.
5. Run
   ```shell
   python3 app.py
   ```
### Docker (For Linux only)
1. Create a folder for record and config, let's say folder name is /var/SteamDBFreeGamesClaimer

   _Please note that this folder name must be absolute path._
      ```shell
      export STEAM_DB_FOLDER_NAME=/var/SteamDBFreeGamesClaimer
      mkdir -p "$STEAM_DB_FOLDER_NAME"
      ```
2. Download [config.example.json5](config.example.json5) and rename to config.json5 into the folder created in step 1, change settings in it according to the comment.
   ```shell
   wget -c "https://raw.githubusercontent.com/lupohan44/SteamDBFreeGamesClaimer/main/config.example.json5" -O "$STEAM_DB_FOLDER_NAME/config.json5" || curl -o "$STEAM_DB_FOLDER_NAME/config.json5" "https://raw.githubusercontent.com/lupohan44/SteamDBFreeGamesClaimer/main/config.example.json5"
   ```
3. Run with docker
   ```shell
   docker pull lupohan44/steamdb_free_games_claimer:latest && docker run -v $STEAM_DB_FOLDER_NAME:/home/wd --rm lupohan44/steamdb_free_games_claimer:latest
   ```
   All changes by script inside docker will be permanently save to this folder.

## Known issue
1. Playwright does not support CentOS. ([issue](https://github.com/microsoft/playwright/issues/6219))
    - Use docker

## Support me
Star would be great! :)

## [Changelog](ChangeLog.md)