# SteamDB Scrapper (gameshub.official.scrapper.steamdb)

## Description
This is plugin to use [playwright](https://playwright.dev/python/docs/intro) scrap free games information from [steamdb](https://steamdb.info/upcoming/free/)

**Seems that SteamDB really don't want people scraping their site.**

## Changelog
v1.0.2
- Fix when start time or end time is None, sqlite3 will raise error

v1.0.1
- Add version
- Fix wrong start time and end time when it is not available on steamdb
- Move all runtime files to {WORKING_DIR}/plugins/{PLUGIN_PACKAGE_NAME}
- Change create folder from os.mkdir to os.makedirs

v1.0.0
- Initial release
