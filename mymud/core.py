import time
import os
from mudserver.server import MudServer

DEFAULTS = {
    "TEST_MODE": os.getenv("TEST_MODE", 0),
    "logon_message": "Welcome to the server",
    "logoff_message": "Goodbye",
}


class MyMudCore:
    def __init__(self):
        self.server = MudServer()
        self.config = DEFAULTS.copy()
        self.commands = {}

    def load_config(self, config):
        self.config.update(config)

    def start(self):
        self.server.start()
        self.game_loop()

    def stop(self):
        self.server.stop()

    def game_loop(self):
        if not self.config["TEST_MODE"]:
            while self.server.running:
                try:
                    time.sleep(self.server.tick_length)
                    self.update()
                except KeyboardInterrupt:
                    break
            self.server.stop()

    def greet_new_connections(self):
        for i in range(len(self.server.new_connections)):
            client_id = self.server.new_connections.pop()
            self.server._send_message(client_id, self.config["logon_message"])

    def get_commands(self):
        for c_id, client in self.server.clients.items():
            if client.buffer[-2:] == "\r\n":
                self.commands[c_id] = client.buffer[:-2]
                client.buffer = ""

    def update(self):
        self.server.update()
        self.greet_new_connections()
        self.get_commands()
        
        for client_id, cmd in self.commands.items():
            router = BaseRouter().route(client_id, cmd)
            # Returns the router for the command
            # Should then call the command via the router??

