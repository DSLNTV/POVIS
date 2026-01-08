import requests

from Configurator import getConfig
from Constants.Status import AlertStatus
from Constants.Status import ConfigStatus


def sendAlert(message: str) -> AlertStatus:
    # TODO: Docstring
    token_status, token = getConfig("Telegram", "token")
    if token_status != ConfigStatus.SUCCESS:
        # TODO: Logging
        return AlertStatus.BAD_CONFIG_TOKEN

    chatId_status, chatId = getConfig("Telegram", "chat-id")
    if chatId_status != ConfigStatus.SUCCESS:
        # TODO: Logging
        return AlertStatus.BAD_CONFIG_CHAT_ID

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chatId, "text": message, "parse_mode": "Markdown"}

    try:
        response = requests.post(url, json=payload, timeout=10)
        # TODO: timeout- and repeat-mechanism

        match response.status_code:
            case 200:
                return AlertStatus.SUCCESS
            case 401:
                return AlertStatus.INVALID_TOKEN
            case 400:
                return AlertStatus.MALFORMED_MESSAGE
            case 403:
                return AlertStatus.INVALID_CHAT_ID
            case 429:
                return AlertStatus.RATE_LIMIT_REACHED
            case _:
                return AlertStatus.UNKNOWN_ERROR

    except requests.exceptions.Timeout:
        return AlertStatus.NETWORK_TIMEOUT
    except requests.exceptions.RequestException:
        return AlertStatus.CONNECTION_FAILED
