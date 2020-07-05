import time
import sys
from mudserver.server import MudServer


if __name__ == '__main__':
    # Getopt stuff to allow config path, default to 'server.config'
    server = MudServer()
    server.start()

    while server.running:
        try:
            time.sleep(server.tick_length)
            server.update()
        except KeyboardInterrupt:
            break
    server.stop()
    