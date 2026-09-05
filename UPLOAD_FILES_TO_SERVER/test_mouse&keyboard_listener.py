from pynput import mouse
from pynput import keyboard
import time

def on_press(key):
    try:
        key = key.char
    except AttributeError:
        key = key
    print(f"pressed: {key}")
def on_release(key):
    try:
        key = key.char
    except AttributeError:
        key = key
    print(f"released: {key}")
    if key == keyboard.Key.esc:
        return False
       
lis =  keyboard.Listener(
    on_press= on_press, 
    on_release = on_release)

lis.start()





def on_move(x, y):
    print(f"mouse moved to ({x, y})")

def on_click(x, y, button, pressed):
    print("mouse clicked {0} on {1}".format("pressed" if pressed else 'Released', (x, y)))
  

def on_scroll(x, y, dx, dy):
    print("scrolled {} at {}.".format("down" if dy < 0 else "up", (x, y)))


mlis = mouse.Listener(
    on_move = on_move, 
    on_click = on_click, 
    on_scroll = on_scroll)
mlis.start()


while True:
    time.sleep(1)