"""ConvoChat WhatsApp integration for Home Assistant."""
import logging
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PORT
import aiohttp

_LOGGER = logging.getLogger(__name__)

DOMAIN = "convochat_whatsapp"
DEFAULT_HOST = "172.30.33.5"
DEFAULT_PORT = 8099

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
    host = entry.data.get(CONF_HOST, DEFAULT_HOST)
    port = entry.data.get(CONF_PORT, DEFAULT_PORT)

    base_url = f"http://{host}:{port}"

    # Store the base URL for service calls
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "base_url": base_url
    }

    async def send_text(call: ServiceCall):
        """Handle send_text service call."""
        recipient = call.data["recipient"]
        message = call.data["message"]
        priority = call.data.get("priority", 2)

        url = f"{base_url}/send/text"
        payload = {
            "recipient": recipient,
            "message": message,
            "priority": priority
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    if response.status == 200:
                        result = await response.json()
                        _LOGGER.info(f"Message sent successfully: {result}")
                    else:
                        _LOGGER.error(f"Failed to send message: {response.status}")
        except Exception as e:
            _LOGGER.error(f"Error sending message: {e}")

    async def send_media(call: ServiceCall):
        """Handle send_media service call."""
        recipient = call.data["recipient"]
        media_url = call.data["media_url"]
        media_type = call.data["media_type"]
        caption = call.data.get("caption", "")
        priority = call.data.get("priority", 2)

        url = f"{base_url}/send/media"
        payload = {
            "recipient": recipient,
            "media_url": media_url,
            "media_type": media_type,
            "message": caption,
            "priority": priority
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    if response.status == 200:
                        result = await response.json()
                        _LOGGER.info(f"Media sent successfully: {result}")
                    else:
                        _LOGGER.error(f"Failed to send media: {response.status}")
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

        url = f"{base_url}/send/document"
        payload = {
            "recipient": recipient,
            "document_url": document_url,
            "document_name": document_name,
            "document_type": document_type,
            "message": caption,
            "priority": priority
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    if response.status == 200:
                        result = await response.json()
                        _LOGGER.info(f"Document sent successfully: {result}")
                    else:
                        _LOGGER.error(f"Failed to send document: {response.status}")
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
