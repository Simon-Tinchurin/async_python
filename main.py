import socket
import logging

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 5001))
server_socket.listen()

FORMAT = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
DATE_FORMAT = '%d.%m.%Y %I:%M:%S %p'
logging.basicConfig(filename='asinc_logs.log',
                    format=FORMAT,
                    datefmt=DATE_FORMAT,
                    level=logging.INFO)

while True:
    logging.info('Before .accept()')
    client_socket, addr = server_socket.accept()
    logging.info(f'Connection from: {addr}')

    while True:
        request = client_socket.recv(4096)

        if not request:
            break
        else:
            response = 'Something received\n'.encode()
            client_socket.send(response)
    logging.info('outside inner while loop')
    client_socket.close()
