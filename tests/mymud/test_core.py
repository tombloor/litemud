import pytest
from pytest_mock import mocker
from mudserver.server import MudServer
from mymud.core import MyMudServer

def test_core_update_calls_super(mocker):
    super_update = mocker.patch('mudserver.server.MudServer.update')

    server = MyMudServer()
    server.update()
    super_update.assert_called_once()

@pytest.mark.skip
def test_core_new_connection_greeting():
    pass

@pytest.mark.skip
def test_core_call_parser():
    pass
    # This should call a parser on the sent command from each client
    