

class BaseCommand():
    client_id = None
    command = None
    targets = []
    args = []

class BaseRouter():
    def route(client_id, cmd):
        pass
