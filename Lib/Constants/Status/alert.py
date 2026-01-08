from enum import Enum


class AlertStatus(Enum):
    # General
    SUCCESS = 0
    UNKNOWN_ERROR = 127

    # Configuration Errors (1x)
    BAD_CONFIG_TOKEN = 11
    BAD_CONFIG_CHAT_ID = 12
    # -------------------- (1x)

    # Connection Errors (2x)
    NETWORK_TIMEOUT = 21
    CONNECTION_FAILED = 22
    # ----------------- (2x)

    # Telegram API Errors (3x)
    INVALID_TOKEN = 31  # HTTP:401
    INVALID_CHAT_ID = 32  # HTTP:403
    MALFORMED_MESSAGE = 33  # HTTP:400
    # ------------------- (3x)

    # Resource Errors (4x)
    RATE_LIMIT_REACHED = 41  # HTTP:429
    # --------------- (4x)
