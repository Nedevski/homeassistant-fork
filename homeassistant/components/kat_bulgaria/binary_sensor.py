"""Setup for a binary sensor from the configuration.yaml."""

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

        data = get_kat_fines(self.egn, self.driver_license_number)

        if data is not None:
            self._attr_is_on = data["hasNonHandedSlip"]
            self._attr_extra_state_attributes = {"last_updated": time()}


def get_kat_fines(egn: str, driver_license_number: str):
    """Call the public BG government API to check if the person has fines."""

    try:
        url = "https://e-uslugi.mvr.bg/api/Obligations/AND?mode=1&obligedPersonIdent={egn}&drivingLicenceNumber={driver_license_number}".format(
            egn=egn, driver_license_number=driver_license_number
        )
        headers = {
            "content-type": "application/json",
        }
        res = get(url, headers=headers, timeout=10)

    except HTTPError as ex:
        _LOGGER.warning("KAT Bulgaria HTTP call failed: %e", str(ex))
        return None
    except TimeoutError as ex:
        _LOGGER.info("KAT Bulgaria HTTP call TIMEOUT: %e", str(ex))
        return None

    return res.json()
