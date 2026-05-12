import keyboard
import time

def inject(text: str):
    if not text:
        return

    print(f"[injector] injecting: {text}")

    time.sleep(0.5)  # bumped from 0.3

    keyboard.write(text, delay=0.05)  # bumped from 0.01
    print("[injector] done.")