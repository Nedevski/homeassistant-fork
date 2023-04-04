"""Setup for a binary sensor from the configuration.yaml."""

import logging
from time import time

from kat_bulgaria.obligations import KatError, KatPersonDetails, check_obligations
import voluptuous as vol

from homeassistant.components.binary_sensor import PLATFORM_SCHEMA, BinarySensorEntity
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

_LOGGER = logging.getLogger(__name__)
DOMAIN = "kat_bulgaria"

CONF_PERSON_EGN = "egn"
CONF_DRIVING_LICENSE = "driver_license_number"
CONF_PERSON_NAME = "person_name"

PERSON_NAME = "person_name"
PERSON_EGN = "egn"
DRIVING_LICENSE = "driver_license_number"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_PERSON_EGN): vol.All(
            cv.string, vol.Match(r"^[0-9]{2}[0,1,2,4][0-9][0-9]{2}[0-9]{4}$")
        ),
        vol.Required(CONF_DRIVING_LICENSE): vol.All(
            cv.string, vol.Match(r"^[0-9]{9}$")
        ),
        vol.Optional(CONF_PERSON_NAME): cv.string,
    }
)


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None,
) -> None:
    """Set up the platform."""

    kat_sensor = KatGlobaSensor(config)
    kat_sensor.update()
    add_entities([kat_sensor])


class KatGlobaSensor(BinarySensorEntity):
    """An entity that holds the properties for the KAT fines."""

    def __init__(self, config) -> None:
        """Set up the KAT Sensor."""
        self.egn = config[PERSON_EGN]
        self.driver_license_number = config[DRIVING_LICENSE]
        self.person_name = None

        self.person = KatPersonDetails(self.egn, self.driver_license_number)

        if PERSON_NAME in config:
            self.person_name = config[PERSON_NAME]

        if self.person_name is None:
            self._attr_name = f"Globi {self.egn}"
            self._attr_unique_id = f"globi_{self.egn}"
        else:
            self._attr_name = f"Globi {self.person_name}"
            self._attr_unique_id = f"globi_{self.person_name}"

    def update(self) -> None:
        """Fetch new state data for the sensor."""

        try:
            data = check_obligations(self.person)
        except KatError as err:
            _LOGGER.info(str(err))
            return

        if data is not None:
            self._attr_is_on = data.has_obligations
            self._attr_extra_state_attributes = {"last_updated": time()}
