import socket as s
import Enum_flags_class as enum
from pynput import mouse
from pynput import keyboard
import time
import io 
from PIL import Image
import threading
import cv2
import numpy



client_sock = None
latest_image = None


def recv_exact(sock, num_bytes):
    buffer = b""
    while len(buffer)<num_bytes:
        chunk = sock.recv(num_bytes - len(buffer))
        if not chunk:
            raise ConnectionError("socket closed before recievig all the information")
        buffer+= chunk
    return buffer

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
    body = f"s{dx},{dy}".encode('utf-8')
    send_exact(client_sock, enum.MsgType.mouse, body)



#function to send the exact type of information, and size
def send_exact(sock, msg_type, body):
    type_bytes = msg_type.value.to_bytes(1, "big")
    length_bytes = len(body).to_bytes(4, "big")
    full_message= type_bytes+length_bytes+body
    with send_lock:
        sock.sendall(full_message)








def recieve_images(sock):
    global latest_image
    while True:
        img_bytes_arr = io.BytesIO()
        header = recv_exact(sock, 5)
        header = header[1:5] #remove the tag, it has to be an image 
        length = int.from_bytes(header[0:], "big")
        img_bytes = recv_exact(sock, length)
        img_bytes_arr = io.BytesIO(img_bytes)
        screenshot = Image.open(img_bytes_arr)
        latest_image = screenshot

        







send_lock = threading.Lock()


def start_server():
    global client_sock
    global latest_image
    adress = ("10.100.102.36",8080)


    server_sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    server_sock.bind(adress)
    print("server waiting for connection....\nlistening on {}".format(adress))
    server_sock.listen(1)
    client_sock, client_adress = server_sock.accept()
    print("connection made with: {}".format(client_adress))
    recieve_screenshots = threading.Thread(target= recieve_images, args= (client_sock, ))
    recieve_screenshots.start()
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
        if latest_image is not None:
            img_array = numpy.array(latest_image)
            img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            cv2.imshow("Remote Screen", img_bgr)
            cv2.waitKey(1)
        time.sleep(0.05)  # קצב בדיקה, לא חייב 1 שנייה כמו קודם

if __name__ == "__main__":
    start_server()

