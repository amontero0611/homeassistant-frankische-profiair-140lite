"""Shared entity helpers for FRÄNKISCHE profi-air 140 lite."""

from __future__ import annotations

from typing import Any

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DEFAULT_NAME, DOMAIN
from .coordinator import ProfiAirCoordinator


class ProfiAirEntity(CoordinatorEntity[ProfiAirCoordinator]):
    """Base entity for a profi-air unit."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: ProfiAirCoordinator, key: str) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        self._key = key
        self._attr_unique_id = f"{self.device_uid}_{key}"

        data = coordinator.data
        setup = data.get("setup", {}) if isinstance(data.get("setup"), dict) else {}
        sw = data.get("sw", {}) if isinstance(data.get("sw"), dict) else {}
        device_type = data.get("deviceType", "unknown")

        # Set this as an entity attribute rather than a dynamic property so the
        # device registry can reliably associate every platform entity with the
        # same physical ventilation unit.
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self.device_uid)},
            manufacturer="FRÄNKISCHE",
            model=f"profi-air 140 lite (deviceType {device_type})",
            name=setup.get("name") or DEFAULT_NAME,
            serial_number=setup.get("serial"),
            sw_version=sw.get("V"),
        )

    @property
    def device_uid(self) -> str:
        """Return stable device UID."""
        uid = str(self.coordinator.data.get("UID", "unknown"))
        return uid.lower().replace(":", "")

    @property
    def result(self) -> dict[str, Any]:
        """Return the RESULT section of device status."""
        result = self.coordinator.data.get("RESULT", {})
        return result if isinstance(result, dict) else {}
