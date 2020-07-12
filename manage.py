import time
import sys
from mymud.core import MyMudCore

CONFIG = {"logon_message": "Welcome to myMud server"}

if __name__ == "__main__":
    # Getopt stuff to allow config path, default to 'server.config'
    mud = MyMudCore()
    mud.load_config(CONFIG)
    mud.start()
