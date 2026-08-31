# FRÄNKISCHE profi-air 140 lite for Home Assistant

Unofficial Home Assistant custom integration for **FRÄNKISCHE profi-air 140 lite** ventilation units using the controller's **local HTTP API**.

> This project is not affiliated with or endorsed by FRÄNKISCHE Rohrwerke. FRÄNKISCHE and profi-air are trademarks of their respective owner.

## Status

Early development / test release (`0.1.0`). Initial development is based on a **profi-air 140 lite**, API `deviceType: 002`, observed with controller firmware `11.0.3`.

The local controller exposes:

```text
http://<device-ip>/api/v/1/status
```

No cloud credentials are required.

## Entities in 0.1.0

- Temperature
- Humidity
- Air quality (raw value reported by the controller)
- Power on/off
- Weekly program on/off
- Ventilation mode: Auto / Night / Minimum / Maximum
- Season: Summer / Winter

## Known local API commands

The integration uses API routes observed in the official `profi-air smart control` Android application:

```text
GET  /api/v/1/status
POST /api/v/1/power/on
POST /api/v/1/power/off
POST /api/v/1/set/function/auto
POST /api/v/1/set/function/night
POST /api/v/1/set/function/min
POST /api/v/1/set/function/max
POST /api/v/1/set/mode/heating
POST /api/v/1/set/mode/cooling
POST /api/v/1/set/calendar/on
POST /api/v/1/set/calendar/off
```

For the ventilation unit, the app maps working mode values `3` and `5` to winter/heating and summer/cooling respectively.

## Installation for development

### HACS custom repository

1. Push this repository to your GitHub account.
2. Replace every `YOUR_GITHUB_USERNAME` in `manifest.json` with your GitHub username.
3. In HACS, add the repository URL as a **Custom repository**, category **Integration**.
4. Install **FRÄNKISCHE profi-air 140 lite**.
5. Restart Home Assistant.
6. Go to **Settings → Devices & services → Add integration** and search for **FRÄNKISCHE profi-air 140 lite**.
7. Enter the controller's local IP address or hostname.

### Manual installation

Copy:

```text
custom_components/frankische_profiair_140lite
```

to:

```text
/config/custom_components/frankische_profiair_140lite
```

and restart Home Assistant.

## Before testing control commands

The read path (`/status`) has been confirmed on a profi-air 140 lite. Control paths were recovered from the official app and should be tested carefully on the first physical unit.

Suggested first test sequence:

1. Add the integration and verify that temperature/humidity values match the official app.
2. Use **Minimum** / **Maximum** while standing near the unit and confirm the expected airflow change.
3. Test **Weekly program** on/off.
4. Test **Summer/Winter** only after confirming what those modes mean in your installation.
5. Test device power last.

## Device identification

During setup, the integration validates that `/api/v/1/status` returns:

```json
{
  "success": true,
  "deviceType": "002"
}
```

The device `UID` is used as the unique Home Assistant identifier.

## HACS publishing checklist

Before requesting inclusion in the default HACS catalog:

- Make the GitHub repository public.
- Replace `YOUR_GITHUB_USERNAME` in `manifest.json`.
- Enable GitHub Issues.
- Add repository description and topics.
- Ensure both **HACS** and **Hassfest** GitHub Actions pass.
- Add appropriate branding/icon or register branding with Home Assistant.
- Create a real GitHub **Release**, not only a tag.
- Then submit the repository to `hacs/default`.

## License

MIT.
