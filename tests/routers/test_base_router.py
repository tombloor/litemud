import pytest
from pytest_mock import mocker

from litemud.routers import BaseRouter

def test_parse_single_command():
    command = 'help'
    router = BaseRouter()

    router.route(0, command)
    assert router._command.client_id == 0
    assert router._command.command == 'help'

