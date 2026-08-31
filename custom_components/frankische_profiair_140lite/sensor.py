"""Sensors for FRÄNKISCHE profi-air 140 lite."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import PERCENTAGE, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import ProfiAirConfigEntry
from .entity import ProfiAirEntity


@dataclass(frozen=True, kw_only=True)
class ProfiAirSensorEntityDescription(SensorEntityDescription):
    """Describe a profi-air sensor."""

    value_fn: Callable[[dict[str, Any]], Any]


def _scaled(result: dict[str, Any], key: str, divisor: float) -> float | None:
    value = result.get(key)
    if value is None:
        return None
    try:
        return round(float(value) / divisor, 1)
    except (TypeError, ValueError):
        return None


SENSORS: tuple[ProfiAirSensorEntityDescription, ...] = (
    ProfiAirSensorEntityDescription(
        key="temperature",
        translation_key="temperature",
        value_fn=lambda result: _scaled(result, "ta", 10),
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ProfiAirSensorEntityDescription(
        key="humidity",
        translation_key="humidity",
        value_fn=lambda result: _scaled(result, "humidity", 10),
        device_class=SensorDeviceClass.HUMIDITY,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ProfiAirSensorEntityDescription(
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

    entity_description: ProfiAirSensorEntityDescription

    def __init__(
        self,
        coordinator,
        description: ProfiAirSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, description.key)
        self.entity_description = description

    @property
    def native_value(self) -> Any:
        """Return the current sensor value."""
        return self.entity_description.value_fn(self.result)
