"""Diagnostics support for FRÄNKISCHE profi-air 140 lite."""

from __future__ import annotations

from typing import Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.core import HomeAssistant

from . import ProfiAirConfigEntry

TO_REDACT = {"UID", "serial", "ip", "sub", "gw", "pwd"}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ProfiAirConfigEntry
) -> dict[str, Any]:
    """Return redacted diagnostics for a config entry."""
    return {
        "entry": async_redact_data(dict(entry.data), {"host"}),
        "status": async_redact_data(entry.runtime_data.coordinator.data, TO_REDACT),
    }
