"""Config flow for Google Translate text-to-speech integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.components.tts import (
    CONF_LANG,
    PLATFORM_SCHEMA as TTS_PLATFORM_SCHEMA,
)
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_API_KEY, CONF_REGION, CONF_TYPE
from homeassistant.generated.microsoft_tts import SUPPORTED_LANGUAGES
from homeassistant.helpers import config_validation as cv

from .const import (
    CONF_CONTOUR,
    CONF_GENDER,
    CONF_PITCH,
    CONF_RATE,
    CONF_VOLUME,
    DEFAULT_CONTOUR,
    DEFAULT_GENDER,
    DEFAULT_LANG,
    DEFAULT_PITCH,
    DEFAULT_RATE,
    DEFAULT_REGION,
    DEFAULT_TYPE,
    DEFAULT_VOLUME,
    DOMAIN,
    GENDERS,
)

_LOGGER = logging.getLogger(__name__)


PLATFORM_SCHEMA2 = TTS_PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_API_KEY): cv.string,
        vol.Optional(CONF_LANG, default=DEFAULT_LANG): vol.In(SUPPORTED_LANGUAGES),
        vol.Optional(CONF_GENDER, default=DEFAULT_GENDER): vol.In(GENDERS),
        vol.Optional(CONF_TYPE, default=DEFAULT_TYPE): cv.string,
        vol.Optional(CONF_RATE, default=DEFAULT_RATE): vol.All(
            vol.Coerce(int), vol.Range(-100, 100)
        ),
        vol.Optional(CONF_VOLUME, default=DEFAULT_VOLUME): vol.All(
            vol.Coerce(int), vol.Range(-100, 100)
        ),
        vol.Optional(CONF_PITCH, default=DEFAULT_PITCH): cv.string,
        vol.Optional(CONF_CONTOUR, default=DEFAULT_CONTOUR): cv.string,
        vol.Optional(CONF_REGION, default=DEFAULT_REGION): cv.string,
    }
)

PLATFORM_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_API_KEY): cv.string,
        vol.Optional(CONF_LANG, default=DEFAULT_LANG): vol.In(SUPPORTED_LANGUAGES),
        vol.Optional(CONF_GENDER, default=DEFAULT_GENDER): vol.In(GENDERS),
        vol.Optional(CONF_TYPE, default=DEFAULT_TYPE): cv.string,
        vol.Optional(CONF_RATE, default=DEFAULT_RATE): vol.All(
            vol.Coerce(int), vol.Range(0, 100)
        ),
        vol.Optional(CONF_VOLUME, default=DEFAULT_VOLUME): vol.All(
            vol.Coerce(int), vol.Range(0, 100)
        ),
        vol.Optional(CONF_PITCH, default=DEFAULT_PITCH): cv.string,
        vol.Optional(CONF_CONTOUR, default=DEFAULT_CONTOUR): cv.string,
        vol.Optional(CONF_REGION, default=DEFAULT_REGION): cv.string,
    }
)


class MicrosoftTextToSpeechConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Google Translate text-to-speech."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        if user_input is not None:
            # self._async_abort_entries_match(
            #     {
            #         CONF_LANG: user_input[CONF_LANG],
            #         CONF_TLD: user_input[CONF_TLD],
            #     }
            # )
            return self.async_create_entry(
                title="Microsoft TTS "
                + user_input[CONF_LANG]
                + " "
                + user_input[CONF_GENDER],
                data=user_input,
            )

        return self.async_show_form(step_id="user", data_schema=PLATFORM_SCHEMA)
