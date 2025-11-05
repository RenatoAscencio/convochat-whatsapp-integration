"""ConvoChat WhatsApp integration for Home Assistant."""
import logging
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.config_entries import ConfigEntry
import aiohttp

from .const import (
    DOMAIN,
    CONF_API_KEY,
    CONF_ACCOUNT_ID,
    API_BASE_URL,
)

_LOGGER = logging.getLogger(__name__)

# Service schemas
SERVICE_SEND_TEXT_SCHEMA = vol.Schema({
    vol.Required("recipient"): cv.string,
    vol.Required("message"): cv.string,
    vol.Optional("priority", default=2): vol.In([1, 2]),
})

SERVICE_SEND_MEDIA_SCHEMA = vol.Schema({
    vol.Required("recipient"): cv.string,
    vol.Required("media_url"): cv.string,
    vol.Required("media_type"): vol.In(["image", "video", "audio"]),
    vol.Optional("caption", default=""): cv.string,
    vol.Optional("priority", default=2): vol.In([1, 2]),
})

SERVICE_SEND_DOCUMENT_SCHEMA = vol.Schema({
    vol.Required("recipient"): cv.string,
    vol.Required("document_url"): cv.string,
    vol.Required("document_name"): cv.string,
    vol.Required("document_type"): vol.In(["pdf", "doc", "docx", "xls", "xlsx", "txt"]),
    vol.Optional("caption", default=""): cv.string,
    vol.Optional("priority", default=2): vol.In([1, 2]),
})


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the ConvoChat WhatsApp component."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up ConvoChat WhatsApp from a config entry."""
    api_key = entry.data.get(CONF_API_KEY)
    account_id = entry.data.get(CONF_ACCOUNT_ID)

    # Store the API credentials for service calls
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "api_key": api_key,
        "account_id": account_id
    }

    async def send_text(call: ServiceCall):
        """Handle send_text service call."""
        recipient = call.data["recipient"]
        message = call.data["message"]
        priority = call.data.get("priority", 2)

        url = f"{API_BASE_URL}/send/text"

        form_data = aiohttp.FormData()
        form_data.add_field("recipient", recipient)
        form_data.add_field("message", message)
        form_data.add_field("priority", str(priority))

        headers = {
            "X-API-Key": api_key,
            "X-Account-Id": account_id
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, data=form_data, headers=headers) as response:
                    if response.status == 200:
                        result = await response.json()
                        _LOGGER.info(f"Message sent successfully: {result}")
                    else:
                        error_text = await response.text()
                        _LOGGER.error(f"Failed to send message: {response.status} - {error_text}")
        except Exception as e:
            _LOGGER.error(f"Error sending message: {e}")

    async def send_media(call: ServiceCall):
        """Handle send_media service call."""
        recipient = call.data["recipient"]
        media_url = call.data["media_url"]
        media_type = call.data["media_type"]
        caption = call.data.get("caption", "")
        priority = call.data.get("priority", 2)

        url = f"{API_BASE_URL}/send/media"

        form_data = aiohttp.FormData()
        form_data.add_field("recipient", recipient)
        form_data.add_field("media_url", media_url)
        form_data.add_field("media_type", media_type)
        form_data.add_field("message", caption)
        form_data.add_field("priority", str(priority))

        headers = {
            "X-API-Key": api_key,
            "X-Account-Id": account_id
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, data=form_data, headers=headers) as response:
                    if response.status == 200:
                        result = await response.json()
                        _LOGGER.info(f"Media sent successfully: {result}")
                    else:
                        error_text = await response.text()
                        _LOGGER.error(f"Failed to send media: {response.status} - {error_text}")
        except Exception as e:
            _LOGGER.error(f"Error sending media: {e}")

    async def send_document(call: ServiceCall):
        """Handle send_document service call."""
        recipient = call.data["recipient"]
        document_url = call.data["document_url"]
        document_name = call.data["document_name"]
        document_type = call.data["document_type"]
        caption = call.data.get("caption", "")
        priority = call.data.get("priority", 2)

        url = f"{API_BASE_URL}/send/document"

        form_data = aiohttp.FormData()
        form_data.add_field("recipient", recipient)
        form_data.add_field("document_url", document_url)
        form_data.add_field("document_name", document_name)
        form_data.add_field("document_type", document_type)
        form_data.add_field("message", caption)
        form_data.add_field("priority", str(priority))

        headers = {
            "X-API-Key": api_key,
            "X-Account-Id": account_id
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, data=form_data, headers=headers) as response:
                    if response.status == 200:
                        result = await response.json()
                        _LOGGER.info(f"Document sent successfully: {result}")
                    else:
                        error_text = await response.text()
                        _LOGGER.error(f"Failed to send document: {response.status} - {error_text}")
        except Exception as e:
            _LOGGER.error(f"Error sending document: {e}")

    # Register services
    hass.services.async_register(
        DOMAIN,
        "send_text",
        send_text,
        schema=SERVICE_SEND_TEXT_SCHEMA
    )

    hass.services.async_register(
        DOMAIN,
        "send_media",
        send_media,
        schema=SERVICE_SEND_MEDIA_SCHEMA
    )

    hass.services.async_register(
        DOMAIN,
        "send_document",
        send_document,
        schema=SERVICE_SEND_DOCUMENT_SCHEMA
    )

    _LOGGER.info("ConvoChat WhatsApp services registered successfully")

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    # Unregister services
    hass.services.async_remove(DOMAIN, "send_text")
    hass.services.async_remove(DOMAIN, "send_media")
    hass.services.async_remove(DOMAIN, "send_document")

    # Remove data
    hass.data[DOMAIN].pop(entry.entry_id)

    return True
