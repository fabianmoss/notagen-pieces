from psychopy import sound, core
from psychopy import prefs

prefs.hardware["audioLib"] = ["sounddevice"]  # safest backend


snd = sound.Sound("audio/human_01.wav")
print("Duration:", snd.getDuration())
snd.play()
core.wait(snd.getDuration())
print("Done")
