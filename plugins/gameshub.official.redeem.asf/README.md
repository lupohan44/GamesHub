# ASF Redeem (gameshub.official.redeem.asf)

## Description
This is plugin to redeem steam free games using [ASF](https://github.com/JustArchiNET/ArchiSteamFarm)

## [Requirements](requirements.txt)
- [ASF](https://github.com/JustArchiNET/ArchiSteamFarm)

## Changelog
v1.0.4
- Fix plugin broken since last commit

v1.0.3
- Redeem using appid should add 'a/' prefix, using subid should add 's/' prefix

v1.0.2
- Fix error when start time or end time is None

v1.0.1
- Add version
- Move all runtime files to {WORKING_DIR}/plugins/{PLUGIN_PACKAGE_NAME}
- Change create folder from os.mkdir to os.makedirs

v1.0.0
- Initial release
