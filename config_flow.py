"""Config flow for aqualia integration."""

from __future__ import annotations

import asyncio
import logging
from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import selector as sel
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from . import const
from .aqualia_api import AqualiaAPI, AqualiaAPIError

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USERNAME): str,
        vol.Required(CONF_PASSWORD): str,
    }
)

def STEP_CONTRACT_DATA_SCHEMA(address_list: list[str]) -> dict[str, Any]:
    """Build the dict schema from a contracts list."""

    return {
        vol.Required(
            const.MODEL_SUPPLY_ADDRESS,
        ): sel.SelectSelector({"options": address_list}),
    }


class PlaceholderHub:
    """Placeholder class to make tests pass.

    TODO Remove this placeholder class and replace with things from your PyPI package.
    """

    def __init__(self, host: str) -> None:
        """Initialize."""
        self.host = host

    async def authenticate(self, username: str, password: str) -> bool:
        """Test if we can authenticate with the host."""
        return True


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """
    session = async_get_clientsession(hass)
    aqualia_client=AqualiaAPI(session, data[CONF_USERNAME], data[CONF_PASSWORD])
    bool_response=await aqualia_client.login()
    if not bool_response:
        raise InvalidAuth

    # Return info that you want to store in the config entry.
    return aqualia_client


class ConfigFlow(ConfigFlow, domain=const.DOMAIN):
    """Handle a config flow for aqualia."""

    def __init__(self) -> None:
        """Initialize config flow."""
        super().__init__()
        self.client = None
        self.inputs = {}
        self.data = {}

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                self.client = await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                self.data ={
                    CONF_USERNAME: user_input[CONF_USERNAME],
                    CONF_PASSWORD: user_input[CONF_PASSWORD]
                }
                return await self.async_step_contract()

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )

    async def async_step_contract(
            self, user_input: dict[str, Any] = None
    ) -> ConfigFlowResult:
        """Confirm contract."""
        errors: dict[str, str] = {}

        if user_input is None:
            try:
                self.inputs[const.MODEL_CONTRACT_LIST] = await self.client.get_contracts()
            except AqualiaAPIError as err:
                errors["base"]=err.args[0]
                self.inputs[const.MODEL_CONTRACT_LIST] = []
            return self.async_show_form(
                step_id="contract",
                data_schema=vol.Schema(
                    STEP_CONTRACT_DATA_SCHEMA(
                        [x[const.MODEL_SUPPLY_ADDRESS] for x in self.inputs[const.MODEL_CONTRACT_LIST]]
                        )
                    ),
                errors=errors
            )
        self.data[const.MODEL_CONTRACT] = [
            x for x in self.inputs[const.MODEL_CONTRACT_LIST]
            if x[const.MODEL_SUPPLY_ADDRESS]==user_input[const.MODEL_SUPPLY_ADDRESS]
        ][0]
        # Assign a unique ID to the flow and abort the flow
        # if another flow with the same unique ID is in progress
        await self.async_set_unique_id(f'aqualia_{self.data[const.MODEL_CONTRACT][const.MODEL_CONTRACT_INFO][const.MODEL_CONTRACT_CODE]}')

        # Abort the flow if a config entry with the same unique ID exists
        self._abort_if_unique_id_configured()

        return self.async_create_entry(title=user_input[const.MODEL_SUPPLY_ADDRESS], data=self.data)

class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
