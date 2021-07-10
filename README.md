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
  - telegram

## Usage
1. Clone repository

2. Install requirements

3. Copy [config.example.json](config.example.json) to config.json, change [settings](#configjson) in it.

4. Run
```shell
python3 app.py
```

## Config.json
```json
{
  "loop": true,
  "loop_delay": 60,
  "headers": {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36 Edg/80.0.361.69"
  },
  "time_format": {
    "format_str": "%Y/%m/%d %H:%M UTC",
    "utc_offset": 0
  },
  "telegram": {
    "token": "TOKEN_FROM_BOT_FATHER",
    "chat_id": "CHAT_ID_FROM_API",
    "notification_format": "<b>{game}</b>\nSub ID: <i>{sub_id}</i>\nlink: <a href=\"{steam_url}\" >{game}</a>\nfree type: {free_type}\nstart time: {start_time}\nend time: {end_time}",
    "notification_free_type": ["ALL"],
    "delay": 1
  },
  "asf": {
    "ipc": "http://127.0.0.1:1242",
    "ipc_password": "",
    "redeem_type_blacklist": ["Weekend"]
  }
}
```

*"telegram"* and *"asf"* field can be deleted if you don't want this feature, but you can't delete both fields.

When *"telegram"* is enabled, *"token"* and *"chat_id"* is required.

When *"asf"* is enabled, *"ipc"* and *"ipc_password"* is required.