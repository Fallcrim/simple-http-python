import socket
import logging
from threading import Thread

import jinja2

from utils import parse_message, build_response
from core import HTTPRequest


class Webserver:
    logger = logging.getLogger("Webserver")
    logger.setLevel(logging.DEBUG)

    def __init__(self) -> None:
        """Constructor for Webserver class"""
        self.server_socket = None
        self.connected_clients = []
        self._routes = {}
        self.config = {}
        self._jinja_env = None

    def run(self, host: str = "localhost", port: int = 8000) -> None:
        """Starts the Webserver

        Args:
            host (str): host to run on
            port (int): port to run on
        """
        self.server_socket: socket.socket = socket.create_server((host, port))
        self.server_socket.listen()
        self.logger.info(f"Listening on {host}:{port}")
        self._jinja_env = jinja2.Environment(autoescape=True, loader=jinja2.FileSystemLoader("templates"))
        self.handle_requests()

    def handle_requests(self) -> None:
        """Handles all incoming requests and creates seperate threads for each client."""
        while True:
            client_socket, client_address = self.server_socket.accept()
            self.logger.debug(f"Accepted connection from {client_address}")
            self.logger.debug(f"Starting client handler thread for {client_address}")
            Thread(
                target=self.handle_client,
                args=(client_socket, client_address, self.logger),
            ).start()

    def handle_client(
        self, client_socket: socket, client_address: tuple, logger: logging.Logger
    ) -> None:
        """Method te handle client requests; thread target.

        Args:
            client_socket (socket): socket of the handled client
            client_address (tuple): address of the handled client
            logger (logging.Logger): logger for the client handler thread
        """
        logger.debug(f"Started client handler thread for {client_address}")
        request = client_socket.recv(1024)
        if not request:
            return
        try:
            message: HTTPRequest = parse_message(request, client_socket, client_address)
            if message.method not in self._routes[message.path]["methods"]:
                logger.error(f"Method {message.method} not allowed for {message.path}")
                client_socket.send(b"HTTP/1.1 405 Method Not Allowed\r\n\r\n")
                client_socket.close()
                return

            ret = self._routes[message.path]["callback"](message)
            if isinstance(ret, str):
                response = build_response(200, body=ret)
            elif isinstance(ret, bytes):
                response = ret
            else:
                response = build_response(**ret.__dict__)

            client_socket.send(response)
            client_socket.close()

        except ValueError:
            logger.error(f"Bad request from {client_address}")
            client_socket.send(b"HTTP/1.1 400 Bad Request\r\n\r\n")
            client_socket.close()
            return

        except KeyError:
            logger.error(f"Page for {message.path} not found from {client_address}")
            client_socket.send(b"HTTP/1.1 404 Page Not Found\r\n\r\n")
            client_socket.close()
            return

        # except Exception as e:
        #     logger.error(f"Failed to parse message from {client_address}")
        #     logger.error(e)
        #     client_socket.send(b"HTTP/1.1 500 Internal Server Error\r\n\r\n")
        #     client_socket.close()
        #     return

    def route(self, path: str, allowed_methods: list) -> callable:
        """Maps a route to a function

        Args:
            path (str): path to map to
            allowed_methods (list): list of allowed http methods

        Returns:
            callable: decorator function
        """

        def decorator(func: callable) -> callable:
            self._routes[path] = {"methods": allowed_methods, "callback": func}
            self.logger.debug(f"Registered route {path}")
            return func

        return decorator
