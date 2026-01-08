from typing import Optional, Tuple

import json

from Constants.Paths import CONFIG_DIR
from Constants.Status import ConfigStatus


def getConfig(configuration: str, key: str) -> Tuple[ConfigStatus, Optional[str]]:
    # TODO: Docstring
    configPath = CONFIG_DIR / f"{configuration}.json"

    if not configPath.exists():
        return (ConfigStatus.MISSING_FILE, None)

    try:
        with open(configPath, "r") as f:
            config = json.load(f).get(key)
        if not config:
            return (ConfigStatus.INVALID_KEY, None)
        if not validateConfig(config):
            return (ConfigStatus.INVALID_CONFIG, None)
        return (ConfigStatus.SUCCESS, config)
    except json.JSONDecodeError:
        return (ConfigStatus.BROKEN_FILE, None)
    except UnicodeDecodeError:
        return (ConfigStatus.READ_ERROR, None)
    except Exception:
        return (ConfigStatus.UNKNOWN_ERROR, None)


def validateConfig(config: str) -> bool:
    if not config:
        return False
    blacklist = ["\n", "\t", "\r"]
    if any(char in config for char in blacklist):
        return False
    return True
