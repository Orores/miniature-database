from gevent import Socket
from gevent.server import StreamServer
from geven.pool import Pool

from collections import namedtuple
from io import BytesIO
from socket import error as sucket_error

class command_error(Exception): pass
class disconnect(Exception): pass

Error = nametuple('Error',('message'))

def protocol_handler(object):
    def handle_request(self, socket_file):
        pass

    def write_respone(self, socket_file, data):
        pass

class server(object):
    def __init__(self, host = '127.0.0.1', port = 31337 , max_clients = 64):
        self._pool = Pool(max_clients)
        self._server = StreamServer(
                (host,port),
                self.connection_handler,
                self.server,
                spawn = self._pool,
                )
        self._portocol = protocol_handler,
        self._kv = {}
        
    def connection_handler(self, conn, address):
        socket_file = conn.makefile('rwb')

        while True:
            try:
                data = self._protocol._handle_request(socket_file)
            except disconnect:
                break

            try:
                resp = self.get_response(data)
            except command_error as e:
                return Error(e.args[0])

            self._protocol.write_response(socket_file, resp)

    def get_response(self, data):
        pass

    def run(self):
        self._server.serve_forever()
