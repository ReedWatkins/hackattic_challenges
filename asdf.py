from pynput.keyboard import Key, Controller
import time

keys = Controller()

keys.type("Hello World")
keys.press(Key.enter)
keys.release(Key.enter)
time.sleep(2)

