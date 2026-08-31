"""Select controls for FRÄNKISCHE profi-air 140 lite."""

from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import ProfiAirConfigEntry
from .const import (
    FUNCTION_OPTION_TO_PATH,
    FUNCTION_VALUE_TO_OPTION,
    WORKING_MODE_OPTION_TO_PATH,
    WORKING_MODE_VALUE_TO_OPTION,
)
from .entity import ProfiAirEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ProfiAirConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up profi-air select entities."""
    coordinator = entry.runtime_data.coordinator
    async_add_entities(
        [
            ProfiAirFunctionSelect(coordinator),
            ProfiAirSeasonSelect(coordinator),
        ]
    )


class _ProfiAirSelect(ProfiAirEntity, SelectEntity):
    """Base select entity."""

    async def _send(self, path: str) -> None:
        await self.coordinator.client.async_post(path)
        await self.coordinator.async_request_refresh()


class ProfiAirFunctionSelect(_ProfiAirSelect):
    """Ventilation operating function."""

    _attr_translation_key = "function"
    _attr_options = list(FUNCTION_OPTION_TO_PATH)

    def __init__(self, coordinator) -> None:
        super().__init__(coordinator, "function")

    @property
    def current_option(self) -> str | None:
        """Return current function."""
        return FUNCTION_VALUE_TO_OPTION.get(self.result.get("fn"))

    async def async_select_option(self, option: str) -> None:
        """Select ventilation function."""
        await self._send(FUNCTION_OPTION_TO_PATH[option])


class ProfiAirSeasonSelect(_ProfiAirSelect):
    """Summer/winter working mode."""

    _attr_translation_key = "season"
    _attr_options = list(WORKING_MODE_OPTION_TO_PATH)

    def __init__(self, coordinator) -> None:
        super().__init__(coordinator, "season")

    @property
    def current_option(self) -> str | None:
        """Return current summer/winter mode."""
        return WORKING_MODE_VALUE_TO_OPTION.get(self.result.get("wm"))

    async def async_select_option(self, option: str) -> None:
        """Select summer/winter mode."""
        await self._send(WORKING_MODE_OPTION_TO_PATH[option])
