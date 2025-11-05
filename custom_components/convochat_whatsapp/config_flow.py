"""Config flow for ConvoChat WhatsApp integration."""
import logging
import voluptuous as vol
import aiohttp

from homeassistant import config_entries
from homeassistant.core import callback

from .const import DOMAIN, CONF_API_KEY, CONF_WHATSAPP_ACCOUNT, API_BASE_URL

_LOGGER = logging.getLogger(__name__)


class ConvoChatWhatsAppConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for ConvoChat WhatsApp."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Fetch WhatsApp accounts
            api_key = user_input[CONF_API_KEY]
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        f"{API_BASE_URL}/get/wa.accounts",
                        params={"secret": api_key, "limit": 100}
                    ) as response:
                        if response.status == 200:
                            result = await response.json()
                            if result.get("status") == 200 and result.get("data"):
                                accounts = result["data"]
                                if len(accounts) > 0:
                                    # Store API key and show account selection
                                    self.api_key = api_key
                                    self.accounts = accounts
                                    return await self.async_step_select_account()
                                else:
                                    errors["base"] = "no_accounts"
                            else:
                                errors["base"] = "invalid_auth"
                        else:
                            errors["base"] = "cannot_connect"
            except Exception as e:
                _LOGGER.error(f"Error fetching WhatsApp accounts: {e}")
                errors["base"] = "unknown"

        # Show form
        data_schema = vol.Schema({
            vol.Required(CONF_API_KEY): str,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors
        )

    async def async_step_select_account(self, user_input=None):
        """Handle account selection."""
        if user_input is not None:
            # Create entry with selected account
            return self.async_create_entry(
                title=f"ConvoChat WhatsApp ({user_input[CONF_WHATSAPP_ACCOUNT]})",
                data={
                    CONF_API_KEY: self.api_key,
                    CONF_WHATSAPP_ACCOUNT: user_input[CONF_WHATSAPP_ACCOUNT],
                }
            )

        # Build account options
        account_options = {
            acc["unique"]: f"{acc['name']} ({acc['phone']})"
            for acc in self.accounts
        }

        data_schema = vol.Schema({
            vol.Required(CONF_WHATSAPP_ACCOUNT): vol.In(account_options),
        })

        return self.async_show_form(
            step_id="select_account",
            data_schema=data_schema,
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
                vol.Required(
                    CONF_API_KEY,
                    default=self.config_entry.data.get(CONF_API_KEY)
                ): str,
                vol.Required(
                    CONF_WHATSAPP_ACCOUNT,
                    default=self.config_entry.data.get(CONF_WHATSAPP_ACCOUNT)
                ): str,
            })
        )
