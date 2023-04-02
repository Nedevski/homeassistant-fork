"""Example integration using DataUpdateCoordinator."""

import logging
from time import time

from requests import HTTPError, get

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

_LOGGER = logging.getLogger(__name__)
DOMAIN = "kat_bulgaria"

PERSON_NAME = "person_name"
PERSON_EGN = "egn"
DRIVING_LICENSE = "driver_license_number"


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None,
) -> None:
    """Set up the alarm platform."""

    kat_sensor = KatGlobaSensor(config)
    kat_sensor.update()
    add_entities([kat_sensor])


class KatGlobaSensor(BinarySensorEntity):
    """An entity using CoordinatorEntity.

    The CoordinatorEntity class provides:
      should_poll
      async_update
      async_added_to_hass
      available
    """

    def __init__(self, config) -> None:
        """Set up the KAT Globa Sensor."""
        self.egn = config[PERSON_EGN]
        self.driver_license_number = config[DRIVING_LICENSE]
        self.person_name = None

        if PERSON_NAME in config:
            self.person_name = config[PERSON_NAME]

        if self.person_name is None:
            self._attr_name = f"Globi {self.egn}"
            self._attr_unique_id = f"globi_{self.egn}"
        else:
            self._attr_name = f"Globi {self.person_name}"
            self._attr_unique_id = f"globi_{self.person_name}"

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """

        try:
            data = check_globa(self.egn, self.driver_license_number)
        except HTTPError as ex:
            _LOGGER.error(ex)
            return

        self._attr_is_on = data["hasNonHandedSlip"]
        self._attr_extra_state_attributes = {"last_updated": time()}


def check_globa(egn: str, driver_license_number: str):
    """Wololo."""

    try:
        url = "https://e-uslugi.mvr.bg/api/Obligations/AND?mode=1&obligedPersonIdent={egn}&drivingLicenceNumber={driver_license_number}".format(
            egn=egn, driver_license_number=driver_license_number
        )
        headers = {
            "content-type": "application/json",
        }
        res = get(url, headers=headers, timeout=10)

    except HTTPError as ex:
        _LOGGER.error("Request to get the globi failed: %ex", str(ex))
        return

    return res.json()
