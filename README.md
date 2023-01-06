# GamesHub

![GamesHubLogo](static_files/logo.png)

[![project](https://img.shields.io/badge/lupohan44-GamesHub-brightgreen)](https://github.com/lupohan44/GamesHub) [![GitHub license](https://img.shields.io/github/license/lupohan44/GamesHub)](https://github.com/lupohan44/GamesHub/blob/main/LICENSE) [![GitHub stars](https://img.shields.io/github/stars/lupohan44/GamesHub)](https://github.com/lupohan44/GamesHub/stargazers) [![docker](https://img.shields.io/badge/Docker-lupohan44%2Fgames_hub-blue?logo=docker)](https://hub.docker.com/r/lupohan44/games_hub) [![Build Status](https://api.travis-ci.com/lupohan44/GamesHub.svg)](https://travis-ci.com/github/lupohan44/GamesHub)

This project is inspired by [SteamDB-FreeGames](https://github.com/azhuge233/SteamDB-FreeGames)

Telegram discussion group: [https://t.me/GamesHubDiscussion](https://t.me/GamesHubDiscussion)

## Star History
[![Stargazers over time](https://starchart.cc/lupohan44/GamesHub.svg)](https://starchart.cc/lupohan44/GamesHub)

## Features
Provide a framework to develop plugins to scrap games from different websites and send notifications to other plugins

## Official Plugins (Maintained by project)
:white_check_mark: Gather Steam free games from [SteamDB](https://steamdb.info/upcoming/free/). (Not recommended)

:white_check_mark: Gather free games from [Keylol](https://keylol.com/t572814-1-1). (recommended)

:white_check_mark: Gather free games from [Reddit](https://www.reddit.com/r/freegames).

:white_check_mark: Use [Apprise](https://github.com/caronc/apprise) to send free games information. [(Telegram demo channel)](https://t.me/GamesHubDemo)

:white_check_mark: Use [ASF](https://github.com/JustArchiNET/ArchiSteamFarm) to redeem games

:white_check_mark: Use [Steam](https://github.com/ValvePython/steam) to redeem games
## Requirements

- python3
  - [requirements.txt](requirements.txt)

## Usage
### Direct run
1. Clone repository
   ```shell
   git clone https://github.com/lupohan44/GamesHub.git
   ```
2. Go into GamesHub directory
   ```shell
   cd GamesHub
   ```
3. Install requirements
   ```shell
   pip3 install -r requirements.txt
   playwright install webkit chromium firefox || python3 -m playwright install webkit chromium firefox
   # Depends on the browser(s) you want to use
   ```
   or install minimum requirements
   ```shell
   pip install -r requirements-no_plugin.txt
   ```
   and install requirements for each plugin you want to enable
4. Copy [config.example.json5](config.example.json5) to ```config.json5```, change settings in it according to the comment.
5. Run
   ```shell
   python3 app.py
   ```
   Each enabled official plugin should create a folder in ```{WORKING_DIR}/plugins/{PLUGIN_PACKAGE_NAME}``` to store runtime files and configs
6. Change plugins' config files from step 5
7. Rerun step 5
### Docker (For Linux only)
1. Create a folder for record and config, let's say folder name is /var/GamesHub

   _Please note that this folder name must be absolute path._
      ```shell
      export GAMES_HUB_FOLDER_NAME=/var/GamesHub
      mkdir -p "$GAMES_HUB_FOLDER_NAME"
      ```
2. Download [config.example.json5](config.example.json5) and rename to ```config.json5``` into the folder created in step 1, change settings in it according to the comment.
   ```shell
   wget -c "https://raw.githubusercontent.com/lupohan44/GamesHub/main/config.example.json5" -O "$STEAM_DB_FOLDER_NAME/config.json5" || curl -o "$STEAM_DB_FOLDER_NAME/config.json5" "https://raw.githubusercontent.com/lupohan44/GamesHub/main/config.example.json5"
   ```
3. Run with docker
   ```shell
   docker pull lupohan44/games_hub:latest && docker run -v $GAMES_HUB_FOLDER_NAME:/config --rm lupohan44/games_hub:latest
   ```
   All changes by script inside docker will be permanently save to this folder.  
   Each enabled official plugin should create a folder in ```{WORKING_DIR}/plugins/{PLUGIN_PACKAGE_NAME}``` to store runtime files and configs
4. Change plugins' config files from step 3
5. Rerun step 3

## Plugins structure example
   ```
   /var/GamesHub (working directory)
   ├── config.json5
   └── plugins
       ├── gameshub.official.notification.apprise
       │   └── config.json5
       ├── gameshub.official.scraper.steamdb
       │   └── config.json5
       ├── gameshub.official.scraper.keylol
       │   ├── config.json5
       │   └── cookies.txt
       └── gameshub.official.redeemer.asf
           └── config.json5
   ```
## Known issue
1. Playwright does not support CentOS. ([issue](https://github.com/microsoft/playwright/issues/6219))
    - Use docker

## Develop plugins
1. Think a package name for your plugin, format should be like gameshub.unofficial.{plugin_purpose}.{plugin_description}[.{your_name}]
2. Copy one of the official plugin in [plugins](plugins) folder and rename it to your package name
3. Follow the official plugin's structure and modify it to your needs

## [Changelog](ChangeLog.md)

## Special Thanks
- The logo is designed by 限免喜加一
![WechatQrCode](static_files/wechat-QRcode.jpg)

## Support me
1. [![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/lupohan44)
2. Star this repository
3. Contribute to this project by pull request

Each of them is appreciated. Thank you.
