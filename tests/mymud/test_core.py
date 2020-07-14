import pytest
from pytest_mock import mocker

from mudserver.server import MudServer
from mudserver.client import MudClient
from mymud.core import MyMudCore


@pytest.fixture
def mock_core():
    c = MyMudCore()
    c.start()
    yield c
    c.stop()

def test_core_start_server(mock_core, mocker):
    mock_start = mocker.patch("mudserver.server.MudServer.start")
    mock_loop = mocker.patch("mymud.core.MyMudCore.game_loop")

    mock_core.start()
    mock_start.assert_called_once()
    mock_loop.assert_called_once()


def test_core_stop_server(mock_core, mocker):
    mock_stop = mocker.patch("mudserver.server.MudServer.stop")
    mock_core.stop()
    mock_stop.assert_called_once()


def test_core_load_config(mock_core):
    config = {"logon_message": "Test"}
    mock_core.load_config(config)
    assert mock_core.config["logon_message"] == "Test"


def test_core_default_config(mock_core):
    expected_logon = "Welcome to the server"
    expected_logoff = "Goodbye"
    config = {"logon_message": "Test"}

    assert mock_core.config["logon_message"] == expected_logon
    mock_core.load_config(config)
    assert mock_core.config["logon_message"] == config["logon_message"]
    assert mock_core.config["logoff_message"] == expected_logoff


def test_core_new_connection_greeting(mock_core, mocker):
    mock_send = mocker.patch("mudserver.server.MudServer._send_message")

    config = {"logon_message": "This is a test"}
    mock_core.load_config(config)
    mock_core.server.new_connections.append(0)

    mock_core.greet_new_connections()

    mock_send.assert_called_once_with(0, config["logon_message"])


def test_core_get_commands(mock_core):
    test_command = 'say "hello, world!"\r\n'
    mock_client = MudClient(None, None)
    mock_client.buffer = test_command
    mock_core.server.clients[0] = mock_client

    mock_core.get_commands()
    assert mock_core.commands[0] == 'say "hello, world!"'


def test_core_call_router(mock_core, mocker):
    mock_router = mocker.patch('mymud.routers.BaseRouter.route')
    test_command = 'say "hello, world!"'

    mock_core.commands[0] = test_command
    mock_core.update()

    mock_router.assert_called_once_with(0, test_command)

