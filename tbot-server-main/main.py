#!/usr/bin/env python3
import threading
import logging
from login_tcp_server import server as login_tcp_server
from ChannelServer import Server as ChannelServer
from RoomHostServer import Server as RoomHostServer
from GameServer import Server as GameServer
from relay_tcp_server import server as relay_tcp_server
from relay_udp_server import server as relay_udp_server

__author__ = "Icseon"
__version__ = "1.2"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(threadName)s] %(message)s'
)

def start_server(target, *args):
    """Helper to start a server in a thread with error handling."""
    def wrapper():
        try:
            target(*args)
        except Exception as e:
            logging.exception(f"Server crashed: {e}")
    thread = threading.Thread(target=wrapper)
    thread.daemon = True  # Allows program to exit even if threads are alive
    thread.start()
    return thread

def main():
    logging.info(f"T-Bot Rewritten Server version: {__version__}")

    # Relay TCP server
    relay_tcp = relay_tcp_server.RelayTCPServer(11004)
    start_server(relay_tcp.listen)

    # GameServer
    game_server = GameServer.Socket(11002, relay_tcp)
    start_server(game_server.listen)

    # Channel Server
    start_server(ChannelServer.Socket, 11010, game_server)

    # RoomHostServer
    room_host_server = RoomHostServer.Socket(11011, game_server)
    start_server(room_host_server.listen)

    # Relay UDP Server
    start_server(relay_udp_server.RelayUDPServer, 11013, relay_tcp, room_host_server)

    # Login Server runs on main thread
    try:
        login_tcp_server.LoginTCPServer(11000).listen()
    except Exception as e:
        logging.exception(f"LoginTCPServer crashed: {e}")

if __name__ == "__main__":
    main()
