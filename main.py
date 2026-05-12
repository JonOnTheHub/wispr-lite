import threading
import time
import os
import sys
from pynput import keyboard as pynput_keyboard
import pystray
from PIL import Image, ImageDraw

from recorder import Recorder
from transcriber import transcribe
from cleaner import clean
from injector import inject
from config import AI_CLEANUP

# --- Single instance lock ---
LOCK_FILE = os.path.join(os.environ.get("TEMP", "."), "wispr-lite.lock")

def acquire_lock():
    if os.path.exists(LOCK_FILE):
        print("[main] already running. exiting.")
        sys.exit(0)
    with open(LOCK_FILE, "w") as f:
        f.write(str(os.getpid()))

def release_lock():
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)

import atexit
atexit.register(release_lock)

# --- State ---
recorder = Recorder()
is_recording = False
tray_icon = None
press_time = None
hold_timer = None
HOLD_THRESHOLD = 0.3

# --- Tray Icon ---
def make_icon(color):
    img = Image.new("RGB", (64, 64), color=color)
    draw = ImageDraw.Draw(img)
    draw.ellipse((16, 16, 48, 48), fill="white")
    return img

def set_tray(color, title):
    global tray_icon
    if tray_icon:
        tray_icon.icon = make_icon(color)
        tray_icon.title = title

# --- Core flow ---
def process_audio():
    audio_path = recorder.stop()

    if not audio_path:
        set_tray("#2ecc71", "Wispr Lite — Ready")
        return

    try:
        transcript = transcribe(audio_path)

        if not transcript:
            set_tray("#2ecc71", "Wispr Lite — Ready")
            return

        result = clean(transcript) if AI_CLEANUP else transcript
        inject(result)

    except Exception as e:
        print(f"[main] error: {e}")
        set_tray("#e67e22", "Wispr Lite — Error!")

    finally:
        recorder.cleanup(audio_path)
        set_tray("#2ecc71", "Wispr Lite — Ready")

def start_recording():
    global is_recording
    if not is_recording:
        is_recording = True
        print("[main] recording started")
        set_tray("#e74c3c", "Wispr Lite — Recording...")
        recorder.start()

def on_press(key):
    global press_time, hold_timer
    if key == pynput_keyboard.Key.caps_lock and not is_recording and press_time is None:
        press_time = time.time()
        hold_timer = threading.Timer(HOLD_THRESHOLD, start_recording)
        hold_timer.start()

def on_release(key):
    global is_recording, press_time, hold_timer
    if key == pynput_keyboard.Key.caps_lock:
        if hold_timer:
            hold_timer.cancel()
            hold_timer = None
        press_time = None

        if is_recording:
            is_recording = False
            print("[main] recording stopped, processing...")
            set_tray("#f39c12", "Wispr Lite — Processing...")
            threading.Thread(target=process_audio).start()
        else:
            print("[main] tap ignored — too short")

def quit_app(icon, item):
    release_lock()
    icon.stop()
    os._exit(0)

# --- tray setup ---
def run_tray():
    global tray_icon
    menu = pystray.Menu(
        pystray.MenuItem("Wispr Lite", lambda: None, enabled=False),
        pystray.MenuItem("Quit", quit_app)
    )
    tray_icon = pystray.Icon(
        "wispr-lite",
        make_icon("#2ecc71"),
        "Wispr Lite — Ready",
        menu
    )
    tray_icon.run()

# --- entry point ---
if __name__ == "__main__":
    acquire_lock()
    print("[main] Wispr Lite starting...")
    print("[main] Hold Caps Lock to record. Release to transcribe.")

    tray_thread = threading.Thread(target=run_tray, daemon=True)
    tray_thread.start()

    time.sleep(1)

    with pynput_keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()