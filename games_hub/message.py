from games_hub.static import *

PARSING_CONFIG_MSG = "parsing %s"
NO_NEW_VERSION_MSG = "Current version is up to date!"
FOUND_NEW_VERSION_MSG = "Found new version %s on github!"
LOADING_PLUGINS_MSG = "loading plugins %s"
PLUGIN_LOADED_MSG = "plugin %s loaded"
USER_INTERRUPT_EXIT_MSG = "User interrupt, exit"
REDEEM_GAME_MSG = "redeeming game %s, sub_id: %s"
REDEEM_GAME_SUCCESS_MSG = "redeem game command %s success"

# warning message
CANNOT_CHECK_UPDATE_WARNING_MSG = "Cannot check update from github!"
CANNOT_LOAD_PLUGIN_WARNING_MSG = "failed to load plugins %s\n error:\n %s"

# error message
CONFIG_NOT_EXIST_ERROR_MSG = "Cannot read %s!" % GAMESHUB_CONFIG_FILE
TELEGRAM_REQUIRE_TOKEN_ERROR_MSG = "Cannot get token of telegram from %s!" % GAMESHUB_CONFIG_FILE
TELEGRAM_REQUIRE_CHAT_ID_ERROR_MSG = "Cannot get chat_id of telegram from %s!" % GAMESHUB_CONFIG_FILE
ASF_REQUIRE_IPC_ERROR_MSG = "Cannot get ipc of asf from %s!" % GAMESHUB_CONFIG_FILE
AT_LEAST_ENABLE_ONE_FUNCTION_ERROR_MSG = "Both telegram and asf are not enabled!"
CONFIG_FILE_NEEDS_TO_BE_UPDATED = "%s's format has been changed, please change it accordingly!" % GAMESHUB_CONFIG_FILE
GET_PAGE_SOURCE_ERROR_MSG = "Get page source error!"
NO_PLUGINS_FOLDER_ERROR_MSG = "Cannot find plugins folder!"
NO_PLUGINS_ENABLE_ERROR_MSG = "No plugins enabled!"
PLUGINS_FOLDER_EMPTY_ERROR_MSG = "Plugins folder is empty!"
SEND_NOTIFICATION_ERROR_MSG = "Error occurred when notify receiver: %s"
