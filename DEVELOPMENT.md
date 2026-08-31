# Development notes

## Reverse-engineered status fields

Observed status payload under `RESULT`:

| Field | Observed meaning |
|---|---|
| `ps` | Power state (`1` on, `0` off) |
| `cm` | Calendar/program state (`1` enabled, `0` disabled) |
| `fn` | Function: `1` Auto, `2` Night, `3` Minimum, `4` Maximum |
| `wm` | Working mode: `3` heating/winter, `5` cooling/summer |
| `ta` | Temperature, tenths of °C |
| `humidity` | Humidity, tenths of % |
| `airQuality` | Air-quality value used by the official app |

The official app calculates a display category from air quality approximately as `round(airQuality / 100)`. Until the physical meaning/unit is documented, the integration exposes the raw value.

## Next useful features

- Reconfigure flow when DHCP changes the IP address.
- DHCP/mDNS discovery if a reliable discovery signature can be identified.
- Alarm sensor from `RESULT.a`.
- Diagnostics for cloud connection and controller state.
- Optional sensors for firmware/uptime.
- Weekly schedule read/write support.
- Tests for config flow and API parsing.
