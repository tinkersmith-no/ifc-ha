# IFC for Home Assistant

This is a custom Home Assistant integration that exposes the **International Fixed Calendar (IFC)** as a sensor, allowing you to display and use IFC dates in dashboards, widgets, and automations.

You can read more about the International Fixed Calendar here:
👉 https://tinkersmith.no/calendar

## Sensor

The integration creates a single sensor:
```
sensor.ifc_date
```
The sensor state provides a neutral, sortable default format, while all date components are exposed as attributes for full user customization.

---

## Available attributes

The following attributes are always available:

- **weekday** — verbal weekday name  
  `Monday`
- **weekday_short** — abbreviated weekday  
  `Mon`
- **weekday_number** — numeric weekday (1–7, Monday = 1)  
  `1`
- **day** — day of month (1–28)  
  `11`
- **month** — month number (1–13)  
  `13`
- **month_name** — verbal month name  
  `December`
- **month_short** — abbreviated month name  
  `Dec`
- **year** — year number  
  `2025`
- **is_intercalary** — boolean indicating an intercalary day  
  `true / false`

All attributes are localized automatically based on Home Assistant’s configured language.

---

## Default state format

The default sensor state is intentionally neutral and machine-friendly:


## Default state format

The default sensor state is intentionally neutral and machine-friendly:
```
YYYY-MM-DD (Month Day Year)
```

Example:
```
2025-13-11 (Dec 11 2025)
```

This format is meant as a sensible baseline and can safely be ignored if you prefer a different presentation.

---

## Custom date formatting

The IFC sensor exposes all date components as attributes.  
Users are encouraged to format the date themselves using Home Assistant templates.

### Example: verbal date

Output:
```
Monday 01. January 2025
```
```
{{ state_attr('sensor.ifc_date', 'weekday') }}
{{ state_attr('sensor.ifc_date', 'day') }}.
{{ state_attr('sensor.ifc_date', 'month_name') }}
{{ state_attr('sensor.ifc_date', 'year') }}
```
![screenshot](https://github.com/user-attachments/assets/581a4a3c-0861-4908-8742-93a24111c30b)

Example: compact format
```
Mon 11 Dec
```
```
{{ state_attr('sensor.ifc_date', 'weekday_short') }}
{{ state_attr('sensor.ifc_date', 'day') }}
{{ state_attr('sensor.ifc_date', 'month_short') }}
```
Example: numeric-only format
```
2025-13-11
```
```
{{ state_attr('sensor.ifc_date', 'year') }}-
{{ '%02d' | format(state_attr('sensor.ifc_date', 'month')) }}-
{{ '%02d' | format(state_attr('sensor.ifc_date', 'day')) }}
```
## Installation
Add the integration in ```configuration.yaml```:
```
sensor:
  - platform: ifc
```
## Notes
Formatting is intentionally left to the user to allow maximum flexibility.
The integration provides structured data, not opinionated presentation.
The sensor updates automatically and is suitable for dashboards, widgets, and automations.

### Translations
Current languages are
- Deutsch
- English
- Español
- Français
- Norsk bokmål
- Svenska

  Feel free to add more translations!
