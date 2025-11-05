"""Constants for the ConvoChat WhatsApp integration."""

DOMAIN = "convochat_whatsapp"

# Configuration keys
CONF_API_KEY = "api_key"
CONF_ACCOUNT_ID = "account_id"

# ConvoChat API
API_BASE_URL = "https://sms.convo.chat/api"

# Service names
SERVICE_SEND_TEXT = "send_text"
SERVICE_SEND_MEDIA = "send_media"
SERVICE_SEND_DOCUMENT = "send_document"

# Service parameters
ATTR_RECIPIENT = "recipient"
ATTR_MESSAGE = "message"
ATTR_CAPTION = "caption"
ATTR_PRIORITY = "priority"
ATTR_MEDIA_URL = "media_url"
ATTR_MEDIA_TYPE = "media_type"
ATTR_DOCUMENT_URL = "document_url"
ATTR_DOCUMENT_NAME = "document_name"
ATTR_DOCUMENT_TYPE = "document_type"
