from mudserver.server import MudServer

class MyMudServer(MudServer):
    
    def update(self):
        super().update()
        # Game specific stuff that should happen after the main update

        send_greeting(self.new_connections)


def send_greeting(new_connections):
    # Need to load the greeting from database? Or config??
    pass
