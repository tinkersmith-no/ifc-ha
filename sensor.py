from homeassistant.helpers.event import async_track_time_change
from datetime import datetime
from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN

LANG = {
    "de": {
        "weekdays": ["Montag","Dienstag","Mittwoch","Donnerstag","Freitag","Samstag","Sonntag"],
        "weekdays_short": ["Mon","Die","Mit","Don","Fre","Sam","Son"],
        "months": ["Januari","Februari","März","April","Mai","Juni","Sol","Juli","August","September","Oktober","November","Dezember"],
        "months_short": ["Jan","Feb","Mär","Apr","Mai","Jun","Sol","Jul","Aug","Sep","Okt","Nov","Dez"],
    },
    "en": {
        "weekdays": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
        "weekdays_short": ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
        "months": ["January","February","March","April","May","June","Sol","July","August","September","October","November","December"],
        "months_short": ["Jan","Feb","Mar","Apr","May","Jun","Sol","Jul","Aug","Sep","Oct","Nov","Dec"],
    },
    "es": {
        "weekdays": ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"],
        "weekdays_short": ["Lun","Mar","Mié","Jue","Vie","Sáb","Dom"],
        "months": ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Sol","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"],
        "months_short": ["Ene","Feb","Mar","Abr","May","Jun","Sol","Jul","Ago","Sep","Oct","Nov","Dic"],
    },
    "fr": {
        "weekdays": ["Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi","Dimanche"],
        "weekdays_short": ["Lun","Mar","Mer","Jeu","Ven","Sam","Dim"],
        "months": ["Janvier","Février","Mars","Avril","Mai","Juin","Sol","Juillet","Août","Septembre","Octobre","Novembre","Décembre"],
        "months_short": ["Janv","Févr","Mars","Avr","Mai","Juin","Sol","Juil","Août","Sept","Oct","Nov","Déc"],
    },
    "nb": {
        "weekdays": ["Mandag","Tirsdag","Onsdag","Torsdag","Fredag","Lørdag","Søndag"],
        "weekdays_short": ["Man","Tir","Ons","Tor","Fre","Lør","Søn"],
        "months": ["Januar","Februar","Mars","April","Mai","Juni","Sol","Juli","August","September","Oktober","November","Desember"],
        "months_short": ["Jan","Feb","Mar","Apr","Mai","Jun","Sol","Jul","Aug","Sep","Okt","Nov","Des"],
    },
    "se": {
        "weekdays": ["Måndag","Tisdag","Onsdag","Torsdag","Fredag","Lördag","Söndag"],
        "weekdays_short": ["Mån","Tis","Ons","Tor","Fre","Lör","Sön"],
        "months": ["Januari","Februari","Mars","April","Maj","Juni","Sol","Juli","Augusti","September","Oktober","November","December"],
        "months_short": ["Jan","Feb","Mar","Apr","Maj","Jun","Sol","Jul","Aug","Sep","Okt","Nov","Dec"],
    }
}

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    sensor = IFCSensor()
    async_add_entities([sensor])

    async def _update(now):
        sensor.update()
        sensor.async_write_ha_state()

    async_track_time_change(hass, _update, minute=0)
    _update(None)

class IFCSensor(SensorEntity):
    name = "IFC Date"
    icon = "mdi:calendar-clock"
    has_entity_name = True

    @property
    def unique_id(self):
        return "ifc_date"

    def update(self):
        # Always initialize attributes first
        self._attributes = {}

        # Read UI / locale language
        lang_raw = getattr(self.hass.config, "language", "en")
        lang_base = lang_raw.split("-")[0].split("_")[0]
        lang = lang_base if lang_base in LANG else "en"

        now = datetime.now()
        doy = now.timetuple().tm_yday - 1
        year = now.year

        # Intercalary day
        if doy >= 364:
            self._state = f"Year Day {year}"
            self._attributes.update({
                "is_intercalary": True,
                "year": year,
                "language": lang,
                "language_raw": lang_raw,
            })
            return

        month = doy // 28 + 1
        day = doy % 28 + 1
        weekday_index = (day - 1) % 7

        weekday = LANG[lang]["weekdays"][weekday_index]
        weekday_short = LANG[lang]["weekdays_short"][weekday_index]
        month_name = LANG[lang]["months"][month - 1]
        month_short = LANG[lang]["months_short"][month - 1]

        # Default format as specified in README.md
        self._state = f"{year}-{month:02d}-{day:02d} ({month_short} {day:02d} {year})"

        self._attributes.update({
            "weekday": weekday,
            "weekday_short": weekday_short,
            "weekday_number": weekday_index + 1,
            "day": day,
            "month": month,
            "month_name": month_name,
            "month_short": month_short,
            "year": year,
            "language": lang,
            "language_raw": lang_raw,
            "is_intercalary": False,
        })

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attributes
