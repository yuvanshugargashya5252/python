import keyboard
import pyautogui
import time
import threading
import sys

messages = [
    " ",
    "  "
]

sending = False
num=1000

def send_messages():
    global sending , num
    sending = True
    time.sleep(1)
    while sending:
        for msg in messages:
            if not sending:
                break
            pyautogui.typewrite(msg)
            
            pyautogui.press('enter')
            # time.sleep(0.1)  # small delay between messages

def start_sending():
    thread = threading.Thread(target=send_messages)
    thread.daemon = True
    thread.start()
    print("Started sending messages... Press CTRL+SHIFT+S or ESC to stop.")

def stop_sending_and_exit():
    global sending
    sending = False
    print("Stopped sending messages and exiting.")
    sys.exit(0)

print("Waiting for hotkey: CTRL+SHIFT+M to start, CTRL+SHIFT+S or ESC to stop and exit.")

keyboard.add_hotkey('ctrl+shift+m', start_sending)
keyboard.add_hotkey('ctrl+shift+s', stop_sending_and_exit)
keyboard.add_hotkey('esc', stop_sending_and_exit)

keyboard.wait()  # Waits forever until a key triggers sys.exit()
