import socket
import logging
from select import select


# to see which ports are in use: netstat -tuln

to_monitor = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 5000))
server_socket.listen()

FORMAT = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
DATE_FORMAT = '%d.%m.%Y %I:%M:%S %p'
logging.basicConfig(filename='async_logs.log',
                    format=FORMAT,
                    datefmt=DATE_FORMAT,
                    level=logging.INFO)


def accept_connection(server_socket):
    logging.info('Inside accept_connection func')
    client_socket, addr = server_socket.accept()
    logging.info(f'Connection from: {addr}')
    to_monitor.append(client_socket)


def send_message(client_socket):
    logging.info('inside send_message func')
    request = client_socket.recv(4096)

    if request:
        response = 'Something received\n'.encode()
        logging.info(f'received {request.decode()}')
        client_socket.send(response)
    else:
        logging.info(f'closing socket {client_socket}')
        client_socket.close()


def event_loop():
    while True:
        # read, write, errors
        ready_to_read, _, _ = select(to_monitor, [], [])
        for sock in ready_to_read:
            if sock is server_socket:
                accept_connection(sock)
            else:
                send_message(sock)


if __name__ == '__main__':
    to_monitor.append(server_socket)
    event_loop()
