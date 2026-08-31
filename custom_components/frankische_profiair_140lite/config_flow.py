"""Config flow for FRÄNKISCHE profi-air 140 lite."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import ProfiAirApiClient, ProfiAirApiError
from .const import DEFAULT_NAME, DOMAIN, SUPPORTED_DEVICE_TYPE


async def _validate_host(hass: HomeAssistant, host: str) -> dict[str, Any]:
    """Connect to the host and return validated device information."""
    client = ProfiAirApiClient(host, async_get_clientsession(hass))
    data = await client.async_get_status()

    if str(data.get("deviceType")) != SUPPORTED_DEVICE_TYPE:
        raise ValueError("unsupported_device")

    uid = str(data.get("UID", "")).strip()
    if not uid:
        raise ValueError("missing_uid")

    setup = data.get("setup", {}) if isinstance(data.get("setup"), dict) else {}
    return {
        "host": client.host,
        "uid": uid.lower(),
        "name": setup.get("name") or DEFAULT_NAME,
    }


class ProfiAirConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for FRÄNKISCHE profi-air 140 lite."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial setup step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                info = await _validate_host(self.hass, user_input[CONF_HOST])
            except ProfiAirApiError:
                errors["base"] = "cannot_connect"
            except ValueError:
                errors["base"] = "invalid_device"
            else:
                await self.async_set_unique_id(info["uid"])
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=info["name"],
                    data={CONF_HOST: info["host"]},
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required(CONF_HOST): str}),
            errors=errors,
        )
