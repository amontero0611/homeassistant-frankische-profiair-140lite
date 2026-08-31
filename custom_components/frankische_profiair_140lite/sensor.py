"""Sensors for FRÄNKISCHE profi-air 140 lite."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorStateClass
from homeassistant.const import PERCENTAGE, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import ProfiAirConfigEntry
from .entity import ProfiAirEntity


@dataclass(frozen=True, kw_only=True)
class ProfiAirSensorDescription:
    """Description of a profi-air sensor."""

    key: str
    translation_key: str
    value_fn: Callable[[dict[str, Any]], Any]
    device_class: SensorDeviceClass | None = None
    native_unit_of_measurement: str | None = None
    state_class: SensorStateClass | None = None


def _scaled(result: dict[str, Any], key: str, divisor: float) -> float | None:
    value = result.get(key)
    if value is None:
        return None
    try:
        return round(float(value) / divisor, 1)
    except (TypeError, ValueError):
        return None


SENSORS = (
    ProfiAirSensorDescription(
        key="temperature",
        translation_key="temperature",
        value_fn=lambda result: _scaled(result, "ta", 10),
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ProfiAirSensorDescription(
        key="humidity",
        translation_key="humidity",
        value_fn=lambda result: _scaled(result, "humidity", 10),
        device_class=SensorDeviceClass.HUMIDITY,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ProfiAirSensorDescription(
        key="air_quality",
        translation_key="air_quality",
        value_fn=lambda result: result.get("airQuality"),
        state_class=SensorStateClass.MEASUREMENT,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ProfiAirConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up profi-air sensors."""
    coordinator = entry.runtime_data.coordinator
    async_add_entities(ProfiAirSensor(coordinator, description) for description in SENSORS)


class ProfiAirSensor(ProfiAirEntity, SensorEntity):
    """Representation of a profi-air sensor."""

    def __init__(self, coordinator, description: ProfiAirSensorDescription) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, description.key)
        self.entity_description = description
        self._attr_translation_key = description.translation_key
        self._attr_device_class = description.device_class
        self._attr_native_unit_of_measurement = description.native_unit_of_measurement
        self._attr_state_class = description.state_class

    @property
    def native_value(self) -> Any:
        """Return the current sensor value."""
        return self.entity_description.value_fn(self.result)
