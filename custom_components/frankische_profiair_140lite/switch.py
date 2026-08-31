"""Switches for FRÄNKISCHE profi-air 140 lite."""

from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import ProfiAirConfigEntry
from .entity import ProfiAirEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ProfiAirConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up profi-air switches."""
    coordinator = entry.runtime_data.coordinator
    async_add_entities(
        [
            ProfiAirPowerSwitch(coordinator),
            ProfiAirCalendarSwitch(coordinator),
        ]
    )


class _ProfiAirSwitch(ProfiAirEntity, SwitchEntity):
    """Base class for command switches."""

    async def _send(self, path: str, result_key: str, expected_value: int) -> None:
        await self.coordinator.async_send_command(path, result_key, expected_value)


class ProfiAirPowerSwitch(_ProfiAirSwitch):
    """Power control for the ventilation unit."""

    _attr_translation_key = "power"

    def __init__(self, coordinator) -> None:
        super().__init__(coordinator, "power")

    @property
    def is_on(self) -> bool:
        """Return whether the unit is powered on."""
        return self.result.get("ps") == 1

    async def async_turn_on(self, **kwargs) -> None:
        """Power on."""
        await self._send("power/on", "ps", 1)

    async def async_turn_off(self, **kwargs) -> None:
        """Power off."""
        await self._send("power/off", "ps", 0)


class ProfiAirCalendarSwitch(_ProfiAirSwitch):
    """Weekly calendar/program control."""

    _attr_translation_key = "calendar"

    def __init__(self, coordinator) -> None:
        super().__init__(coordinator, "calendar")

    @property
    def is_on(self) -> bool:
        """Return whether calendar mode is enabled."""
        return self.result.get("cm") == 1

    async def async_turn_on(self, **kwargs) -> None:
        """Enable calendar/program mode."""
        await self._send("set/calendar/on", "cm", 1)

    async def async_turn_off(self, **kwargs) -> None:
        """Disable calendar/program mode."""
        await self._send("set/calendar/off", "cm", 0)
