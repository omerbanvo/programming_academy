import socket as s
import Enum_flags_class as enum
from pynput import mouse
from pynput import keyboard
from pynput.mouse import Button, Controller 
from pynput.keyboard import  Controller as kController
from PIL import ImageGrab
from PIL import Image
from io import BytesIO
import time
import threading

def send_exact(sock, msg_type, body):
    type_bytes = msg_type.value.to_bytes(1, "big")
    length_bytes = len(body).to_bytes(4, "big")
    full_message= type_bytes+length_bytes+body
    sock.sendall(full_message)



def take_screenshot(sock):
   
    while True:
        img_byte_arr = BytesIO()
        screenshot =ImageGrab.grab()
        screenshot = screenshot.convert("RGB")
        screenshot = screenshot.resize(size= (1280, 800))
        screenshot.save(img_byte_arr, format="JPEG")
        image_body = img_byte_arr.getvalue()
        send_exact(sock, enum.MsgType.image, image_body)
        time.sleep(0.1)
    pass
        
        
        

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
    mControll = mouse.Controller()


    screenshot_Thread = threading.Thread(target= take_screenshot, args= (client_sock, ))
    screenshot_Thread.start()
                

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

        if msg_type == enum.MsgType.mouse.value:
            if(body[0] == "c"):
                body_without_tag = body[1:]        
                data = body_without_tag.split(",")
                mposition = (float(data[0]), float(data[1]))
                mControll.position = mposition
                button_name = data[2][7:]
                mControll.click(button= getattr(Button, button_name))
            
            elif body[0] == "s":
                body_without_tag = body[1:]
                data = body_without_tag.split(",")
                mControll.scroll(float(data[0]), float(data[1])) 
            elif body[0] == "m":
                body_without_tag = body[1:]
                data = body_without_tag.split(",")
                mControll.position = (float(data[0]), float(data[1]))


           

if __name__ == "__main__":
    start_client()