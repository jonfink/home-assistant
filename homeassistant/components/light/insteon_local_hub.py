"""
Support for Insteon Hub lights with local hub

"""
from homeassistant.components.insteon_local_hub import INSTEON
from homeassistant.components.light import (ATTR_BRIGHTNESS,
                                            SUPPORT_BRIGHTNESS, Light)

DEPENDENCIES = ['insteon_local_hub']

SUPPORT_INSTEON_HUB = SUPPORT_BRIGHTNESS

import logging
_LOGGER = logging.getLogger(__name__)

from homeassistant.helpers.entity import _OVERWRITE as customize_dict

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the Insteon Hub light platform."""

    devs = []
    for (device_id, device_data) in INSTEON.get_linked().items():
        _LOGGER.debug("Processing %s" % device_id.lower())
        if device_data['cat_type'] == "dimmer":
            light_customize = customize_dict.get('light.'+device_id.lower(), {})
            friendly_name = light_customize.get('friendly_name', 'Insteon_'+device_id.lower())
            devs.append(InsteonLocalToggleDevice(INSTEON.dimmer(device_id), friendly_name))
        else:
            _LOGGER.warn("Unsupported device category")
    add_devices(devs)

class InsteonLocalToggleDevice(Light):
    """An abstract Class for an Insteon node."""

    def __init__(self, node, name):
        """Initialize the device."""

        self.node = node
        self.friendly_name = name
        self._value = 0

    @property
    def name(self):
        """Return the the name of the node."""
        #return self.node.device_id
        return self.friendly_name

    @property
    def unique_id(self):
        """Return the ID of this insteon node."""
        return self.node.device_id

    @property
    def brightness(self):
        """Return the brightness of this light between 0..255."""
        return self._value / 100 * 255

    def update(self):
        """Update state of the sensor."""
        status = INSTEON.get_device_status(self.node.device_id, 0)
        print('GOT DIMMER STATUS for %s' % (self.node.device_id), status)
        try:
            if status is not None:
                self._value = 100*float(int(status['cmd2'], 16))/255.
        except KeyError:
            pass
        pass

    @property
    def is_on(self):
        """Return the boolean response if the node is on."""
        return self._value != 0

    @property
    def supported_features(self):
        """Flag supported features."""
        return SUPPORT_INSTEON_HUB

    def turn_on(self, **kwargs):
        """Turn device on."""
        if ATTR_BRIGHTNESS in kwargs:
            self._value = kwargs[ATTR_BRIGHTNESS] / 255 * 100
            self.node.on(self._value)
        else:
            self._value = 100
            self.node.on(self._value)
        self.schedule_update_ha_state()

    def turn_off(self, **kwargs):
        """Turn device off."""
        self.node.off()
        self._value = 0
        self.schedule_update_ha_state()
