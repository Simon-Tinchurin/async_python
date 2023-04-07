import socket
import logging
from select import select

# to see which ports are in use: netstat -tuln

FORMAT = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
DATE_FORMAT = '%d.%m.%Y %I:%M:%S %p'
logging.basicConfig(filename='async_logs.log',
                    format=FORMAT,
                    datefmt=DATE_FORMAT,
                    level=logging.INFO)

tasks = []

to_read = {}
to_write = {}


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5000))
    server_socket.listen()

    while True:
        yield ('read', server_socket)
        client_socket, addr = server_socket.accept()
        logging.info(f'Connection from {addr}')
        tasks.append(client(client_socket))


def client(client_socket):
    while True:
        yield ('read', client_socket)
        request = client_socket.recv(4096)
        if not request:
            break
        else:
            response = 'Something received\n'.encode()
            yield ('write', client_socket)
            logging.info(f'Received {request} from {client_socket}')
            client_socket.send(response)
    client_socket.close()


def event_loop():
    while any([tasks, to_read, to_write]):
        while not tasks:
            ready_to_read, ready_to_write, _ = select(to_read, to_write, [])
            for sock in ready_to_read:
                tasks.append(to_read.pop(sock))
            for sock in ready_to_write:
                tasks.append(to_write.pop(sock))
        try:
            task = tasks.pop(0)
            sign, sock = next(task)
            if sign == 'read':
                to_read[sock] = task
            if sign == 'write':
                to_write[sock] = task
        except StopIteration:
            logging.info('all done')


tasks.append(server())
event_loop()