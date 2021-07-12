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
3. Copy [config.example.json](config.example.json) to config.json, change [settings](#configjson) in it.
4. Run
   ```shell
   python3 app.py
   ```

## Config.json

Notice: **DO NOT** copy paste from below
```json5
{
  "loop": true,
  "loop_delay": 600,
  "headers": {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36 Edg/80.0.361.69"
  },
  "time_format": {
    "format_str": "%Y/%m/%d %H:%M UTC",
    "utc_offset": 0
  },
  // Remove this field if you don't need it, but you can't remove it and "asf" at the same time
  "telegram": {
    // Required
    "token": "TOKEN_FROM_BOT_FATHER",
    // Required
    "chat_id": [
      "CHAT_ID_FROM_API"
    ],
    "format": {
      "markdown": false,
      "message": "<b>{game}</b>\nSub ID: <i>{sub_id}</i>\nlink: <a href=\"{steam_url}\" >{game}</a>\nfree type: {free_type}\nstart time: {start_time}\nend time: {end_time}\n!redeem asf {sub_id}"
    },
    // "ALL" will include all free types
    "notification_free_type": ["ALL"],
    // Delay after each message sent by telegram bot
    "delay": 1
  },
  // Remove this field if you don't need it, but you can't remove it and "telegram" at the same time
  "asf": {
    // Required
    "ipc": "http://127.0.0.1:1242",
    "ipc_password": "",
    "redeem_type_blacklist": ["Weekend"]
  }
}
```

## Known issue
1. Playwright does not support CentOS. ([issue](https://github.com/microsoft/playwright/issues/6219))

## Changelog
###2021/7/12
1. Fix wrong requirements
2. Change loop delay default value to 600 seconds
3. Support MarkDown format in telegram notification
4. Support multiple chat_id in telegram
5. Change README.md

**Notice**: This upgrade change config.json
###2021/7/11
1. Initial release