from enum import Enum


class ConfigStatus(Enum):
    # General
    SUCCESS = 0
    UNKNOWN_ERROR = 127

    # File-Errors (1x)
    MISSING_FILE = 11
    BROKEN_FILE = 12
    # ----------- (1x)

    # Configuration-Errors (2x)
    INVALID_CONFIG = 21
    READ_ERROR = 22
    INVALID_KEY = 23
    # -------------------- (2x)
