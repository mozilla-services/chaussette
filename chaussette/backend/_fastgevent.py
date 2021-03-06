import socket
from gevent.wsgi import WSGIServer

import signal
from gevent import signal as gevent_signal
from chaussette.util import create_socket


class Server(WSGIServer):

    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM

    def __init__(self, listener, application=None, backlog=None,
                 spawn='default', log='default', handler_class=None,
                 environ=None, socket_type=socket.SOCK_STREAM,
                 address_family=socket.AF_INET, graceful_timeout=None,
                 disable_monkeypatch=False, **ssl_args):
        host, port = listener
        self.socket = create_socket(host, port, self.address_family,
                                    self.socket_type, backlog=backlog)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_address = self.socket.getsockname()

        if graceful_timeout is not None:
            self.stop_timeout = graceful_timeout
            gevent_signal(signal.SIGTERM, self.stop)

        super(Server, self).__init__(self.socket, application, None, spawn,
                                     log, handler_class, environ, **ssl_args)
