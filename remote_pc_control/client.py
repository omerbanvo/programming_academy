import socket as s
import Enum_flags_class as enum
from pynput import mouse
from pynput import keyboard
from pynput.mouse import Button, Controller 
from pynput.keyboard import  Controller as kController



def recv_exact(sock,num_bytes ):
    final = b""
    while len(final)< num_bytes:
        chunk = sock.recv(num_bytes - len(final))
        if not chunk:
            raise ConnectionError("socket closed before recievig all the information")
        final+=chunk
    return final

def start_client():
    adress = ("10.100.102.34", 8080)
    client_sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    print(f"connecting to server on- {adress}")
    client_sock.connect(adress)
    kControll = keyboard.Controller()
    while True:
        header = recv_exact(client_sock, 5)
        type_bytes = header[0:1]
        length_bytes = header[1:5]
        length = int.from_bytes(length_bytes, "big")
        body = recv_exact(client_sock, length).decode('utf-8')
        msg_type = int.from_bytes(type_bytes, "big")
        if  msg_type == enum.MsgType.keyboard.value:
            
            if body[0:3] == "Key":
                try:
                    special_key = body[4:]
                    key = getattr(keyboard.Key, special_key)
                except:
                    print(f"no such key as {special_key}.")
                    raise TypeError
                    
            else:
                key = body

            kControll.press(key)
            kControll.release(key)



        elif msg_type == enum.MsgType.mouse.value:
            pass 

if __name__ == "__main__":
    start_client()