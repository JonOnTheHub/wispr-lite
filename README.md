# wispr-lite

Hold Caps Lock, speak, release. Your words appear wherever your cursor is.

No subscription. No Electron app eating RAM. No Mac-only nonsense. Just a tray icon, a hotkey, and Groq's free tier doing the work.

This is an MVP — built in a day, ships as a single exe.

---

## How it works

Hold Caps Lock for ~0.3 seconds to start recording. Release to stop. wispr-lite sends the audio to Groq Whisper for transcription, runs it through an LLM for light cleanup (punctuation, filler words, grammar), then types the result directly into whatever window has focus.

Works in any app — browsers, VS Code, Notepad, chat apps, anything with a text cursor.

Two API calls per session. Combined cost: fractions of a cent. On Groq's free tier, you'll likely never hit the daily limit at normal dictation pace.

---

## Requirements

- Windows 10 or 11
- A Groq API key — free, no card needed: [console.groq.com](https://console.groq.com)

No Python required for the exe version.

---

## Installation

### Option A: exe (easiest)

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

### Option C: No terminal (bat file)

After Option B setup, double-click `start.bat`. Runs silently in the background — no terminal window.

---

## Usage

| Action | Result |
|---|---|
| Hold Caps Lock (~0.3s) | Recording starts, tray turns red |
| Release Caps Lock | Processing, tray turns yellow |
| Done | Text typed at cursor, tray goes green |
| Quick tap Caps Lock | Ignored |

---

## Startup on boot

Right-click the tray icon → "Launch at startup". A checkmark confirms it's enabled — wispr-lite will launch automatically on every login. Click again to disable.

---

## Config

Everything lives in `config.py`:

```python
GROQ_API_KEY = "..."                  # your Groq API key
HOLD_KEY = "caps_lock"                # trigger key
WHISPER_MODEL = "whisper-large-v3-turbo"
LLM_MODEL = "openai/gpt-oss-20b"     # cleanup model
AI_CLEANUP = True                     # set False to inject raw Whisper output
```

`AI_CLEANUP = False` skips the LLM pass entirely — useful for zero-latency raw transcription.

---

## Maintenance

**Auth errors** — API key was revoked. Generate a new one at [console.groq.com/keys](https://console.groq.com/keys) and update `config.py`.

**Model not found** — Groq retires models occasionally. Check current IDs at [console.groq.com/docs/models](https://console.groq.com/docs/models) and update `LLM_MODEL` or `WHISPER_MODEL` in `config.py`.

**Garbled text injection** — increase the typing delay in `injector.py`:
```python
keyboard.write(text, delay=0.08)
```
Older machines sometimes need more breathing room between keystrokes.

**Usage limits** — Groq's free tier resets daily. Check usage at [console.groq.com](https://console.groq.com). At normal pace you won't get close.

**Audio device lockout** — if your mic stops working after repeated use, the audio stream didn't release cleanly. Restart the audio service in CMD:
```cmd
net stop audiosrv && net start audiosrv
```
If that doesn't work, restart your machine.

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

- [Groq](https://groq.com) — Whisper large-v3-turbo + openai/gpt-oss-20b
- [sounddevice](https://python-sounddevice.readthedocs.io) — mic capture
- [pynput](https://pynput.readthedocs.io) — hotkey detection
- [keyboard](https://github.com/boppreh/keyboard) — text injection
- [pystray](https://github.com/moses-palmer/pystray) — system tray
- [psutil](https://pypi.org/project/psutil/) — stale lock detection