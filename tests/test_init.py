"""Test component setup."""

from unittest.mock import MagicMock, patch, AsyncMock, PropertyMock

import pytest
from homeassistant.setup import async_setup_component
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.hilo.const import DOMAIN


@pytest.fixture(autouse=True)
def mock_api():
    """Return a mocked Hilo API"""
    with patch("custom_components.hilo.API") as api_mock:
        api_mock.async_create.return_value = AsyncMock()
        yield api_mock

@pytest.fixture(autouse=True)
def mock_graphql_helper():
    with patch("custom_components.hilo.GraphQlHelper") as mock:
        mock.return_value.async_init = AsyncMock()
        mock.return_value.subscribe_to_device_updated = AsyncMock()
        yield mock

@pytest.fixture(autouse=True)
def mock_aiohttp_client():
    with patch("homeassistant.helpers.aiohttp_client.async_get_clientsession") as mock:
        mock.return_value = AsyncMock()
        yield mock

@pytest.fixture(autouse=True)
def mock_websocket_reconnect():
    with patch(
        "custom_components.hilo.Hilo.should_websocket_reconnect",
        new_callable=PropertyMock,
    ) as mock:
        mock.return_value = False
        yield mock

async def test_async_setup(hass, mock_api, mock_graphql_helper, mock_aiohttp_client, mock_websocket_reconnect):
    """Test the component gets setup."""
    assert await async_setup_component(hass, DOMAIN, {}) is True
