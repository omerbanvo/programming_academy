from pynput.mouse import Button, Controller
from pynput.keyboard import  Controller as mController
mouse = Controller()
keyboard = mController()

def move_mouse(x, y):
    mouse.move(x, y)

def click_mouse(button):
    mouse.press(button)
    mouse.release(button)


def scroll_mouse(dx, dy):
    mouse.scroll(dx, dy)

move_mouse(300, 300)
click_mouse(Button.left)
scroll_mouse(0, 2)


def click_keyboard(key):
    keyboard.press(key)
    keyboard.release(key)


click_keyboard("a")