import select
import socket
import time

from mudserver.client import MudClient

class MudServer():

    def __init__(self):
        self.buffer_size = 1024
        self.tick_length = 0.1
        self.port = 1234

        self.running = False
        self.clients = {}
        self._nextid = 0

    def _accept_new_connections(self):
        # 'select' is used to check whether there is data waiting to be read
        # from the socket. We pass in 3 lists of sockets, the first being those
        # to check for readability. It returns 3 lists, the first being
        # the sockets that are readable. The last parameter is how long to wait
        # - we pass in 0 so that it returns immediately without waiting
        rlist, wlist, xlist = select.select([self._listen_socket], [], [], 0)

        if self._listen_socket not in rlist:
            return

        conn, addr = self._listen_socket.accept()
        conn.setblocking(False)

        self.clients[self._nextid] = MudClient(conn, addr)
        self._nextid += 1

        print('New Connection')
        print(conn)

    def _check_for_disconnects(self):
        for client_id, client in list(self.clients.items()):
            # if we last checked less than 5 seconds ago, skip this client
            if time.time() - client.lastcheck < 5.0:
                continue
            
            # send invisible char to make sure the socket is writable
            client.lastcheck = time.time()
            # For some reason the first time doesn't always error
            self._send_message(client_id, '\x00')
            self._send_message(client_id, '\x00')

    def _get_messages(self):
        for client_id, client in self.clients.items():
            try:
                msg = client.socket.recv(self.buffer_size)
                if msg:
                    print(f'msg from {client.addr}: {msg}')
                    client.buffer = msg
            except BlockingIOError:
                pass

    def _send_message(self, client_id, msg):
        try:
            if not isinstance(msg, bytes):
                msg = bytes(msg, 'latin1')
            client = self.clients[client_id]
            client.socket.sendall(msg)
        except socket.error:
            # Some sort of notification that the client is disconnected
            del(self.clients[client_id])

    def start(self):
        print('Starting the MUD!')

        self._listen_socket = socket.socket()
        self._listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind the socket to all available listening addresses
        self._listen_socket.bind(("0.0.0.0", self.port))

        # set to non-blocking mode. This means that when we call 'accept', it
        # will return immediately without waiting for a connection
        self._listen_socket.setblocking(False)

        # start listening
        self._listen_socket.listen(1)
        self.running = True

    def stop(self):
        try:
            self.running = False
            self._listen_socket.close()
            print("Graceful shutdown complete")
        except Exception as err:
            print("Unable to shutdown gracefully")
            print(err)

    def update(self):
        self._accept_new_connections()
        self._get_messages()