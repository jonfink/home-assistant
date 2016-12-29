"""
Support for Insteon Hub with Local Connection

"""
import logging

import voluptuous as vol

from homeassistant.const import (CONF_HOST, CONF_PASSWORD, CONF_USERNAME, CONF_PORT)
from homeassistant.helpers import discovery
import homeassistant.helpers.config_validation as cv

REQUIREMENTS = ['insteonlocal==0.39']

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'insteon_local_hub'
INSTEON = None

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PORT): cv.string,
    })
}, extra=vol.ALLOW_EXTRA)


def setup(hass, config):
    """Setup Insteon Hub component.

    This will automatically import associated lights.
    """
    # pylint: disable=unreachable
    from insteonlocal.Hub import Hub

    username = config[DOMAIN][CONF_USERNAME]
    password = config[DOMAIN][CONF_PASSWORD]
    ip = config[DOMAIN][CONF_HOST]
    port = config[DOMAIN][CONF_PORT]

    global INSTEON

    INSTEON = Hub(ip, username, password, port, logger=_LOGGER)

    if INSTEON is None:
        _LOGGER.error("Could not connect to Insteon service")
        return False

    discovery.load_platform(hass, 'light', DOMAIN, {}, config)

    return True
