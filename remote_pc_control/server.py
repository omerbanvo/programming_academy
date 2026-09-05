import socket as s
import Enum_flags_class as enum
from pynput import mouse
from pynput import keyboard
import time

client_sock = None
def on_press(key):
    global client_sock
    try:
        key = key.char
    except AttributeError:
        key = key
    key_bytes = str(key).encode('utf-8')
    send_exact(client_sock, enum.MsgType.keyboard, key_bytes)
    
def on_release(key):
    try:
        key = key.char
    except AttributeError:
        key = key
    print(f"released: {key}")
    if key == keyboard.Key.esc:
        return False
       






def on_move(x, y):
    body = f"m{x},{y}".encode('utf-8')
    send_exact(client_sock, enum.MsgType.mouse, body)
    print(f"mouse moved to ({x, y})")

def on_click(x, y, button, pressed):
    global client_sock
    data_str = f"c{x},{y},{str(button)},{pressed}"
    body = data_str.encode("utf-8")
    send_exact(client_sock, enum.MsgType.mouse, body)
  

def on_scroll(x, y, dx, dy):
    global client_sock
    body = f"s{x},{dy}".encode('utf-8')
    send_exact(client_sock, enum.MsgType.mouse, body)



#function to send the exact type of information, and size
def send_exact(sock, msg_type, body):
    type_bytes = msg_type.value.to_bytes(1, "big")
    length_bytes = len(body).to_bytes(4, "big")
    full_message= type_bytes+length_bytes+body
    sock.sendall(full_message)


def start_server():
    global client_sock
    adress = ("10.100.102.36",8080)


    server_sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    server_sock.bind(adress)
    print("server waiting for connection....\nlistening on {}".format(adress))
    server_sock.listen(1)
    client_sock, client_adress = server_sock.accept()
    print("connection made with: {}".format(client_adress))

    lis =  keyboard.Listener(
    on_press= on_press, 
    on_release = on_release)
    lis.start()

    mlis = mouse.Listener(
    on_move = on_move, 
    on_click = on_click, 
    on_scroll = on_scroll)
    mlis.start()

    while True:
        time.sleep(1)

if __name__ == "__main__":
    start_server()

