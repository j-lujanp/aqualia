"""HTTP Client for the Aqualia API."""

import asyncio
from datetime import datetime
import json
import logging

from aiohttp import ClientResponse, ClientSession
import requests

from . import const

_LOGGER = logging.getLogger(__name__)

class AqualiaAPIError(Exception):
    pass

class AqualiaAPI:
    """Class to make authenticated requests."""

    def __init__(self, websession: ClientSession, username:str, password:str):
        """Initialize the auth."""
        self.websession = websession
        self.username = username
        self.password = password
        self.headers = const.AQUALIA_HEADERS
        self.token = ''
        self.token_expiration_date = datetime.now()

    async def login(self) ->bool:
        """Get the bearer token if there is no valid one."""
        return True #for testing
        if self.token == '' or self.token_expiration_date < datetime.now():
            data = {
                "LoginType": 1,
                "User": self.username,
                "Password": self.password
            }
            url=f'{const.AQUALIA_API_BASE_URL}/{const.AQUALIA_LOGIN_PATH}'
            async with self.websession.post(url=url,json=data, headers=self.headers) as response:
                json_body= await response.json()
                if const.MODEL_TOKEN in json_body:
                    self.token=json_body[const.MODEL_TOKEN]
                    self.token_expiration_date=datetime.strptime(json_body[const.MODEL_TOKEN_EXPIRATION_DATE],"%Y-%m-%dT%H:%M:%SZ")
                    self.headers['Authorization']=f'Bearer {self.token}'
                    return True
                else:
                    return False
        else:
            return True

    async def get_contracts(self)->list:
        """Get the contracts for the authenticated user."""
        return json.loads(const.FAKE_CONTRACTS)[const.MODEL_CONTRACT_DETAILS] #For testing only
        bool_response = await self.login()
        if bool_response:
            url=f'{const.AQUALIA_API_BASE_URL}/{const.AQUALIA_CONTRACTS_PATH}'
            async with self.websession.get(url=url, headers=self.headers) as response:
                response = await response.json()
                try:
                    return response[const.MODEL_CONTRACT_DETAILS]
                except KeyError:
                    raise AqualiaAPIError(response['title'])
        else:
            return []

    async def get_consumption(self,contract,date_from=None) ->dict:
        """Get the consumption from a date until now."""
        return json.loads(const.FAKE_CONSUMPTION) #For testing only
        if await self.login():
            data={
                "DateFrom":date_from.strftime("%Y-%m-%dT00:00:00.000Z"),
                "DateTo":datetime.now().strftime("%Y-%m-%dT00:00:00.000Z"),
                "Contract":{
                    const.MODEL_CAC_CODE:contract[const.MODEL_CONTRACT_INFO][const.MODEL_CAC_CODE],
                    const.MODEL_CONTRACT_CODE:contract[const.MODEL_CONTRACT_INFO][const.MODEL_CONTRACT_CODE],
                    const.MODEL_INSTALLATION_CODE:contract[const.MODEL_CONTRACT_INFO][const.MODEL_INSTALLATION_CODE],
                    const.MODEL_CONTRACT_NUMBER:contract[const.MODEL_CONTRACT_INFO][const.MODEL_CONTRACT_NUMBER]
                    }
            }
            url=f'{const.AQUALIA_API_BASE_URL}/{const.AQUALIA_CONSUMPTION_PATH}'
            async with self.websession.post(headers=self.headers,url=url,json=data) as response:
                return await response.json()
        else:
            return {}

#{
#    'UnitOfMeasurement' ='Litros',
#    'ResponseCode' ='00001',
#    'ResponseDescription' ='OK',
#    {
#        'DateTimeConsumptionCurve': '2024-10-12T00:00:00',
#        'ReadingIndex': 0,
#        'ConsumptionValue': 259.94
#    }
#}



class Consumption:
    """Class that represents a Consumption object in the AqualiaAPI."""

    def __init__(self, raw_data: dict, api: AqualiaAPI):
        """Initialize a consumption object."""
        self.raw_data = raw_data
        self.api = api

    # Note: each property name maps the name in the returned data

    @property
    def ContractNumber(self) -> str:
        """Return the ID of the light."""
        return self.raw_data[const.MODEL_CONTRACT_NUMBER]

    @property
    def UnitOfMeasurement(self) -> str:
        """Return the ID of the light."""
        return self.raw_data[const.MODEL_UNIT_OF_MEASUREMENT]

    @property
    def DateTimeConsumptionCurve(self) -> str:
        """Return the ID of the light."""
        return self.raw_data[const.MODEL_DATE_TIME_CONSUMPTION_CURVE]

    @property
    def ReadingIndex(self) -> int:
        """Return the reading index of the consumption."""
        return self.raw_data[const.MODEL_READING_INDEX]

    @property
    def ConsumptionValue(self) -> float:
        """Return the value of the consumption."""
        return self.raw_data[const.MODEL_CONSUMPTION_VALUE]

    async def async_update(self):
        """Update the consumption data."""
        resp = await self.api.get_consumption(
            self.ContractNumber,
            datetime.strptime(self.DateTimeConsumptionCurve,"%Y/%m/%dT%H:%M:%S"))
        resp.raise_for_status()
        self.raw_data = await resp.json()
