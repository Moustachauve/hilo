"""Fixtures for testing."""

import json
import pytest
from unittest.mock import patch, MagicMock, AsyncMock, PropertyMock
from collections.abc import Generator
from homeassistant.core import HomeAssistant
from pyhilo.websocket import WebsocketClient
from pytest_homeassistant_custom_component.common import (
    MockConfigEntry,
    load_fixture,
)

from custom_components.hilo.const import DOMAIN


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    """Enable custom integrations."""
    return


@pytest.fixture
def entity_registry_enabled_by_default() -> Generator[None]:
    """Test fixture that ensures all entities are enabled in the registry."""
    with patch(
        "homeassistant.helpers.entity.Entity.entity_registry_enabled_default",
        return_value=True,
    ):
        yield


@pytest.fixture
def mock_config_entry() -> MockConfigEntry:
    """Return the default mocked config entry."""
    return MockConfigEntry(
        domain=DOMAIN,
        data={"auth_implementation": "hilo", "token": "123"},
        unique_id="hilo",
        version=2,
    )


@pytest.fixture
def mock_setup_entry() -> Generator[AsyncMock]:
    """Mock setting up a config entry."""
    with patch(
        "custom_components.hilo.async_setup_entry", return_value=True
    ) as mock_setup:
        yield mock_setup


@pytest.fixture
def mock_onboarding() -> Generator[MagicMock]:
    """Mock that Home Assistant is currently onboarding."""
    with patch(
        "homeassistant.components.onboarding.async_is_onboarded",
        return_value=False,
    ) as mock_onboarding:
        yield mock_onboarding


@pytest.fixture
def mock_api() -> Generator[MagicMock]:
    """Return a mocked Hilo API"""
    with patch("pyhilo.API", autospec=True) as api_mock:
        # Mock websocket methods to prevent indefinite blocking
        api_mock.websocket_devices = AsyncMock(spec=WebsocketClient)
        api_mock.websocket_devices.async_connect = AsyncMock(return_value=None)
        api_mock.websocket_devices.async_listen = AsyncMock(return_value=None)
        api_mock.websocket_challenges = AsyncMock(spec=WebsocketClient)
        api_mock.websocket_challenges.async_connect = AsyncMock(return_value=None)
        api_mock.websocket_challenges.async_listen = AsyncMock(return_value=None)

        api_mock.log_traces = True
        api_mock.get_devices.return_value = json.loads(load_fixture("all_devices.json"))
        api_mock.async_create.return_value = api_mock
        yield api_mock


@pytest.fixture(autouse=True)
def mock_network_calls() -> Generator[None]:
    """Mock network calls to prevent SocketBlockedError."""
    with (
        patch("homeassistant.helpers.aiohttp_client.async_get_clientsession"),
        patch("asyncio.BaseEventLoop.create_connection"),
        patch("aiohappyeyeballs.impl.start_connection"),
        patch("custom_components.hilo.GraphQlHelper") as mock_graphql_cc,
        patch("pyhilo.graphql.GraphQlHelper") as mock_graphql_pyhilo,
    ):
        mock_graphql_cc.return_value.async_init = AsyncMock()
        mock_graphql_cc.return_value.subscribe_to_device_updated = AsyncMock()
        mock_graphql_pyhilo.return_value.async_init = AsyncMock()
        mock_graphql_pyhilo.return_value.subscribe_to_device_updated = AsyncMock()
        yield


@pytest.fixture
async def init_integration(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_api: MagicMock,
) -> MockConfigEntry:
    """Set up the Hilo integration for testing."""
    mock_config_entry.add_to_hass(hass)

    with (
        patch("custom_components.hilo.API.async_create", return_value=mock_api),
        patch(
            "custom_components.hilo.Hilo.should_websocket_reconnect",
            new_callable=PropertyMock,
        ) as mock_should_websocket_reconnect,
    ):
        mock_should_websocket_reconnect.return_value = False
        await hass.config_entries.async_setup(mock_config_entry.entry_id)
        await hass.async_block_till_done()

        return mock_config_entry
