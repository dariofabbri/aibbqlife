import voluptuous as vol
from homeassistant import config_entries

from .const import DOMAIN

DATA_SCHEMA = vol.Schema({
    vol.Required("device_name", default="AIBBQLife"): str,
    vol.Required("char_uuid", default="bf83f3f2-399a-414d-9035-ce64ceb3ff67"): str,
})

class AIBBQLifeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for AIBBQLife integration."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        _LOGGER.debug("Starting async_step_user with input: %s", user_input)
        """Handle the initial step."""
        if user_input is not None:
            _LOGGER.debug("Creating config entry with data: %s", user_input)
            return self.async_create_entry(title=user_input["device_name"], data=user_input)

        return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA)
