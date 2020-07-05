import time

class MudClient:
    socket = None
    addr = None
    buffer = None
    lastcheck = None

    def __init__(self, socket, addr, buffer=None):
        self.socket = socket
        self.addr = addr
        self.buffer = buffer
        self.lastcheck = time.time()
