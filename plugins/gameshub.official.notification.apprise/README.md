# Apprise Notifier (gameshub.official.notification.apprise)

## Description
This is plugin to send free games information using [Apprise](https://github.com/caronc/apprise)

## [Requirements](requirements.txt)

## Changelog
v1.0.2
- Fix extra_info will show "None" when extra_info field is None

v1.0.1
- Add version
- Send "N/A" when start time or end time is not available
- Move all runtime files to {WORKING_DIR}/plugins/{PLUGIN_PACKAGE_NAME}
- Change create folder from os.mkdir to os.makedirs

v1.0.0
- Initial release
