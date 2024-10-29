"""The aqualia integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from . import const
from .aqualia_api import AqualiaAPI

# This integration will create a sensor for water consumption.
PLATFORMS: list[Platform] = [Platform.SENSOR]

type AqualiaConfigEntry = ConfigEntry[AqualiaAPI]  # noqa: F821


async def async_setup_entry(hass: HomeAssistant, entry: AqualiaConfigEntry) -> bool:
    """Set up aqualia from a config entry."""
    hass.data.setdefault(const.DOMAIN, {})
    hass.data[const.DOMAIN][entry.entry_id] = entry.data
    # This will call Entity.set_sleep_timer(sleep_time=VALUE)
    #Platform.SENSOR.async_register_entity_service("reset_statistics")
    # 1. Create API instance
    session = async_get_clientsession(hass)
    api=AqualiaAPI(session, entry.data[CONF_USERNAME], entry.data[CONF_PASSWORD])
    # 2. Validate the API connection (and authentication)
    if await api.login():
        # 3. Store an API object for your platforms to access
        entry.runtime_data = api
        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
        return True
    else:
        return False




async def async_unload_entry(hass: HomeAssistant, entry: AqualiaConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
