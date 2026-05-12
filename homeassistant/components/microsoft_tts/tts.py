"""Support for the Google speech service."""

from __future__ import annotations

import logging
from typing import Any

from pycsspeechtts import pycsspeechtts
from requests.exceptions import HTTPError

from homeassistant.components.tts import (
    CONF_LANG,
    Provider,
    TextToSpeechEntity,
    TtsAudioType,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_API_KEY, CONF_REGION, CONF_TYPE, PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.generated.microsoft_tts import SUPPORTED_LANGUAGES
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import (
    CONF_CONTOUR,
    CONF_GENDER,
    CONF_PITCH,
    CONF_RATE,
    CONF_VOLUME,
    DEFAULT_CONTOUR,
    DEFAULT_OUTPUT,
    DEFAULT_PITCH,
    DEFAULT_RATE,
    DEFAULT_VOLUME,
)

_LOGGER = logging.getLogger(__name__)


class MicrosoftProvider(Provider):
    """The Microsoft speech API provider."""

    def __init__(
        self, apikey, lang, gender, ttype, rate, volume, pitch, contour, region
    ) -> None:
        """Init Microsoft TTS service."""
        self._apikey: str = apikey
        self._lang: str = lang
        self._gender: str = gender
        self._type: str = ttype
        self._output: str = DEFAULT_OUTPUT
        self._rate: str = f"{rate}{PERCENTAGE}"
        self._volume: str = f"{volume}{PERCENTAGE}"
        self._pitch: str = pitch
        self._contour: str = contour
        self._region: str = region
        self.name = "Microsoft"

    @property
    def default_language(self) -> str | None:
        """Return the default language."""
        return self._lang

    @property
    def supported_languages(self) -> list[str]:
        """Return list of supported languages."""
        return list(SUPPORTED_LANGUAGES)

    @property
    def supported_options(self) -> list[str] | None:
        """Return list of supported options like voice, emotion."""
        return [CONF_GENDER, CONF_TYPE]

    @property
    def default_options(self) -> dict[str, Any] | None:
        """Return a dict include default options."""
        return {CONF_GENDER: self._gender, CONF_TYPE: self._type}

    def get_tts_audio(
        self, message: str, language: str, options: dict[str, Any]
    ) -> TtsAudioType:
        """Load TTS from Microsoft."""
        if language is None:
            language = self._lang

        try:
            trans = pycsspeechtts.TTSTranslator(self._apikey, self._region)
            data = trans.speak(
                language=language,
                gender=options[CONF_GENDER],
                voiceType=options[CONF_TYPE],
                output=self._output,
                rate=self._rate,
                volume=self._volume,
                pitch=self._pitch,
                contour=self._contour,
                text=message,
            )
        except HTTPError as ex:
            _LOGGER.error("Error occurred for Microsoft TTS: %s", ex)
            return (None, None)
        return ("mp3", data)


async def async_get_engine(
    hass: HomeAssistant,
    config: ConfigType,
    discovery_info: DiscoveryInfoType | None = None,
) -> MicrosoftProvider:
    """Set up Google speech component."""
    return MicrosoftProvider(
        config[CONF_API_KEY],
        config[CONF_LANG],
        config[CONF_GENDER],
        config[CONF_TYPE],
        config[CONF_RATE],
        config[CONF_VOLUME],
        config[CONF_PITCH],
        config[CONF_CONTOUR],
        config[CONF_REGION],
    )


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Google Translate speech platform via config entry."""
    default_language = config_entry.data[CONF_LANG]
    async_add_entities([MicrosoftTTSEntity(config_entry, default_language)])


class MicrosoftTTSEntity(TextToSpeechEntity):
    """The Microsoft speech API entity."""

    def __init__(self, config_entry: ConfigEntry, lang: str) -> None:
        """Init Google TTS service."""

        self._apikey = config_entry.data[CONF_API_KEY]
        self._lang = config_entry.data[CONF_LANG]

        self._attr_name = f"Microsoft TTS {self._lang}"
        self._attr_unique_id = config_entry.entry_id

    @property
    def default_language(self) -> str:
        """Return the default language."""
        return self._lang

    @property
    def supported_languages(self) -> list[str]:
        """Return list of supported languages."""
        return list(SUPPORTED_LANGUAGES)

    # @property
    # def supported_options(self) -> list[str]:
    #     """Return a list of supported options."""
    #     return SUPPORT_OPTIONS

    def get_tts_audio(
        self, message: str, language: str, options: dict[str, Any] | None = None
    ) -> TtsAudioType:
        """Load TTS from Microsoft."""
        if language is None:
            language = self._lang

        try:
            trans = pycsspeechtts.TTSTranslator(self._apikey, "uksouth")
            data = trans.speak(
                language="en-US",
                gender="Female",
                voiceType="JennyNeural",
                output=DEFAULT_OUTPUT,
                rate=DEFAULT_RATE,
                volume=DEFAULT_VOLUME,
                pitch=DEFAULT_PITCH,
                contour=DEFAULT_CONTOUR,
                text=message,
            )
        except HTTPError as ex:
            _LOGGER.error("Error occurred for Microsoft TTS: %s", ex)
            return (None, None)

        return ("mp3", data)
