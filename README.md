# SteamDBFreeGamesClaimer

[![project](https://img.shields.io/badge/lupohan44-SteamDBFreeGamesClaimer-brightgreen)](https://github.com/lupohan44/SteamDBFreeGamesClaimer) [![GitHub license](https://img.shields.io/github/license/lupohan44/SteamDBFreeGamesClaimer)](https://github.com/lupohan44/SteamDBFreeGamesClaimer/blob/main/LICENSE) [![GitHub stars](https://img.shields.io/github/stars/lupohan44/SteamDBFreeGamesClaimer)](https://github.com/lupohan44/SteamDBFreeGamesClaimer/stargazers)

[![docker](https://img.shields.io/badge/Docker-lupohan44%2Fsteamdb__free__games__claimer-blue)](https://hub.docker.com/r/lupohan44/steamdb_free_games_claimer) <!--[![Build Status](https://travis-ci.org/lupohan44/SteamDBFreeGamesClaimer.svg?branch=main)](https://travis-ci.org/lupohan44/SteamDBFreeGamesClaimer)-->

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
1. Clone repository
   ```shell
   git clone https://github.com/lupohan44/SteamDBFreeGamesClaimer.git
   ```
2. Go into SteamDBFreeGamesClaimer directory
   ```shell
   cd SteamDBFreeGamesClaimer
   ```
3. Copy [config.example.json5](config.example.json5) to config.json5, change settings in it according to the comment.
4. Run with docker
   ```shell
   docker pull lupohan44/steamdb_free_games_claimer:latest && docker run -v $PWD:/home/SteamDBFreeGamesClaimer --rm lupohan44/steamdb_free_games_claimer:latest
   ```
   All changes by script inside docker will be permanently save to this folder.

## Known issue
1. Playwright does not support CentOS. ([issue](https://github.com/microsoft/playwright/issues/6219))
    - Use docker

## [Changelog](ChangeLog.md)