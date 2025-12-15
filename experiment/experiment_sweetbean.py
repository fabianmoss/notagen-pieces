import sounddevice as sd
import soundfile as sf
from pynput import keyboard
import time
import csv

trials = ["audio/test.wav"]
results = []

for fpath in trials:
    data, fs = sf.read(fpath)
    print("Press H for human, M for machine")

    start = time.time()
    sd.play(data, fs)

    pressed = None

    def on_press(key):
        nonlocal pressed
        try:
            if key.char.lower() == "h":
                pressed = "H"
                return False  # stop listener
            elif key.char.lower() == "m":
                pressed = "M"
                return False
        except AttributeError:
            pass

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

    rt = time.time() - start
    results.append({"file": fpath, "response": pressed, "RT": rt})
    sd.stop()

with open("results.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["file", "response", "RT"])
    writer.writeheader()
    writer.writerows(results)
