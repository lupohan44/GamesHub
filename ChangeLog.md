# Changelog
## 2021/7/13
1. Fix wrong command in default telegram notify message (#3)
2. Separate changelog from README.md (No one care about changelog)
3. Modify README.md

## 2021/7/12-2
1. Fix wrong requirements "telegram"
2. Support json5 (#2)
3. Change README.md

**Notice**: This upgrade change config.json to config.json5 and change record.json to record.json5

Run
```shell
pip3 uninstall telegram
```
should remove the wrong requirements

## 2021/7/12
1. Fix wrong requirements
2. Change loop delay default value to 600 seconds
3. Support MarkDown format in telegram notification
4. Support multiple chat_id in telegram
5. Change README.md

**Notice**: This upgrade change config.json
## 2021/7/11
1. Initial release