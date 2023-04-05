"""Tests the kat_bulgaria platform."""

# import pytest

from homeassistant.components.binary_sensor import DOMAIN as BINARY_SENSOR_DOMAIN
from homeassistant.components.kat_bulgaria.binary_sensor import DOMAIN
from homeassistant.components.kat_bulgaria.const import (
    CONF_DRIVING_LICENSE,
    CONF_PERSON_EGN,
    CONF_PERSON_NAME,
)
from homeassistant.core import HomeAssistant

# from homeassistant.config_entries import SOURCE_USER
from homeassistant.setup import async_setup_component  # , setup_component

# from tests.common import MockConfigEntry
# from unittest.mock import PropertyMock, patch

# from kat_bulgaria.obligations import KatPersonDetails

VALID_CONFIG_FULL = {
    BINARY_SENSOR_DOMAIN: {
        "platform": DOMAIN,
        CONF_PERSON_EGN: "0011223344",
        CONF_DRIVING_LICENSE: "123456789",
        CONF_PERSON_NAME: "Nikola",
    }
}

VALID_CONFIG = {
    BINARY_SENSOR_DOMAIN: {
        "platform": DOMAIN,
        CONF_PERSON_EGN: "0011223344",
        CONF_DRIVING_LICENSE: "123456789",
    }
}

INVALID_EGN_CONFIG = {
    BINARY_SENSOR_DOMAIN: {
        "platform": DOMAIN,
        CONF_PERSON_EGN: "9999999999",
        CONF_DRIVING_LICENSE: "123456789",
    }
}

INVALID_DRIVER_LICENSE_CONFIG = {
    BINARY_SENSOR_DOMAIN: {
        "platform": DOMAIN,
        CONF_PERSON_EGN: "0011223344",
        CONF_DRIVING_LICENSE: "123456",
    }
}


# async def test_init_platform(hass: HomeAssistant) -> None:
#     """Test the initialization of the platform"""

#     result = await hass.config_entries.flow.async_init(
#         DOMAIN, context={"source": SOURCE_USER}
#     )
#     return


# @patch("kat_bulgaria.obligations.check_obligations")
# def check_obligations(person: KatPersonDetails, request_timeout: int = 5):
#     """Hello"""

#     return False


async def test_full_valid_config(hass: HomeAssistant) -> None:
    """Ensure everything starts correctly."""

    # entry = MockConfigEntry(
    #     domain=DOMAIN,
    #     title="Home",
    #     unique_id="0123456",
    #     data=VALID_CONFIG_FULL,
    #     options={},
    # )

    # with patch(
    #     "kat_bulgaria.obligations.check_obligations",
    #     return_value=False,
    # ):
    #     # entry.add_to_hass(hass)
    #     # assert await hass.config_entries.async_setup(entry.entry_id)
    #     # await hass.async_block_till_done()

    #     assert await async_setup_component(
    #         hass, BINARY_SENSOR_DOMAIN, VALID_CONFIG_FULL
    #     )
    #     await hass.async_block_till_done()
    #     print(hass.states.async_entity_ids())
    #     print(hass.states.get("binary_sensor.globi_nikola"))
    #     test = 5

    assert await async_setup_component(hass, BINARY_SENSOR_DOMAIN, VALID_CONFIG_FULL)
    # await hass.async_block_till_done()
    # print(hass.states.async_entity_ids())
    # print(hass.states.get("binary_sensor.globi_nikola"))
    # test = 5

    # test1 = hass.states.get("binary_sensor.globi_nikola")
    # assert hass.states.async_entity_ids_count() == 1


# async def test_valid_config(hass: HomeAssistant) -> None:
#     """Ensure everything starts correctly."""
#     res = await async_setup_component(hass, DOMAIN, VALID_CONFIG)
#     print(res)
#     await hass.async_block_till_done()
#     assert hass.states.async_entity_ids()[0] == "wololo"
#     assert hass.states.async_entity_ids_count() == 1


# async def test_invalid_egn_config(hass: HomeAssistant) -> None:
#     """Ensure EGN validation works."""
#     assert await async_setup_component(hass, BINARY_SENSOR_DOMAIN, INVALID_EGN_CONFIG)
#     await hass.async_block_till_done()

#     var = 5
#     # assert hass.states.async_entity_ids_count() == 0
#     # assert hass.states.async_entity_ids()[0] == "wololo"
#     # assert excinfo.value.args == ("Person(s) not registered ['Batman']")


# def test_invalid_egn_config2(hass: HomeAssistant) -> None:
#     """Ensure EGN validation works."""
#     assert setup_component(hass, BINARY_SENSOR_DOMAIN, INVALID_EGN_CONFIG)

#     var = 5
#     # assert hass.states.async_entity_ids_count() == 0
#     # assert hass.states.async_entity_ids()[0] == "wololo"
#     # assert excinfo.value.args == ("Person(s) not registered ['Batman']")
