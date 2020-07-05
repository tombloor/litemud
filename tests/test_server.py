import pytest
import socket
import datetime
import time

from mudserver.server import MudServer

@pytest.fixture
def mock_server():
    s = MudServer()
    s.start()
    yield s
    s.stop()

@pytest.fixture
def mock_client(mock_server):
    c = socket.socket()
    c.connect(('127.0.0.1', mock_server.port))
    mock_server._accept_new_connections()
    yield c
    c.close()

def test_server_runs(mock_server):
    assert mock_server.running

    fake_client = socket.socket()
    fake_client.connect(('127.0.0.1', mock_server.port))
    # This proves the socket is open

def test_server_connect_client(mock_server):
    fake_client = socket.socket()
    fake_client.connect(('127.0.0.1', mock_server.port))

    mock_server._accept_new_connections()

    assert len(mock_server.clients) == 1

def test_server_disconnect_client(mock_server, mock_client):
    mock_client.shutdown(socket.SHUT_RDWR)
    mock_client.close()
    
    mock_update_time = datetime.datetime.now() - datetime.timedelta(seconds=5)
    mock_server.clients[0].lastcheck = mock_update_time.timestamp()

    mock_server._check_for_disconnects()
    assert len(mock_server.clients.keys()) == 0

def test_server_receive_message(mock_server, mock_client):
    data = b'hello, world!'
    assert mock_server.clients[0].buffer is None

    mock_client.sendall(data)

    mock_server._get_messages()

    assert mock_server.clients[0].buffer == data

def test_server_send_message(mock_server, mock_client):
    data = b'hello, world!'
    client_id = 0

    mock_server._send_message(client_id, data)
    recved = mock_client.recv(mock_server.buffer_size)

    assert recved == data

def test_server_send_large_message(mock_server, mock_client):
    data = b'ab' * 1024
    client_id = 0
    mock_server._send_message(client_id, data)

    chunk1 = mock_client.recv(mock_server.buffer_size)
    assert chunk1 == data[0:mock_server.buffer_size]

    chunk2 = mock_client.recv(mock_server.buffer_size)
    assert chunk2 == data[mock_server.buffer_size:]
