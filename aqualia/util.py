"""Util methods for statistics import."""
from datetime import datetime, timedelta
import logging
import zoneinfo

from homeassistant.components.recorder.statistics import valid_statistic_id
from homeassistant.core import valid_entity_id
from homeassistant.exceptions import HomeAssistantError

from . import const

_LOGGER = logging.getLogger(__name__)

def get_source(statistic_id: str) -> str:
    """Get the source of a statistic based on the given statistic_id."""
    if valid_entity_id(statistic_id):
        source = statistic_id.split(".")[0]
        if source == "recorder":
            raise HomeAssistantError(f"Invalid statistic_id {statistic_id}. DOMAIN 'recorder' is not allowed.")
        source = "recorder"
    elif valid_statistic_id(statistic_id):
        source = statistic_id.split(":")[0]
        if len(source) == 0:
            raise HomeAssistantError(f"Implementation error, this must not happen. Invalid statistic_id. (must not start with ':'): {statistic_id}")
        if source == "recorder":
            raise HomeAssistantError(f"Invalid statistic_id {statistic_id}. DOMAIN 'recorder' is not allowed.")
    else:
        raise HomeAssistantError(f"Statistic_id {statistic_id} is invalid. Use either an existing entity ID (containing a '.'), or a statistic id (containing a ':')")

    return source

def prepare_data(
        sensor_id:str,
        sensor_unit:str,
        data:dict,
        last_consumption:float,
        last_update_dt:datetime)->tuple:
    """Prepare data to import the statistics."""
    metadata={
            "has_mean": False,
            "has_sum": True,
            "source": get_source(sensor_id),
            "statistic_id": sensor_id,
            "name": None,
            "unit_of_measurement": sensor_unit,
        }
    stats = {
        const.STATS_METADATA:metadata,
        const.STATS_STATISTICS:[]
    }
    timezone = zoneinfo.ZoneInfo("Europe/Madrid")
    last_update_dt = last_update_dt.replace(minute=0, second=0,tzinfo=timezone)
    for record in data:
        record_dt = datetime.strptime(record[const.MODEL_DATE_TIME_CONSUMPTION_CURVE],"%Y-%m-%dT%H:%M:%S")
        record_dt = record_dt.replace(minute=0, second=0, tzinfo=timezone)
        while (record_dt-last_update_dt).total_seconds()>3600: #We fill the gaps between records
            last_update_dt=last_update_dt+timedelta(hours=1)
            stats[const.STATS_STATISTICS].append(
            {
                "start": last_update_dt,
                "state": 0,
                "sum": last_consumption,
                "last_reset": last_update_dt-timedelta(hours=1)
            }
        )
        consumption = record[const.MODEL_CONSUMPTION_VALUE]
        consumption_sum=consumption+last_consumption
        last_consumption=consumption_sum
        stats[const.STATS_STATISTICS].append(
            {
                "start": record_dt,
                "state": consumption,
                "sum": consumption_sum,
                "last_reset": record_dt-timedelta(hours=1)
            }
        )
    now=datetime.now().replace(minute=0, second=0, tzinfo=timezone)
    while (now-last_update_dt).total_seconds()>3600: #We fill the gaps between records
            last_update_dt=last_update_dt+timedelta(hours=1)
            stats[const.STATS_STATISTICS].append(
            {
                "start": last_update_dt,
                "state": 0,
                "sum": last_consumption,
                "last_reset": last_update_dt-timedelta(hours=1)
            }
        )
    return stats
