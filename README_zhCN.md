# GamesHub

![GamesHub](https://socialify.git.ci/lupohan44/GamesHub/image?description=1&descriptionEditable=提供一个允许开发从不同的网站上抓取游戏并将通知发送给其他插件的插件的框架&forks=1&issues=1&language=1&logo=https%3A%2F%2Fgithub.com%2Flupohan44%2FGamesHub%2Fraw%2Fmain%2Fstatic_files%2Flogo.png&name=1&owner=1&pattern=Plus&pulls=1&stargazers=1&theme=Light)

[![project](https://img.shields.io/badge/lupohan44-GamesHub-brightgreen)](https://github.com/lupohan44/GamesHub) [![GitHub 许可证](https://img.shields.io/github/license/lupohan44/GamesHub)](https://github.com/lupohan44/GamesHub/blob/main/LICENSE) [![GitHub stars](https://img.shields.io/github/stars/lupohan44/GamesHub)](https://github.com/lupohan44/GamesHub/stargazers) [![docker](https://img.shields.io/badge/Docker-lupohan44%2Fgames_hub-blue?logo=docker)](https://hub.docker.com/r/lupohan44/games_hub) [![构建状态](https://api.travis-ci.com/lupohan44/GamesHub.svg)](https://travis-ci.com/github/lupohan44/GamesHub)

[README](README.md) | [中文文档](README_zhCN.md)

本项目的灵感来源于 [SteamDB-FreeGames](https://github.com/azhuge233/SteamDB-FreeGames)

Telegram 讨论组：[https://t.me/GamesHubDiscussion](https://t.me/GamesHubDiscussion)

## Star 历史
[![Stargazers over time](https://starchart.cc/lupohan44/GamesHub.svg)](https://starchart.cc/lupohan44/GamesHub)

## 特性
提供一个允许开发从不同的网站上抓取游戏并将通知发送给其他插件的插件的框架

## 官方插件 (由本项目维护)
:white_check_mark: 从 [SteamDB](https://steamdb.info/upcoming/free/) 获取 Steam 免费游戏(不建议使用)

:white_check_mark: 从 [Keylol](https://keylol.com/t572814-1-1) 获取免费游戏(建议使用)

:white_check_mark: 从 [Reddit](https://www.reddit.com/r/freegames) 获取免费游戏。

:white_check_mark: 使用 [Apprise](https://github.com/caronc/apprise) 发送免费游戏信息。[(Telegram 演示频道)](https://t.me/GamesHubDemo)

:white_check_mark: 使用 [ASF](https://github.com/JustArchiNET/ArchiSteamFarm) 领取游戏

:white_check_mark: 使用 [Steam](https://github.com/ValvePython/steam) 领取游戏

## 依赖项

- python3
   - [requirements.txt](requirements.txt)

## 使用方法
### 直接运行
1. 克隆存储库
   ```shell
   git clone https://github.com/lupohan44/GamesHub.git
   ```
2. 进入 GamesHub 目录
   ```shell
   cd GamesHub
   ```
3. 安装依赖项
   ```shell
   pip3 install -r requirements.txt
   playwright install webkit chromium firefox || python3 -m playwright install webkit chromium firefox
   # 取决于您想要使用什么浏览器
   ```
   或者安装最少的依赖项
   ```shell
   pip install -r requirements-no_plugin.txt
   ```
   并根据所需插件安装对应插件所需的依赖项
4. 将 [config.example.json5](config.example.json5) 复制为 `config.json5`，并根据注释修改其中的设置。
5. 运行
   ```shell
   python3 app.py
   ```
   每个启用的官方插件应在 `{工作目录}/plugins/{插件包名}` 下创建一个文件夹，用于存储运行时文件和配置。
6. 修改步骤 5 中的插件配置文件
7. 重新运行步骤 5

### Docker（仅适用于 Linux）
1. 创建用于记录和配置的文件夹，假设文件夹名为 `/var/GamesHub`

   _请注意，此文件夹名必须为绝对路径。_
   ```shell
   export GAMES_HUB_FOLDER_NAME=/var/GamesHub
   mkdir -p "$GAMES_HUB_FOLDER_NAME"
   ```
2. 下载 [config.example.json5](config.example.json5) 并将其重命名为 `config.json5`，放入步骤 1 创建的文件夹中，根据注释修改其中的设置。
   ```shell
   wget -c "https://raw.githubusercontent.com/lupohan44/GamesHub/main/config.example.json5" -O "$STEAM_DB_FOLDER_NAME/config.json5" || curl -o "$STEAM_DB_FOLDER_NAME/config.json5" "https://raw.githubusercontent.com/lupohan44/GamesHub/main/config.example.json5"
   ```
3. 使用 Docker 运行
   ```shell
   docker pull lupohan44/games_hub:latest && docker run -v $GAMES_HUB_FOLDER_NAME:/home/wd --rm lupohan44/games_hub:latest
   ```
   Docker 中的脚本所做的所有更改将永久保存在此文件夹中。
   每个启用的官方插件应在 `{工作目录}/plugins/{插件包名}` 下创建一个文件夹，用于存储运行时文件和配置。
4. 修改步骤 3 中的插件配置文件
5. 重新运行步骤 3

## 插件结构示例
   ```
   /var/GamesHub (工作目录)
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

## 已知问题
1. Playwright 不支持 CentOS。 ([Issue](https://github.com/microsoft/playwright/issues/6219))
   - 使用 Docker

## 开发插件
1. 为您的插件思考一个包名称，格式应为 gameshub.unofficial.{plugin_purpose}.{plugin_description}[.{your_name}]。
2. 将官方插件中的一个副本复制到 [plugins](plugins) 文件夹，并将其重命名为您的包名称。
3. 按照官方插件的结构进行修改以满足您的需求。

## [更新日志(英文)](ChangeLog.md)

## 特别感谢
- 本项目图标由限免喜加一设计
  ![WechatQrCode](static_files/wechat-QRcode.jpg)

## 支持我
1. [![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/lupohan44)
2. 给这个存储库点赞
3. 通过PR为该项目做出贡献

选择以上任何一个项目都将对我做出巨大贡献。谢谢。
