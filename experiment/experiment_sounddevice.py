#!/usr/bin/env python3
import sounddevice as sd
import soundfile as sf
from pynput import keyboard
import time
import csv
import random
import os

# ----------------------------
# CONFIGURATION
# ----------------------------
# Path to your audio files
audio_dir = "audio"


# Human / machine mapping (example: filename contains 'human' or 'machine')
def label_from_filename(fname):
    return "H" if "human" in fname.lower() else "M"


# ----------------------------
# COLLECT AUDIO FILES
# ----------------------------
all_files = [f for f in os.listdir(
    audio_dir) if f.lower().endswith((".wav", ".mp3"))]
random.shuffle(all_files)  # randomize trial order

# ----------------------------
# RUN TRIALS
# ----------------------------
results = []

for fpath in all_files:
    full_path = os.path.join(audio_dir, fpath)
    data, fs = sf.read(full_path)
    print(f"\nNow playing: {fpath}")
    print("Press H for human, M for machine.")

    start_time = time.time()
    sd.play(data, fs)

    pressed = []

    def on_press(key):
        try:
            if key.char.lower() in ["h", "m"]:
                pressed.append(key.char.upper())
                return False  # stop listener
        except AttributeError:
            pass

    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    # Wait until a valid key is pressed
    while not pressed:
        time.sleep(0.01)

    listener.stop()
    rt = time.time() - start_time
    sd.stop()

    # Store trial data
    results.append(
        {
            "file": fpath,
            "correct_label": label_from_filename(fpath),
            "response": pressed[0],
            "RT": round(rt, 3),
        }
    )

# ----------------------------
# FEEDBACK BLOCK
# ----------------------------
print("\nAll trials completed!")
feedback = input(
    "Optional: Please provide any feedback about the experiment: ")

#
