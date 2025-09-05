import asyncio
import logging

from bleak import BleakClient, BleakScanner
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.sensor.const import TEMP_CELSIUS
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    _LOGGER.debug("Entering async_setup_entry; hass: %s entry: %s", hass, entry)
    """Set up AIBBQLife sensor from config entry."""
    device_name = entry.data["device_name"]
    char_uuid = entry.data["char_uuid"]
    sensor = AIBBQLifeTemperatureSensor(device_name, char_uuid)
    async_add_entities([sensor])


class AIBBQLifeTemperatureSensor(SensorEntity):
    """Representation of the AIBBQLife Temperature sensor."""

    def __init__(self, device_name, char_uuid):
        _LOGGER.debug("Entering __init__ function in AIBBQLifeTemperatureSensor; device: %s uuid: %s", device_name, char_uuid)
        self._attr_name = f"{device_name} Temperature"
        self._attr_native_unit_of_measurement = TEMP_CELSIUS
        self._attr_unique_id = f"{device_name.lower()}_temperature"
        self._attr_native_value = None
        self._device_name = device_name
        self._char_uuid = char_uuid
        self._client = None
        self._connected = False
        asyncio.create_task(self._scan_and_connect())

    async def _scan_and_connect(self):

        _LOGGER.debug("Entering _scan_and_connect")

        """Find device by name and connect."""
        while True:
            try:
                if not self._connected:
                    _LOGGER.info("Scanning for device named '%s'...", self._device_name)
                    device = await BleakScanner.find_device_by_filter(
                        lambda d, ad: d.name == self._device_name
                    )

                    if not device:
                        _LOGGER.warning("Device '%s' not found, retrying...", self._device_name)
                        await asyncio.sleep(5)
                        continue

                    _LOGGER.info("Found %s at %s", self._device_name, device.address)
                    self._client = BleakClient(device.address)

                    await self._client.connect()
                    self._connected = True
                    _LOGGER.info("Connected to %s", self._device_name)

                    await self._client.start_notify(self._char_uuid, self._notification_handler)

            except Exception as e:
                _LOGGER.error("BLE error: %s", e)
                self._connected = False
                if self._client:
                    try:
                        await self._client.disconnect()
                    except Exception:
                        pass
                await asyncio.sleep(5)  # retry after delay

            await asyncio.sleep(1)

    def _notification_handler(self, sender: int, data: bytearray):
        """Handle incoming BLE notifications."""
        if len(data) >= 2:
            temp_raw = data[-2]  # second-to-last byte
            self._attr_native_value = temp_raw
            _LOGGER.debug("Received temperature notification: %s °C", temp_raw)
            self.async_write_ha_state()
