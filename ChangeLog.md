# Changelog
## 2.0.1
### 2022/11/3
1. Remove version in [requirements.txt](requirements.txt)
2. Add [requirements-no_plugin.txt](requirements-no_plugin.txt) for users who don't want to use any official plugins
3. Add new plugin [Keylol Scrapper](plugins/gameshub.official.scrapper.keylol)

### 2022/10/19
1. Fix ASF redeeming fail cause system crash issue
2. Fix plugins config load too late

## 2.0.0
1. Rename the project to GamesHub (from SteamDBFreeGamesClaimer)
2. Change the project's architecture to plugin based
3. Remove check_update_when setting, check update on startup now
4. Add github mirror for check update
5. Remove loop option in SteamDBScrapper plugin, now it will loop forever
6. Add browser option in SteamDBScrapper plugin, now it support webkit, chromium and firefox
7. Add headless option in SteamDBScrapper plugin
8. Change notification method to [Apprise](https://github.com/caronc/apprise)
9. Change ASFRedeem plugin settings

## 1.2.2
1. Fix wrong indent in config.example.json5
2. Add version tag in docker image
3. Support argument: "-h" or "--help" to show help message
4. Support argument: "-v" or "--version" to show version
5. Support argument: "-c" or "--check-update" to check update

## 1.2.1

### 2021/12/26
1. Add new config option to take screenshot while waiting for steamdb loading

### 2021/12/22
1. Add bot whitelist ([#9](/../../pull/9))

## 1.2.0
1. Supports new SteamDB website structure
2. Fix docker not working properly ([#6](/../../issues/6))
3. Fix broken links in ChangeLog

## 1.1.1
1. Remove default telegram message from source code
2. Change example telegram message
3. Add check update option in config
4. Add variable {steamdb_url} in telegram message
5. Remove unused code

## 1.1.0
1. Use SQLite to store records
2. Fix "loop" setting not working
3. Enhance version compare
4. Enhance docker

## 1.0.1
1. Always redeem games since free might not begin yet
2. Increase loop delay time
3. Merge upstream changes(https://github.com/azhuge233/SteamDB-FreeGames)

## 1.0.0

### 2021/7/18
1. Add update checking
2. Isolate static variables
3. Add banner

### 2021/7/17
1. Support docker ([#1](/../../issues/1))
2. Increase wait time for cloudflare redirect to enhance stability

### 2021/7/13
1. Fix wrong command in default telegram notify message ([#3](/../../issues/13))
2. Separate changelog from README.md (No one care about changelog)

### 2021/7/12
1. Fix wrong requirements
2. Change loop delay default value to 600 seconds
3. Support MarkDown format in telegram notification
4. Support multiple chat_id in telegram
5. Fix wrong requirements "telegram"
6. Support json5 ([#2](/../../issues/2))

**Notice**: This upgrade change config.json to config.json5 and change record.json to record.json5

Run
```shell
pip3 uninstall telegram
```
should remove the wrong requirements

### 2021/7/11
1. Initial release
