"""Test KAT Bulgaria reconfigure flow."""

from unittest.mock import AsyncMock, patch

from kat_bulgaria.errors import KatError, KatErrorSubtype, KatErrorType
import pytest

from homeassistant.components.kat_bulgaria import const as kat_constants
from homeassistant.components.kat_bulgaria.config_flow import STEP_ID_RECONFIGURE
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType

from . import (
    CONF_BULSTAT,
    CONF_DOCUMENT_NUMBER,
    CONF_DOCUMENT_TYPE,
    CONF_PERSON_EGN,
    CONF_PERSON_TYPE,
    EGN_VALID,
    GOV_ID_INVALID,
    LICENSE_VALID,
    PersonalDocumentType,
    PersonType,
)

from tests.common import MockConfigEntry

ABORT_RECONFIGURE_SUCCESSFUL = "reconfigure_successful"

UPDATED_LICENSE = "999888777"
UPDATED_GOV_ID = "AA9998888"


@pytest.mark.asyncio
async def test_reconfigure_flow_individual_update_license_ok(
    hass: HomeAssistant,
    config_entry_v2_individual: MockConfigEntry,
    mock_get_obligations_ok_nodata,
) -> None:
    """Test reconfigure flow."""

    config_entry_v2_individual.add_to_hass(hass)

    reconfigure_flow = await hass.config_entries.flow.async_init(
        kat_constants.DOMAIN,
        context={
            "source": STEP_ID_RECONFIGURE,
            "entry_id": config_entry_v2_individual.entry_id,
        },
        data={
            CONF_DOCUMENT_TYPE: PersonalDocumentType.DRIVING_LICENSE,
            CONF_DOCUMENT_NUMBER: UPDATED_LICENSE,
        },
    )
    await hass.async_block_till_done()

    assert reconfigure_flow["type"] is FlowResultType.ABORT
    assert reconfigure_flow["reason"] == ABORT_RECONFIGURE_SUCCESSFUL

    config = config_entry_v2_individual.data

    assert config
    assert config.get(CONF_DOCUMENT_TYPE) == PersonalDocumentType.DRIVING_LICENSE
    assert config.get(CONF_DOCUMENT_NUMBER) == UPDATED_LICENSE
    assert config.get(CONF_PERSON_TYPE) == PersonType.INDIVIDUAL
    assert config.get(CONF_PERSON_EGN) == EGN_VALID
    assert config.get(CONF_BULSTAT) is None


@pytest.mark.asyncio
async def test_reconfigure_flow_individual_update_license_to_gov_id_ok(
    hass: HomeAssistant,
    config_entry_v2_individual: MockConfigEntry,
    mock_get_obligations_ok_nodata,
) -> None:
    """Test reconfigure flow."""

    config_entry_v2_individual.add_to_hass(hass)

    reconfigure_flow = await hass.config_entries.flow.async_init(
        kat_constants.DOMAIN,
        context={
            "source": STEP_ID_RECONFIGURE,
            "entry_id": config_entry_v2_individual.entry_id,
        },
        data={
            CONF_DOCUMENT_TYPE: PersonalDocumentType.NATIONAL_ID,
            CONF_DOCUMENT_NUMBER: UPDATED_GOV_ID,
        },
    )
    await hass.async_block_till_done()

    assert reconfigure_flow["type"] is FlowResultType.ABORT
    assert reconfigure_flow["reason"] == ABORT_RECONFIGURE_SUCCESSFUL

    config = config_entry_v2_individual.data

    assert config
    assert config.get(CONF_DOCUMENT_TYPE) == PersonalDocumentType.NATIONAL_ID
    assert config.get(CONF_DOCUMENT_NUMBER) == UPDATED_GOV_ID
    assert config.get(CONF_PERSON_TYPE) == PersonType.INDIVIDUAL
    assert config.get(CONF_PERSON_EGN) == EGN_VALID
    assert config.get(CONF_BULSTAT) is None


@pytest.mark.asyncio
@patch(
    "homeassistant.components.kat_bulgaria.kat_client.KatClient.validate_credentials",
    AsyncMock(
        side_effect=KatError(
            KatErrorType.VALIDATION_ERROR,
            KatErrorSubtype.VALIDATION_DRIVING_LICENSE_INVALID,
            "error text",
        )
    ),
)
async def test_reconfigure_flow_individual_update_license_invalid(
    hass: HomeAssistant,
    config_entry_v2_individual: MockConfigEntry,
    mock_get_obligations_ok_nodata,
) -> None:
    """Test reconfigure flow."""

    config_entry_v2_individual.add_to_hass(hass)

    reconfigure_flow = await hass.config_entries.flow.async_init(
        kat_constants.DOMAIN,
        context={
            "source": STEP_ID_RECONFIGURE,
            "entry_id": config_entry_v2_individual.entry_id,
        },
        data={
            CONF_DOCUMENT_TYPE: PersonalDocumentType.DRIVING_LICENSE,
            CONF_DOCUMENT_NUMBER: UPDATED_LICENSE,
        },
    )
    await hass.async_block_till_done()

    assert reconfigure_flow["type"] is FlowResultType.FORM
    assert reconfigure_flow["errors"] == {"base": "invalid_config"}

    config = config_entry_v2_individual.data

    # unchanged
    assert config
    assert config.get(CONF_DOCUMENT_TYPE) == PersonalDocumentType.DRIVING_LICENSE
    assert config.get(CONF_DOCUMENT_NUMBER) == LICENSE_VALID
    assert config.get(CONF_PERSON_TYPE) == PersonType.INDIVIDUAL
    assert config.get(CONF_PERSON_EGN) == EGN_VALID
    assert config.get(CONF_BULSTAT) is None


@pytest.mark.asyncio
@patch(
    "homeassistant.components.kat_bulgaria.kat_client.KatClient.validate_credentials",
    AsyncMock(
        side_effect=KatError(
            KatErrorType.VALIDATION_ERROR,
            KatErrorSubtype.VALIDATION_GOV_ID_NUMBER_INVALID,
            "error text",
        )
    ),
)
async def test_reconfigure_flow_individual_update_gov_id_invalid(
    hass: HomeAssistant,
    config_entry_v2_individual: MockConfigEntry,
    mock_get_obligations_ok_nodata,
) -> None:
    """Test reconfigure flow."""

    config_entry_v2_individual.add_to_hass(hass)

    reconfigure_flow = await hass.config_entries.flow.async_init(
        kat_constants.DOMAIN,
        context={
            "source": STEP_ID_RECONFIGURE,
            "entry_id": config_entry_v2_individual.entry_id,
        },
        data={
            CONF_DOCUMENT_TYPE: PersonalDocumentType.NATIONAL_ID,
            CONF_DOCUMENT_NUMBER: GOV_ID_INVALID,
        },
    )
    await hass.async_block_till_done()

    assert reconfigure_flow["type"] is FlowResultType.FORM
    assert reconfigure_flow["errors"] == {"base": "invalid_config"}

    config = config_entry_v2_individual.data

    # unchanged
    assert config
    assert config.get(CONF_DOCUMENT_TYPE) == PersonalDocumentType.DRIVING_LICENSE
    assert config.get(CONF_DOCUMENT_NUMBER) == LICENSE_VALID
    assert config.get(CONF_PERSON_TYPE) == PersonType.INDIVIDUAL
    assert config.get(CONF_PERSON_EGN) == EGN_VALID
    assert config.get(CONF_BULSTAT) is None
