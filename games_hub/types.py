from enum import Enum


class GamePlatform(Enum):
    STEAM = "Steam"
    EPIC = "Epic"
    ORIGIN = "Origin"
    UPLAY = "Uplay"
    GOG = "GOG"
    BATTLENET = "Battle.net"
    AMAZON = "Amazon"
    WINDOWS_STORE = "Windows Store"
    HUMBLE_BUNDLE = "Humble Bundle"
    BETHESDA = "Bethesda"
    OTHER = "Other"


class GameFreeType(Enum):
    LIMITED_TIME = "Limited Time"
    KEEP_FOREVER = "Keep Forever"
