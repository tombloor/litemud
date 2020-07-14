

class BaseCommand():
    client_id = None
    command = None
    targets = []
    args = []

class BaseRouter():
    def __init__(self, client_id=None, cmd=None):
        command = BaseCommand()
        command.client_id = client_id
        if cmd:
            #This needs to be a call to a parser??
            command.command = cmd
            #command.targets
            #command.args
        self._command = command

    def route(self, client_id, cmd):
        self._command = BaseCommand()
        self._command.client_id = client_id
        self._command.command = cmd

        # Need to be doing some parsing for args etc

