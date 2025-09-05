# AIBBQLife Sensor Integration for Home Assistant

Custom integration to read temperature from the AIBBQLife Bluetooth sensor.

## Installation (via HACS)
1. Add this repository as a **Custom Repository** in HACS → Integrations.
2. Install "AIBBQLife Sensor".
3. Restart Home Assistant.
4. Go to **Settings → Devices & Services → Add Integration → AIBBQLife**.
5. Enter your device name (default: `AIBBQLife`) and the characteristic UUID.

## Features
- Connects automatically to device by name
- Subscribes to BLE notifications
- Exposes temperature as `sensor.aibbqlife_temperature`
