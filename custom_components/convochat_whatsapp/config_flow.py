"""Config flow for ConvoChat WhatsApp integration."""
import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.core import callback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

DEFAULT_HOST = "172.30.33.5"
DEFAULT_PORT = 8099


class ConvoChatWhatsAppConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for ConvoChat WhatsApp."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Create the config entry
            return self.async_create_entry(
                title="ConvoChat WhatsApp",
                data=user_input
            )

        # Show form
        data_schema = vol.Schema({
            vol.Optional(CONF_HOST, default=DEFAULT_HOST): str,
            vol.Optional(CONF_PORT, default=DEFAULT_PORT): int,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for ConvoChat WhatsApp."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Optional(
                    CONF_HOST,
                    default=self.config_entry.data.get(CONF_HOST, DEFAULT_HOST)
                ): str,
                vol.Optional(
                    CONF_PORT,
                    default=self.config_entry.data.get(CONF_PORT, DEFAULT_PORT)
                ): int,
            })
        )
