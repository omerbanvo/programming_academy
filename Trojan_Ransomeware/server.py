import socket
import ssl
from Crypto.Random import get_random_bytes
from  encryptor import *

adress = ("127.0.0.1", 31337)
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain("server.crt", "server.key")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(adress)
    print(f"server is listening on {adress}")
    server_socket.listen(5)
    while True:
        connection, conadd = server_socket.accept()
        print(f"connection made with {conadd}")
        key = get_random_bytes(32)
        with context.wrap_socket(connection, server_side= True) as ssock:
            cipher = AESCipher(key)
            ssock.send(key)
            

start_server()