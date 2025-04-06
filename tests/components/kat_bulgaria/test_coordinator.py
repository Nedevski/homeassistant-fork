"""Coordinator."""

import pytest

from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import HomeAssistant

from . import BULSTAT_VALID, EGN_VALID, LICENSE_VALID, PersonType

from tests.common import MockConfigEntry

# region Integration Setup


@pytest.mark.asyncio
async def test_coordinator_setup_individual(
    hass: HomeAssistant,
    config_entry_v2_individual: MockConfigEntry,
    mock_get_obligations_ok_nodata,
) -> None:
    """Test that the coordinator can update."""
    assert config_entry_v2_individual.state == ConfigEntryState.NOT_LOADED
    config_entry_v2_individual.add_to_hass(hass)

    result = await hass.config_entries.async_setup(config_entry_v2_individual.entry_id)
    await hass.async_block_till_done()

    assert result is True
    assert config_entry_v2_individual.state == ConfigEntryState.LOADED

    coordinator = config_entry_v2_individual.runtime_data
    assert coordinator
    assert coordinator.client.person_type == PersonType.INDIVIDUAL
    assert coordinator.client.person_egn == EGN_VALID
    assert coordinator.client.person_document_number == LICENSE_VALID
    assert coordinator.client.bulstat is None

    assert coordinator.client.get_obligations.call_count == 1


@pytest.mark.asyncio
async def test_coordinator_setup_business(
    hass: HomeAssistant,
    config_entry_v2_business: MockConfigEntry,
    mock_get_obligations_ok_nodata,
) -> None:
    """Test that the coordinator can update."""
    assert config_entry_v2_business.state == ConfigEntryState.NOT_LOADED
    config_entry_v2_business.add_to_hass(hass)

    result = await hass.config_entries.async_setup(config_entry_v2_business.entry_id)
    await hass.async_block_till_done()

    assert result is True
    assert config_entry_v2_business.state == ConfigEntryState.LOADED

    coordinator = config_entry_v2_business.runtime_data
    assert coordinator
    assert coordinator.client.person_type == PersonType.BUSINESS
    assert coordinator.client.person_egn == EGN_VALID
    assert coordinator.client.person_document_number == LICENSE_VALID
    assert coordinator.client.bulstat == BULSTAT_VALID

    assert coordinator.client.get_obligations.call_count == 1


# @pytest.mark.asyncio
# async def test_coordinator_update_ok_nodata(
#     hass: HomeAssistant,
#     config_entry_v2_individual: MockConfigEntry,
#     mock_get_obligations_ok_nodata,
# ) -> None:
#     """Test that the coordinator can update."""
#     # find coordinator, test if katclient is the correct type


#     assert config_entry_v2_individual.state == ConfigEntryState.NOT_LOADED
#     await integration_setup_v2_individual(client_fine_served_individual)
#     assert config_entry_v2_individual.state == ConfigEntryState.LOADED
#     assert client_fine_served_individual.get_obligations.call_count == 1
#     assert client_fine_served_individual.get_obligations.call_args[0] == (
#         EGN_VALID,
#         LICENSE_VALID,
#     )

# async def test_coordinator_usernotfoundonline(
#     config_entry_v2_individual: MockConfigEntry,
#     integration_setup_v2_individual: Callable[[MagicMock], Awaitable[bool]],
#     client_ok_individual: MagicMock,
#     katclient_get_obligations_usernotfoundonline,
# ) -> None:
#     """Test that the coordinator can update."""
#     assert config_entry_v2_individual.state == ConfigEntryState.NOT_LOADED
#     await integration_setup_v2_individual(client_ok_individual)
#     assert config_entry_v2_individual.state == ConfigEntryState.SETUP_ERROR


# async def test_coordinator_api_timeout(
#     config_entry_v2_individual: MockConfigEntry,
#     integration_setup_v2_individual: Callable[[MagicMock], Awaitable[bool]],
#     client_ok_individual: MagicMock,
#     katclient_get_obligations_api_timeout,
# ) -> None:
#     """Test that the coordinator can update."""
#     assert config_entry_v2_individual.state == ConfigEntryState.NOT_LOADED
#     await integration_setup_v2_individual(client_ok_individual)
#     assert config_entry_v2_individual.state == ConfigEntryState.SETUP_RETRY


# async def test_coordinator_api_toomanyrequests(
#     config_entry_v2_individual: MockConfigEntry,
#     integration_setup_v2_individual: Callable[[MagicMock], Awaitable[bool]],
#     client_ok_individual: MagicMock,
#     katclient_get_obligations_api_toomanyrequests,
# ) -> None:
#     """Test that the coordinator can update."""
#     assert config_entry_v2_individual.state == ConfigEntryState.NOT_LOADED
#     await integration_setup_v2_individual(client_ok_individual)
#     assert config_entry_v2_individual.state == ConfigEntryState.SETUP_RETRY


# async def test_coordinator_api_invaliddata(
#     config_entry_v2_individual: MockConfigEntry,
#     integration_setup_v2_individual: Callable[[MagicMock], Awaitable[bool]],
#     client_ok_individual: MagicMock,
#     katclient_get_obligations_api_errorreadingdata,
# ) -> None:
#     """Test that the coordinator can update."""
#     assert config_entry_v2_individual.state == ConfigEntryState.NOT_LOADED
#     await integration_setup_v2_individual(client_ok_individual)
#     assert config_entry_v2_individual.state == ConfigEntryState.SETUP_RETRY


# async def test_coordinator_api_invalidschema(
#     config_entry_v2_individual: MockConfigEntry,
#     integration_setup_v2_individual: Callable[[MagicMock], Awaitable[bool]],
#     client_ok_individual: MagicMock,
#     katclient_get_obligations_api_invalidschema,
# ) -> None:
#     """Test that the coordinator can update."""
#     assert config_entry_v2_individual.state == ConfigEntryState.NOT_LOADED
#     await integration_setup_v2_individual(client_ok_individual)
#     assert config_entry_v2_individual.state == ConfigEntryState.SETUP_RETRY


# async def test_coordinator_api_unknownerror(
#     config_entry_v2_individual: MockConfigEntry,
#     integration_setup_v2_individual: Callable[[MagicMock], Awaitable[bool]],
#     client_ok_individual: MagicMock,
#     katclient_get_obligations_api_unknownerror,
# ) -> None:
#     """Test that the coordinator can update."""
#     assert config_entry_v2_individual.state == ConfigEntryState.NOT_LOADED
#     await integration_setup_v2_individual(client_ok_individual)
#     assert config_entry_v2_individual.state == ConfigEntryState.SETUP_RETRY


# # endregion


# # region Fetch data


# async def test_coordinator_update(
#     config_entry_v2_individual: MockConfigEntry,
#     integration_setup_v2_individual: Callable[[MagicMock], Awaitable[bool]],
#     client_fine_served_individual: MagicMock,
#     katclient_get_obligations_success_none,
# ) -> None:
#     """Test that the coordinator can update."""
#     assert config_entry_v2_individual.state == ConfigEntryState.NOT_LOADED
#     await integration_setup_v2_individual(client_fine_served_individual)
#     assert config_entry_v2_individual.state == ConfigEntryState.LOADED
#     assert client_fine_served_individual.get_obligations.call_count == 1
#     assert client_fine_served_individual.get_obligations.call_args[0] == (
#         EGN_VALID,
#         LICENSE_VALID,
#     )


# # endregion
