import socket
import ssl
from encryptor import *

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
context.load_verify_locations("server.crt")

adress = ("127.0.0.1", 31337)

def recv_exact(sock, num_bytes):
    buffer = b""
    while len(buffer)<num_bytes:
        chunk = sock.recv(num_bytes - len(buffer))
        if not chunk:
            raise ConnectionError("connection faild\nconnection stopped unexpectedly before recieveing expected data ")
        buffer+=chunk
        
def start_client():
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    with context.wrap_socket(client_sock, server_hostname= "localhost") as ssock:
        ssock.connect(adress)
        key = recv_exact(ssock, 32)
        cipher = AESCipher(key)

start_client()