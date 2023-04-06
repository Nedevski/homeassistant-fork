"""Options flow for KAT Bulgaria integration."""
from __future__ import annotations

import logging
from typing import Any

from kat_bulgaria.obligations import KatApi, KatError, KatErrorType
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .common import generate_entity_name
from .const import CONF_DRIVING_LICENSE, CONF_PERSON_EGN, CONF_PERSON_NAME

_LOGGER = logging.getLogger(__name__)


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Options flow handler."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""

        self.config_entry = config_entry
        self.options = dict(config_entry.options)

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""

        # On options form open
        if user_input is None:
            data_schema = vol.Schema(
                {
                    vol.Required(
                        CONF_PERSON_EGN,
                        description="EGN",
                        default=self.config_entry.data.get(CONF_PERSON_EGN),
                    ): str,
                    vol.Required(
                        CONF_DRIVING_LICENSE,
                        description="Driving License",
                        default=self.config_entry.data.get(CONF_DRIVING_LICENSE),
                    ): str,
                }
            )

            return self.async_show_form(step_id="init", data_schema=data_schema)

        # If user entered data in the form
        user_name = str(self.config_entry.data.get(CONF_PERSON_NAME))
        # user_egn = str(self.config_entry.data.get(CONF_PERSON_EGN))

        new_user_egn = user_input[CONF_DRIVING_LICENSE]
        new_user_driving_license = user_input[CONF_DRIVING_LICENSE]

        try:
            # Verify user creds
            verify = await KatApi().async_verify_credentials(
                new_user_egn, new_user_driving_license
            )

            if not verify.success:
                if verify.error_type == KatErrorType.VALIDATION_ERROR:
                    return self.async_abort(reason="invalid_config")

                if verify.error_type in (
                    KatErrorType.VALIDATION_ERROR,
                    KatErrorType.TIMEOUT,
                ):
                    return self.async_abort(reason="cannot_connect")

                return self.async_abort(reason="unknown")
        except KatError as ex:
            _LOGGER.exception(str(ex))
            return self.async_abort(reason="unknown")

        # Success!
        return self.async_create_entry(
            title=generate_entity_name(user_name),
            data={
                CONF_PERSON_NAME: user_name,
                CONF_PERSON_EGN: new_user_egn,
                CONF_DRIVING_LICENSE: new_user_driving_license,
            },
        )
