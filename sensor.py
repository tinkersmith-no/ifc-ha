from datetime import datetime
from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    async_add_entities([IFCSensor()])

class IFCSensor(SensorEntity):
    name = "IFC Date"
    icon = "mdi:calendar-clock"

    def update(self):
        now = datetime.now()
        doy = now.timetuple().tm_yday - 1  # 0-based
        year = now.year

        if doy >= 364:
            self._state = f"Year Day {year}"
            return

        month = doy // 28 + 1
        day   = doy % 28 + 1

        months = {
            1: "January", 2: "February", 3: "March",
            4: "April", 5: "May", 6: "June",
            7: "Sol", 8: "July", 9: "August",
            10: "September", 11: "October", 12: "November",
            13: "December"
        }

        weekdays = [
            "Monday","Tuesday","Wednesday",
            "Thursday","Friday","Saturday","Sunday"
        ]

        weekday = weekdays[(day - 1) % 7]
        self._state = f"{weekday} {day}. {months[month]} {year}"

    @property
    def state(self):
        return self._state
