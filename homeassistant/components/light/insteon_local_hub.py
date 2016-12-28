"""
Support for Insteon Hub lights with local hub

"""
from homeassistant.components.insteon_local_hub import INSTEON
from homeassistant.components.light import (ATTR_BRIGHTNESS,
                                            SUPPORT_BRIGHTNESS, Light)

DEPENDENCIES = ['insteon_local_hub']

SUPPORT_INSTEON_HUB = SUPPORT_BRIGHTNESS


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the Insteon Hub light platform."""
    devs = []
    for (device_id, device_data) in INSTEON.getLinked().items():
        if device_data['cat_type'] == "dimmer":
            devs.append(InsteonLocalToggleDevice(INSTEON.dimmer(device_id)))
    add_devices(devs)

class InsteonLocalToggleDevice(Light):
    """An abstract Class for an Insteon node."""

    def __init__(self, node):
        """Initialize the device."""
        self.node = node
        self._value = 0

    @property
    def name(self):
        """Return the the name of the node."""
        return self.node.deviceId

    @property
    def unique_id(self):
        """Return the ID of this insteon node."""
        return self.node.deviceId

    @property
    def brightness(self):
        """Return the brightness of this light between 0..255."""
        return self._value / 100 * 255

    def update(self):
        """Update state of the sensor."""
        status = INSTEON.getDeviceStatus(self.node.deviceId, 0)
        print('GOT DIMMER STATUS for %s' % (self.node.deviceId), status)
        try:
            if status is not None:
                self._value = 100*float(status['cmd2'])/255.
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

    def turn_off(self, **kwargs):
        """Turn device off."""
        self.node.off()
        self._value = 0
