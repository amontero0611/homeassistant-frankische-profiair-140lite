"""Data coordinator for FRÄNKISCHE profi-air 140 lite."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import ProfiAirApiClient, ProfiAirApiError
from .const import DEFAULT_SCAN_INTERVAL, DOMAIN

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

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch current status from the unit."""
        try:
            return await self.client.async_get_status()
        except ProfiAirApiError as err:
            raise UpdateFailed(str(err)) from err
