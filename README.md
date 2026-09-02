# wispr-lite

A lean, zero-cost Wispr Flow alternative for Windows. Hold Caps Lock, speak, release — your words appear wherever your cursor is. Built on Groq's free tier so it costs nothing to run.

An MVP. It works. Not quite pretty yet but yeah.

---

## How it works

Hold Caps Lock (for ~0.3s) → speak → release → text types itself into whatever window you're in.

Under the hood: your mic audio goes to Groq Whisper for transcription, then to LLaMA 3.3 for light cleanup (filler words, punctuation, grammar), then `keyboard.write()` injects it at your cursor.

Two API calls per use. Combined cost is fractions of a cent per session. On Groq's free tier, you'll likely never hit the rate limit at normal usage pace. NORMAL USAGE PACE

---

## Requirements

- Windows 10 or 11
- A Groq API key — free, no card needed: [console.groq.com](https://console.groq.com)

That's it for the exe version. No Python required.

---

## Installation

### Option A: Run the exe (easiest)

1. Download `wispr-lite.exe` from [Releases](../../releases)
2. Copy `config.example.py`, rename it to `config.py`
3. Open `config.py` and paste your Groq API key
4. Double-click `wispr-lite.exe`

Green dot in your system tray means it's running.

### Option B: Run from source

You'll need Python 3.10, 3.11, or 3.12. (3.14 has known venv issues — avoid it.)

```bash
git clone https://github.com/JonOnTheHub/wispr-lite.git
cd wispr-lite
python -m venv venv
source venv/Scripts/activate   # Git Bash
# or: venv\Scripts\activate    # CMD / PowerShell
pip install -r requirements.txt
cp config.example.py config.py
```

Open `config.py`, add your Groq API key, then:

```bash
python main.py
```

### Option C: Run without a terminal (bat file)

After Option B setup, just double-click `start.bat`. No terminal window, no fuss — same as the exe but runs from source.

---

## Usage

| Action                 | Result                                |
| ---------------------- | ------------------------------------- |
| Hold Caps Lock (~0.3s) | Recording starts, tray turns red      |
| Release Caps Lock      | Processing, tray turns yellow         |
| Done                   | Text typed at cursor, tray goes green |
| Quick tap Caps Lock    | Ignored                               |

## Startup on boot

Right-click the tray icon and click "Launch at startup" to register wispr-lite with Windows. 
A checkmark confirms it's enabled. From that point, it launches automatically whenever you log in — no manual launch needed.

To disable, click "Launch at startup" again. The checkmark disappears and the registry entry is removed.

---

## Config

Everything is in `config.py`:

```python
GROQ_API_KEY = "..."            # your key
HOLD_KEY = "caps_lock"          # trigger key
WHISPER_MODEL = "whisper-large-v3-turbo"
LLM_MODEL = "llama-3.3-70b-versatile"
AI_CLEANUP = True               # set False to skip LLM, inject raw transcript
```

`AI_CLEANUP = False` skips the LLaMA pass entirely and injects raw Whisper output — useful if you want zero latency or Groq is slow.

---

## Maintenance

**Auth errors** — your API key was revoked. Generate a new one at [console.groq.com/keys](https://console.groq.com/keys) and update `config.py`.

**Model not found error** — Groq occasionally retires models. Check current IDs at [console.groq.com/docs/models](https://console.groq.com/docs/models) and update `config.py`.

**Garbled text injection** — increase the typing delay in `injector.py`:

```python
keyboard.write(text, delay=0.08)
```

Older machines sometimes need more breathing room between keystrokes.

**Usage limits** — Groq's free tier resets daily. Check your usage at [console.groq.com](https://console.groq.com). At normal dictation pace you won't get close.

---

## Building the exe yourself

```bash
source venv/Scripts/activate
pip install pyinstaller
pyinstaller --noconsole --onefile --name wispr-lite main.py
```

Output lands in `dist/wispr-lite.exe`. Your `config.py` (including the API key) gets bundled in — don't share that build publicly.

---

## Known issues

- Caps Lock still toggles while the app is running
- Requires internet for every transcription  
- Not tested on Python 3.13+

---

## Stack

- [Groq](https://groq.com) — Whisper large-v3-turbo + LLaMA 3.3 70b
- [sounddevice](https://python-sounddevice.readthedocs.io) — mic capture
- [pynput](https://pynput.readthedocs.io) — hotkey detection
- [keyboard](https://github.com/boppreh/keyboard) — text injection
- [pystray](https://github.com/moses-palmer/pystray) — system tray