"""SMSAERO notify component."""
import json
import logging

from aiohttp.hdrs import CONTENT_TYPE
import requests
import voluptuous as vol

from homeassistant.components.notify import ATTR_TARGET, PLATFORM_SCHEMA, BaseNotificationService
from homeassistant.const import (
    CONF_API_KEY,
    CONF_LOGIN,
    CONF_SENDER,
    CONTENT_TYPE_JSON,
)
from http import HTTPStatus
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

BASE_API_URL = "https://gate.smsaero.ru/v2/sms"
DEFAULT_SENDER = "SERVICE"
TIMEOUT = 5

PLATFORM_SCHEMA = vol.Schema(
    vol.All(
        PLATFORM_SCHEMA.extend(
            {
                vol.Required(CONF_API_KEY): cv.string,
                vol.Required(CONF_LOGIN): cv.string,
                vol.Optional(CONF_SENDER, default=DEFAULT_SENDER): cv.string,
            }
        )
    )
)

def get_service(hass, config, discovery_info=None):
    """Get the SMSAERO notification service."""
    return SmsAeroNotificationService(config)

class SmsAeroNotificationService(BaseNotificationService):
    """Implementation of a notification service for the SMSAERO service."""

    def __init__(self, config):
        """Initialize the service."""
        self.api_key = config[CONF_API_KEY]
        self.login = config[CONF_API_KEY]
        self.sender = config[CONF_SENDER]

    def send_message(self, message="", **kwargs):
        """Send SMS to specified target user cell."""
        targets = kwargs.get(ATTR_TARGET)

        api_url = f"{BASE_API_URL}/send"

        if not targets:
            _LOGGER.info("At least 1 target is required")
            return

        for target in targets:
            url_param = {
                "number": target,
                "text": message,
                "from": self.sender,
            }
            resp = requests.get(api_url, auth=(self.login, self.api_key), params=url_param, timeout=TIMEOUT)

            if resp.status_code != HTTPStatus.OK:
                _LOGGER.error("Error %s", resp.status_code)
            else:
                data = resp.json()
                if data['success'] is not True:
                    _LOGGER.error(
                        "Error %s (Code %s)", data['data'], data['success']
                    )