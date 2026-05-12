import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import tempfile
import os
from config import SAMPLE_RATE, CHANNELS

class Recorder:
    def __init__(self):
        self.recording = False
        self.frames = []

    def start(self):
        self.frames = []
        self.recording = True
        self.stream = sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype='int16',
            callback=self._callback
        )
        self.stream.start()
        print("[recorder] recording...")

    def _callback(self, indata, frames, time, status):
        if self.recording:
            self.frames.append(indata.copy())

    def stop(self):
        self.recording = False
        self.stream.stop()
        self.stream.close()
        print("[recorder] stopped.")

        if not self.frames:
            return None

        audio = np.concatenate(self.frames, axis=0)

        # write to a temp wav file
        tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        wav.write(tmp.name, SAMPLE_RATE, audio)
        print(f"[recorder] saved to {tmp.name}")
        return tmp.name

    def cleanup(self, path):
        if path and os.path.exists(path):
            os.remove(path)