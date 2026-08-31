"""Local HTTP API client for FRÄNKISCHE profi-air 140 lite devices."""

from __future__ import annotations

import asyncio
from typing import Any

from aiohttp import ClientError, ClientResponseError, ClientSession

from .const import API_PREFIX


class ProfiAirApiError(Exception):
    """Base exception for profi-air API errors."""


class ProfiAirConnectionError(ProfiAirApiError):
    """Raised when the local device cannot be reached."""


class ProfiAirResponseError(ProfiAirApiError):
    """Raised when the device returns an invalid response."""


class ProfiAirApiClient:
    """Client for the local /api/v/1 API used by profi-air 140 lite."""

    def __init__(self, host: str, session: ClientSession) -> None:
        """Initialize the client."""
        self.host = self.normalize_host(host)
        self._session = session
        self._base_url = f"http://{self.host}{API_PREFIX}"

    @staticmethod
    def normalize_host(host: str) -> str:
        """Normalize a user-entered host or IP address."""
        value = host.strip()
        if value.startswith("http://"):
            value = value.removeprefix("http://")
        elif value.startswith("https://"):
            value = value.removeprefix("https://")
        return value.rstrip("/")

    async def async_get_status(self) -> dict[str, Any]:
        """Return current device status."""
        return await self._async_request("GET", "status")

    async def async_post(self, path: str) -> dict[str, Any]:
        """Send a control command to the device."""
        return await self._async_request("POST", path)

    async def _async_request(self, method: str, path: str) -> dict[str, Any]:
        """Perform an API request and validate the JSON response."""
        url = f"{self._base_url}/{path.lstrip('/')}"
        try:
            async with asyncio.timeout(10):
                response = await self._session.request(method, url)
                response.raise_for_status()
                data = await response.json(content_type=None)
        except (TimeoutError, ClientError, ClientResponseError) as err:
            raise ProfiAirConnectionError(f"Cannot reach {url}: {err}") from err
        except ValueError as err:
            raise ProfiAirResponseError(f"Invalid JSON response from {url}") from err

        if not isinstance(data, dict):
            raise ProfiAirResponseError(f"Unexpected response from {url}")
        if data.get("success") is not True:
            raise ProfiAirResponseError(
                f"Device rejected {method} {path}: {data.get('error', data)}"
            )
        return data
