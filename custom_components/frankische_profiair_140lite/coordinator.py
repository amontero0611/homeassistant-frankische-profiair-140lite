"""Data coordinator for FRÄNKISCHE profi-air 140 lite."""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import ProfiAirApiClient, ProfiAirApiError
from .const import (
    COMMAND_CONFIRM_ATTEMPTS,
    COMMAND_CONFIRM_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


class ProfiAirCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinate polling of a single profi-air device."""

    def __init__(self, hass: HomeAssistant, client: ProfiAirApiClient) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=DEFAULT_SCAN_INTERVAL,
        )
        self.client = client


    async def async_send_command(
        self, path: str, result_key: str, expected_value: Any
    ) -> None:
        """Send a command and wait until the device reports the new state.

        The profi-air controller acknowledges POST requests immediately, but its
        status endpoint can take a few seconds to expose the consolidated RESULT.
        Keep the last valid coordinator data during that window instead of
        replacing entity state with temporary unknown/off values.
        """
        await self.client.async_post(path)

        for _ in range(COMMAND_CONFIRM_ATTEMPTS):
            await asyncio.sleep(COMMAND_CONFIRM_INTERVAL)
            try:
                data = await self.client.async_get_status()
            except ProfiAirApiError:
                continue

            result = data.get("RESULT")
            if not isinstance(result, dict):
                continue

            if result.get(result_key) == expected_value:
                self.async_set_updated_data(data)
                return

        _LOGGER.warning(
            "Command %s was accepted but the expected %s=%r was not confirmed "
            "within %.1f seconds",
            path,
            result_key,
            expected_value,
            COMMAND_CONFIRM_ATTEMPTS * COMMAND_CONFIRM_INTERVAL,
        )
        await self.async_request_refresh()

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch current status from the unit."""
        try:
            return await self.client.async_get_status()
        except ProfiAirApiError as err:
            raise UpdateFailed(str(err)) from err
