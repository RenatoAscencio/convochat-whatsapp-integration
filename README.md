# ConvoChat WhatsApp Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Standalone Home Assistant integration that provides native WhatsApp messaging services directly through the ConvoChat API.

## Features

- Native Home Assistant services for WhatsApp messaging
- Send text messages, images, videos, audio, and documents
- Direct connection to ConvoChat API (no addon required!)
- UI configuration through Home Assistant settings
- Priority message support
- Fully standalone integration

## Prerequisites

**ConvoChat Account** - Active account with API credentials
- Sign up at: https://convo.chat
- Get your API Key and Account ID from the ConvoChat dashboard

## Installation

### HACS Installation (Recommended)

1. Open HACS in your Home Assistant
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL: `https://github.com/RenatoAscencio/convochat-whatsapp-integration`
6. Select category: "Integration"
7. Click "Add"
8. Search for "ConvoChat WhatsApp" in HACS
9. Click "Download"
10. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/convochat_whatsapp` directory to your Home Assistant's `custom_components` directory
2. Restart Home Assistant

## Configuration

1. Go to **Settings** → **Devices & Services**
2. Click **+ ADD INTEGRATION**
3. Search for "ConvoChat WhatsApp"
4. Enter your ConvoChat API credentials:
   - **API Key**: Your ConvoChat API key
   - **Account ID**: Your ConvoChat account ID
   - Get these from: https://convo.chat dashboard
5. Click **Submit**

The integration will register three services automatically:
- `convochat_whatsapp.send_text`
- `convochat_whatsapp.send_media`
- `convochat_whatsapp.send_document`

## Services

### send_text

Send a text message via WhatsApp.

**Service Data:**
| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| recipient | Yes | Phone number in E.164 format | +523349426465 |
| message | Yes | Text message to send | "Hello from Home Assistant!" |
| priority | No | Message priority (1=high, 2=normal) | 2 |

**Example:**
```yaml
service: convochat_whatsapp.send_text
data:
  recipient: "+523349426465"
  message: "The door was opened at {{ now().strftime('%H:%M') }}"
  priority: 2
```

### send_media

Send an image, video, or audio file via WhatsApp.

**Service Data:**
| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| recipient | Yes | Phone number in E.164 format | +523349426465 |
| media_url | Yes | Public URL of the media file | https://example.com/image.jpg |
| media_type | Yes | Type of media (image/video/audio) | image |
| caption | No | Caption for the media | "Photo from camera" |
| priority | No | Message priority (1=high, 2=normal) | 2 |

**Example:**
```yaml
service: convochat_whatsapp.send_media
data:
  recipient: "+523349426465"
  media_url: "https://your-ha.duckdns.org/local/snapshot.jpg"
  media_type: "image"
  caption: "Motion detected!"
```

### send_document

Send a document (PDF, DOC, XLS, etc.) via WhatsApp.

**Service Data:**
| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| recipient | Yes | Phone number in E.164 format | +523349426465 |
| document_url | Yes | Public URL of the document | https://example.com/report.pdf |
| document_name | Yes | Name of the file with extension | report.pdf |
| document_type | Yes | Type of document (pdf/doc/docx/xls/xlsx/txt) | pdf |
| caption | No | Caption for the document | "Monthly report" |
| priority | No | Message priority (1=high, 2=normal) | 2 |

**Example:**
```yaml
service: convochat_whatsapp.send_document
data:
  recipient: "+523349426465"
  document_url: "https://example.com/report.pdf"
  document_name: "report.pdf"
  document_type: "pdf"
  caption: "Here's the monthly report"
```

## Usage in Automations

### Visual Editor

1. Create a new automation
2. Add a trigger (time, state change, etc.)
3. Add an action → Call service
4. Search for "convochat" or "whatsapp"
5. Select the service you want to use
6. Fill in the required fields

### YAML Editor

```yaml
alias: Door Opened Notification
trigger:
  - platform: state
    entity_id: binary_sensor.front_door
    to: "on"
action:
  - service: convochat_whatsapp.send_text
    data:
      recipient: "+523349426465"
      message: "Front door was opened at {{ now().strftime('%H:%M') }}"
mode: single
```

### Motion Detection with Photo

```yaml
alias: Motion Alert with Photo
trigger:
  - platform: state
    entity_id: binary_sensor.motion_sensor
    to: "on"
action:
  - service: camera.snapshot
    target:
      entity_id: camera.front_door
    data:
      filename: /config/www/motion_snapshot.jpg
  - delay:
      seconds: 2
  - service: convochat_whatsapp.send_media
    data:
      recipient: "+523349426465"
      caption: "Motion detected at {{ now().strftime('%H:%M:%S') }}"
      media_url: "https://YOUR-DOMAIN.duckdns.org/local/motion_snapshot.jpg"
      media_type: "image"
mode: single
```

### Daily Report

```yaml
alias: Daily Energy Report
trigger:
  - platform: time
    at: "23:00:00"
action:
  - service: convochat_whatsapp.send_text
    data:
      recipient: "+523349426465"
      message: |
        📊 Daily Report {{ now().strftime('%d/%m/%Y') }}

        🏠 Home Temperature: {{ states('sensor.temperature_home') }}°C
        💡 Energy Consumption: {{ states('sensor.energy_daily') }} kWh

        Security Status:
        {% if is_state('alarm_control_panel.home', 'armed_away') %}
        ✅ Alarm is armed
        {% else %}
        ⚠️ Alarm is disarmed
        {% endif %}
mode: single
```

## Phone Number Format

Always use E.164 international format:

✅ **CORRECT:**
- +523349426465
- +5215551234567
- +14155552671

❌ **INCORRECT:**
- 3349426465 (missing country code)
- 52-334-942-6465 (hyphens not allowed)
- (334) 942-6465 (parentheses not allowed)

## Troubleshooting

### Services not appearing

1. Check that the integration is configured (Settings → Devices & Services)
2. Restart Home Assistant
3. Check logs: Settings → System → Logs
4. Verify integration loaded successfully in logs

### Messages not being delivered

1. Verify phone number format (E.164)
2. Check integration logs for errors
3. Verify API credentials are correct
4. Check ConvoChat account has sufficient credits
5. Test API credentials at https://convo.chat dashboard

### Authentication errors

1. Verify API Key is correct
2. Verify Account ID is correct
3. Check credentials at https://convo.chat dashboard
4. Ensure your ConvoChat account is active

## Support

- Integration Issues: https://github.com/RenatoAscencio/convochat-whatsapp-integration/issues
- ConvoChat API Documentation: https://sms.convo.chat/docs
- ConvoChat Support: https://convo.chat

## Migration from v1.x (Addon-based)

If you were using v1.x with the addon:

1. Uninstall the old integration (if installed)
2. **Keep the addon running** (for now, you can uninstall it after testing v2.0)
3. Install v2.0 from HACS
4. Configure with your API Key and Account ID
5. Test that messages work
6. Once confirmed working, you can uninstall the addon

## License

MIT License - see LICENSE file for details

## Credits

Developed by [@RenatoAscencio](https://github.com/RenatoAscencio)

Powered by [ConvoChat API](https://convo.chat)
