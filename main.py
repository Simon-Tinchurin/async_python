import socket
import logging
import selectors


# to see which ports are in use: netstat -tuln

selector = selectors.DefaultSelector()

FORMAT = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
DATE_FORMAT = '%d.%m.%Y %I:%M:%S %p'
logging.basicConfig(filename='async_logs.log',
                    format=FORMAT,
                    datefmt=DATE_FORMAT,
                    level=logging.INFO)


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5000))
    server_socket.listen()

    selector.register(fileobj=server_socket,
                      events=selectors.EVENT_READ,
                      data=accept_connection)


def accept_connection(server_socket):
    logging.info('Inside accept_connection func')
    client_socket, addr = server_socket.accept()
    logging.info(f'Connection from: {addr}')

    selector.register(fileobj=client_socket,
                      events=selectors.EVENT_READ,
                      data=send_message)


def send_message(client_socket):
    logging.info('inside send_message func')
    request = client_socket.recv(4096)

    if request:
        response = 'Something received\n'.encode()
        logging.info(f'received {request.decode()}')
        client_socket.send(response)
    else:
        logging.info(f'closing socket {client_socket}')
        selector.unregister(client_socket)
        client_socket.close()


def event_loop():
    while True:
        # (key, events)
        events = selector.select()
        for key, _ in events:
            callback = key.data
            callback(key.fileobj)


if __name__ == '__main__':
    server()
    event_loop()
