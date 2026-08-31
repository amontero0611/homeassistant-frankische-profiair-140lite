"""Constants for the FRÄNKISCHE profi-air 140 lite integration."""

from datetime import timedelta

from homeassistant.const import Platform

DOMAIN = "frankische_profiair_140lite"

DEFAULT_NAME = "FRÄNKISCHE profi-air 140 lite"
DEFAULT_SCAN_INTERVAL = timedelta(seconds=30)
COMMAND_CONFIRM_INTERVAL = 1.0
COMMAND_CONFIRM_ATTEMPTS = 6
API_PREFIX = "/api/v/1"
SUPPORTED_DEVICE_TYPE = "002"

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.SWITCH, Platform.SELECT]

FUNCTION_AUTO = 1
FUNCTION_NIGHT = 2
FUNCTION_MINIMUM = 3
FUNCTION_MAXIMUM = 4

FUNCTION_VALUE_TO_OPTION = {
    FUNCTION_AUTO: "auto",
    FUNCTION_NIGHT: "night",
    FUNCTION_MINIMUM: "minimum",
    FUNCTION_MAXIMUM: "maximum",
}
FUNCTION_OPTION_TO_PATH = {
    "auto": "set/function/auto",
    "night": "set/function/night",
    "minimum": "set/function/min",
    "maximum": "set/function/max",
}

WORKING_MODE_WINTER = 3
WORKING_MODE_SUMMER = 5

WORKING_MODE_VALUE_TO_OPTION = {
    WORKING_MODE_WINTER: "winter",
    WORKING_MODE_SUMMER: "summer",
}
WORKING_MODE_OPTION_TO_PATH = {
    "winter": "set/mode/heating",
    "summer": "set/mode/cooling",
}
