"""Config flow for Athletic Fitness BG integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import (
    ConfigFlow as ConfigEntriesFlow,
    ConfigFlowResult,
)
from homeassistant.helpers.selector import (
    SelectOptionDict,
    SelectSelector,
    SelectSelectorConfig,
)

from .athletic_api_client import (
    AthleticApiClient,
    AthleticApiClientAuthError,
    AthleticApiClientError,
)
from .const import DOMAIN
from .models import GymDetails

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("email"): str,
        vol.Required("password"): str,
    }
)


class ConfigFlow(ConfigEntriesFlow, domain=DOMAIN):
    """Handle a config flow for Athletic Fitness BG."""

    VERSION = 1

    def __init__(self, *args, **kwargs) -> None:
        """Initialize the config flow."""
        super().__init__(*args, **kwargs)
        self._user_data: dict[str, Any] = {}
        self._available_gyms: dict[int, GymDetails] = {}

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                await self._test_credentials(
                    user_input["email"], user_input["password"]
                )
            except AthleticApiClientAuthError:
                errors["base"] = "invalid_auth"
            except AthleticApiClientError:
                errors["base"] = "cannot_connect"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                # Store user data and proceed to location selection
                self._user_data = user_input
                return await self.async_step_location()

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )

    async def async_step_location(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the location selection step."""
        if user_input is not None:
            selected_gym_ids = [int(gid) for gid in user_input["gym_ids"]]
            selected_gyms = [
                self._available_gyms[gym_id] for gym_id in selected_gym_ids
            ]

            config_data = {
                **self._user_data,
                "gyms": [
                    {"gym_id": gym.gym_id, "gym_name": gym.gym_name, "city": gym.city}
                    for gym in selected_gyms
                ],
            }

            # Single-instance integration uses a static unique ID
            await self.async_set_unique_id(DOMAIN)
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title="Athletic Fitness",
                data=config_data,
            )

        # Fetch available gyms
        client = AthleticApiClient(self.hass)
        try:
            gyms = await client.get_gyms()
        except AthleticApiClientError as err:
            _LOGGER.error("Error fetching gyms: %s", err)
            return self.async_show_form(
                step_id="location",
                data_schema=vol.Schema({}),
                errors={"base": "cannot_fetch_gyms"},
            )

        self._available_gyms = {
            gym["gymId"]: GymDetails(
                gym_id=gym["gymId"], gym_name=gym["gymName"], city=gym.get("city", "")
            )
            for gym in gyms
        }

        # Create dynamic schema with gym options
        options: list[SelectOptionDict] = [
            SelectOptionDict(
                value=str(gym.gym_id), label=f"{gym.city} - {gym.gym_name}"
            )
            for gym in self._available_gyms.values()
        ]
        location_schema = vol.Schema(
            {
                vol.Required("gym_ids", default=[]): SelectSelector(
                    SelectSelectorConfig(
                        options=options,
                        multiple=True,
                        translation_key="gym_ids",
                    )
                ),
            }
        )

        return self.async_show_form(
            step_id="location",
            data_schema=location_schema,
        )

    async def _test_credentials(self, email: str, password: str) -> None:
        """Test if the provided credentials are valid."""
        client = AthleticApiClient(self.hass)
        await client.authenticate(email, password)
