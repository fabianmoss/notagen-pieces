from psychopy import visual, core, sound, event, gui
import random
import os
import csv
import json
from datetime import datetime
from psychopy import prefs

prefs.hardware["audioLib"] = ["sounddevice"]

# ----------------
# EXPERIMENT SETUP
# ----------------

AUDIO_DIR = "audio"
DATA_DIR = "data"
HIGHSCORE_FILE = "highscores.json"

KEY_HUMAN = "h"
KEY_MACHINE = "m"
QUIT_KEY = "escape"

os.makedirs(DATA_DIR, exist_ok=True)

# Participant info dialog
exp_info = {"participant": "", "age": "", "session": "001"}

dlg = gui.DlgFromDict(exp_info, title="Can you hear the difference?")
if not dlg.OK:
    core.quit()

# Timestampted data file
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
data_file = os.path.join(
    DATA_DIR, f"sub-{exp_info['participant']}_{timestamp}.csv")

# ------------
# WINDOW
# -----------

win = visual.Window(size=[800, 600], color="black", units="pix")

text = visual.TextStim(win, text="", wrapWidth=700)

# ----------------
# INTRO BLOCK
# ----------------

text.text = (
    "Welcome to the Turing Test.\n\n"
    "You will hear audio clips.\n"
    "Press 'H' if you think it is HUMAN.\n"
    "Press 'M' if you think it is MACHINE.\n\n"
    "Press any key to start."
)
text.draw()
win.flip()
event.waitKeys()

# ----------------------------
# TRIAL SETUP
# ----------------------------

audio_files = [f for f in os.listdir(AUDIO_DIR) if f.lower().endswith(".wav")]

random.shuffle(audio_files)

trials_data = []
correct_count = 0

# ----------------------------
# TRIAL LOOP
# ----------------------------

for trial_idx, audio_file in enumerate(audio_files, start=1):
    filepath = os.path.join(AUDIO_DIR, audio_file)
    snd = sound.Sound(filepath)

    # Ground truth from filename
    correct_answer = "human" if "human" in audio_file.lower() else "machine"

    # Prompt
    text.text = "Listening..."
    text.draw()
    win.flip()

    core.wait(0.3)
    snd.play()
    # core.wait(snd.getDuration())

    # Collect response
    clock = core.Clock()
    keys = event.waitKeys(
        keyList=[KEY_HUMAN, KEY_MACHINE, QUIT_KEY], timeStamped=clock)

    key, rt = keys[0]
    if key == QUIT_KEY:
        win.close()
        core.quit()

    response = "human" if key == KEY_HUMAN else "machine"
    correct = response == correct_answer
    if correct:
        correct_count += 1

    trials_data.append(
        {
            "participant": exp_info["participant"],
            "trial": trial_idx,
            "stimulus": audio_file,
            "correct_answer": correct_answer,
            "response": response,
            "rt": rt,
            "correct": correct,
        }
    )

    # Inter-trial interval
    core.wait(0.5)

# ----------------------------
# SCORE & HIGHSCORE
# ----------------------------

score = correct_count
max_score = len(audio_files)

# Load existing highscore
if os.path.exists(HIGHSCORE_FILE):
    with open(HIGHSCORE_FILE, "r") as f:
        highscores = json.load(f)
else:
    highscores = {"highscore": 0}

new_highscore = score > highscores["highscore"]
if new_highscore:
    highscores["highscore"] = score
    with open(HIGHSCORE_FILE, "w") as f:
        json.dump(highscores, f)

# ----------------------------
# FINAL BLOCK (FEEDBACK)
# ----------------------------

text.text = (
    f"Your score: {score} / {max_score}\n"
    f"Highscore: {highscores['highscore']}\n\n"
    "Press any key to continue."
)
text.draw()
win.flip()
event.waitKeys()

# Free text
feedback = ""
text.text = "Optional feedback:\n(Type and press RETURN to submit)\n\n"
win.flip()

while True:
    keys = event.waitKeys()
    for key in keys:
        if key == "return":
            break
        elif key == "backspace":
            feedback = feedback[:-1]
        elif len(key) == 1:
            feedback += key

    text.text = "Optional feedback:\n(Type and press RETURN to submit)\n\n" + feedback
    text.draw()
    win.flip()

    if "return" in keys:
        break

# ----------------------------
# SAVE DATA
# ----------------------------

with open(data_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=trials_data[0].keys() | {"feedback"})
    writer.writeheader()
    for row in trials_data:
        row["feedback"] = feedback
        writer.writerow(row)

# ----------------------------
# CLEANUP
# ----------------------------

text.text = "Thank you for participating!"
text.draw()
win.flip()
core.wait(2)

win.close()
core.quit()
