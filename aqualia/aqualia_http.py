"""HTTP Client for the Aqualia API."""

import asyncio
import aiohttp
import json
import logging

import requests

_LOGGER = logging.getLogger(__name__)

class AqualiaAPI:
    """Class to make authenticated requests."""

    def __init__(self, username: str, password: str):
        """Initialize the auth."""
        self.username = username
        self.password = password
        self.host = "https://oficinavirtualapi.aqualia.es"
        self.origin="https://oficinavirtual.aqualia.es"
        self.login_path="ofcvirtual/auth/v1/api/auth/Auth/Login"
        self.consumption_path="ofcvirtual/meter/v1/api/meter/Meter/GetContractConsumptionCurve"
        self.contracts_path="ofcvirtual/contract/v1/api/contract/Contract/GetUserLinkedContracts"
        self.headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Accept":"application/json, text/plain, */*",
            "Application-Id":"1",
            "Country":"34",
            "Origin":self.origin,
            "Referer":f"{self.origin}/",
            "X-Content-Type-Options":"nosniff",
            "Accept-Language":"es-es"
        }

    async def get_token(self) -> bool:
        """Get a Bearer Token."""
        data = {
            "LoginType": 1,
            "User": self.username,
            "Password": self.password
        }
        url=f'{self.host}/{self.login_path}'
        async with aiohttp.ClientSession(headers=self.headers) as session, session.post(url=url,json=data) as response:
            json_body= await response.json()
            if 'Token' in json_body:
                self.headers['Authorization']=f'Bearer {json_body['Token']}'
                return json_body
            return None

    async def get_contracts(self):
        """Get the contracts for the authenticated user."""
        url=f'{self.host}/{self.contracts_path}'
        async with aiohttp.ClientSession(headers=self.headers) as session, session.get(url=url) as response:
            contracts = await response.json()
            return contracts["ContractDetails"]

    async def get_consumption(self,date_from) ->dict:
        """Get the consumption from a date until now."""
        data={
            "DateFrom":date_from,
            "DateTo":"2024-10-16T00:00:00.000Z",
            "Contract":{
                "CacCode":25862610,
                "ContractCode":163790,
                "InstallationCode":13905,
                "ContractNumber":"13905-1/1-163769"
                }
        }
        url=f'{self.host}/{self.consumption_path}'
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.post(url=url,json=data) as response:
                json_body= await response.json()
                _LOGGER.info(str(json_body))
                return json_body


