"""FRÄNKISCHE profi-air 140 lite local integration."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import ProfiAirApiClient
from .const import PLATFORMS
from .coordinator import ProfiAirCoordinator


@dataclass
class ProfiAirRuntimeData:
    """Runtime data for a config entry."""

    client: ProfiAirApiClient
    coordinator: ProfiAirCoordinator


type ProfiAirConfigEntry = ConfigEntry[ProfiAirRuntimeData]


async def async_setup_entry(
    hass: HomeAssistant, entry: ProfiAirConfigEntry
) -> bool:
    """Set up FRÄNKISCHE profi-air from a config entry."""
    session = async_get_clientsession(hass)
    client = ProfiAirApiClient(entry.data[CONF_HOST], session)
    coordinator = ProfiAirCoordinator(hass, client)

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = ProfiAirRuntimeData(
        client=client,
        coordinator=coordinator,
    )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(
    hass: HomeAssistant, entry: ProfiAirConfigEntry
) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
