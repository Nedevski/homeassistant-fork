"""Binary sensor platform."""

from datetime import datetime, timedelta
import logging

from kat_bulgaria.obligations import KatApi, KatApiResponse

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    BINARY_SENSOR_ENTITY_PREFIX,
    BINARY_SENSOR_NAME_PREFIX,
    CONF_DRIVING_LICENSE,
    CONF_PERSON_EGN,
    CONF_PERSON_NAME,
    DOMAIN,
)

SCAN_INTERVAL = timedelta(minutes=20)
_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the platform from config_entry."""

    person_name: str = str(entry.data.get(CONF_PERSON_NAME)).lower().capitalize()
    person_egn: str = str(entry.data.get(CONF_PERSON_EGN))
    license_number: str = str(entry.data.get(CONF_DRIVING_LICENSE))

    api: KatApi = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [KatObligationsSensor(api, person_name, person_egn, license_number)], True
    )


class KatObligationsSensor(BinarySensorEntity):
    """A simple sensor."""

    def __init__(self, api: KatApi, name: str, egn: str, license_number: str) -> None:
        """Initialize the sensor."""

        self.api = api

        self._attr_name = f"{BINARY_SENSOR_NAME_PREFIX}{name}"
        self._attr_unique_id = f"{BINARY_SENSOR_ENTITY_PREFIX}{name}"

        self.egn = egn
        self.license_number = license_number

    async def async_update(self) -> None:
        """Fetch new state data for the sensor."""

        resp: KatApiResponse[bool] = await self.api.async_check_obligations(
            self.egn, self.license_number
        )
        if resp.success:
            self._attr_is_on = resp.data
            self._attr_extra_state_attributes = {
                "last_updated": datetime.now().isoformat()
            }
        else:
            _LOGGER.warning(resp.error_message)
