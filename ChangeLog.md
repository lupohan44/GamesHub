# Changelog
## 1.2.0
1. Supports new SteamDB website structure
2. Fix docker not working properly (#6)

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
1. Support docker (#1)
2. Increase wait time for cloudflare redirect to enhance stability

### 2021/7/13
1. Fix wrong command in default telegram notify message (#3)
2. Separate changelog from README.md (No one care about changelog)

### 2021/7/12
1. Fix wrong requirements
2. Change loop delay default value to 600 seconds
3. Support MarkDown format in telegram notification
4. Support multiple chat_id in telegram
5. Fix wrong requirements "telegram"
6. Support json5 (#2)

**Notice**: This upgrade change config.json to config.json5 and change record.json to record.json5

Run
```shell
pip3 uninstall telegram
```
should remove the wrong requirements

### 2021/7/11
1. Initial release