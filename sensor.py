"""Platform for sensor integration."""
from __future__ import annotations

from collections.abc import Callable
from datetime import datetime, timedelta
import logging
from typing import Any

import async_timeout
import voluptuous as vol

from homeassistant.components.sensor import (
    PLATFORM_SCHEMA as SENSOR_PLATFORM_SCHEMA,
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, Platform, UnitOfVolume
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers import (
    config_validation as cv,
    device_registry as dr,
    discovery_flow,
)
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback, async_get_current_platform
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.components.recorder.statistics import (
    async_add_external_statistics,
    async_import_statistics,
)

from . import const
from .aqualia_api import AqualiaAPI
from .util import prepare_data

SCAN_INTERVAL = timedelta(minutes=1)
_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
        hass: HomeAssistant,
        entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback
        ) -> bool:
    """Set up the platform."""
    session = async_get_clientsession(hass)
    my_api = AqualiaAPI(session, entry.data[CONF_USERNAME], entry.data[CONF_PASSWORD])

    device = Consumption(my_api, entry.data[const.MODEL_CONTRACT])
    async_add_entities(
        [device]
    )
    platform = async_get_current_platform()
    platform.async_register_entity_service(
        name=const.SERVICE_RESET_STATISTICS,
        schema=None,
        func="reset_statistics",
    )

# https://developers.home-assistant.io/docs/core/entity/sensor/
class Consumption(SensorEntity):
    """Aqualia Sensor."""

    def __init__(self, my_api:AqualiaAPI, contract) -> None:
        """Init entity."""
        super().__init__()

        self.contract = contract
        self._attr_native_unit_of_measurement = UnitOfVolume.LITERS
        self._attr_device_class = SensorDeviceClass.WATER
        self._attr_state_class = SensorStateClass.TOTAL
        self._name = f'aqualia_{contract[const.MODEL_CONTRACT_INFO][const.MODEL_CONTRACT_NUMBER]}'
        self._state = 0
        self._available = True
        self.api = my_api
        self._last_consumption_datetime = None
        self._last_consumption_value = 0
        self._last_consumption_sum = 0
        self.attrs: dict[str, Any]= {const.MODEL_ENTRY_DATE:self.contract[const.MODEL_ENTRY_DATE]}
        self.attrs[const.MODEL_DATE_TIME_CONSUMPTION_CURVE]=self.last_consumption_datetime
        self.attrs[const.MODEL_CONSUMPTION_VALUE]=self._last_consumption_value
        self.attrs[const.TOTAL_CONSUMPTION_SUM]=self._last_consumption_sum
        for key in list(self.contract[const.MODEL_CONTRACT_INFO]):
            self.attrs[key]=self.contract[const.MODEL_CONTRACT_INFO][key]

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return DeviceInfo(
            identifiers={
                # Serial numbers are unique identifiers within a specific domain
                (const.DOMAIN, self.contract[const.MODEL_CONTRACT_INFO][const.MODEL_CONTRACT_NUMBER])
            },
            name=self.contract[const.MODEL_CONTRACT_INFO][const.MODEL_CONTRACT_NUMBER]
        )

    @property
    def name(self) -> str:
        """Return the name of the entity."""
        return self._name

    @property
    def last_consumption_datetime(self) -> str:
        """Return the datetime of the last update."""
        return self._last_consumption_datetime

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._available

    @property
    def state(self) -> str | None:
        """Return the last measurement of the event."""
        return self._state

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra attributes."""
        return self.attrs

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return self.name

    async def reset_statistics(self):
        """Recreate statistics from the Entry Date."""
        last_update=datetime.strptime(self.contract[const.MODEL_ENTRY_DATE],"%d/%m/%Y %H:%M:%S")
        consumption = await self.api.get_consumption(self.contract,last_update)
        if len(consumption[const.MODEL_CONSUMPTION_CURVES]) > 0:
            stats, consumption_sum, last_reported_update = prepare_data(
                self.entity_id,
                self._attr_native_unit_of_measurement,
                consumption[const.MODEL_CONSUMPTION_CURVES],
                last_consumption=0,
                last_update_dt=last_update
                )
            metadata = stats[const.STATS_METADATA]
            async_import_statistics(self.hass, metadata, stats[const.STATS_STATISTICS])
            self._last_consumption_value = consumption[const.MODEL_CONSUMPTION_CURVES][-1][const.MODEL_CONSUMPTION_VALUE]
            self._state = self._last_consumption_value
            self.attrs[const.MODEL_CONSUMPTION_VALUE]=self._last_consumption_value
            self._last_consumption_sum = consumption_sum
            self.attrs[const.TOTAL_CONSUMPTION_SUM]=self._last_consumption_sum
            self._last_consumption_datetime = last_reported_update
            self.attrs[const.MODEL_DATE_TIME_CONSUMPTION_CURVE]=self._last_consumption_datetime
            self.last_reset=self._last_consumption_datetime

    # https://github.com/klausj1/homeassistant-statistics/blob/main/custom_components/import_statistics/prepare_data.py#L22
    async def async_update(self) -> None:
        """Update the value of the entity."""
        if self.last_consumption_datetime is not None:
            last_update=self.last_consumption_datetime
        else:
            last_update=datetime.strptime(self.contract[const.MODEL_ENTRY_DATE],"%d/%m/%Y %H:%M:%S")
        consumption = await self.api.get_consumption(self.contract,last_update)
        if len(consumption[const.MODEL_CONSUMPTION_CURVES]) > 0:
            stats, consumption_sum, last_reported_update = prepare_data(
                self.entity_id,
                self._attr_native_unit_of_measurement,
                consumption[const.MODEL_CONSUMPTION_CURVES],
                last_consumption=self._state,
                last_update_dt=last_update
                )
            metadata = stats[const.STATS_METADATA]
            async_import_statistics(self.hass, metadata, stats[const.STATS_STATISTICS])
            self._last_consumption_value = consumption[const.MODEL_CONSUMPTION_CURVES][-1][const.MODEL_CONSUMPTION_VALUE]
            self._state = self._last_consumption_value
            self.attrs[const.MODEL_CONSUMPTION_VALUE]=self._last_consumption_value
            self._last_consumption_sum = consumption_sum
            self.attrs[const.TOTAL_CONSUMPTION_SUM]=self._last_consumption_sum
            self._last_consumption_datetime = last_reported_update
            self.attrs[const.MODEL_DATE_TIME_CONSUMPTION_CURVE]=self.last_consumption_datetime
            self.last_reset=self.last_consumption_datetime
        else:
            self._state = 0
            self.last_reset = self.last_consumption_datetime
        self._available = True
