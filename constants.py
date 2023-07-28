from colors import *
import sys
WIDTH, HEIGHT = 1920, 1080
# game
FPS = 60

import os
import sys

# If the script is running in a PyInstaller bundle
if getattr(sys, 'frozen', False):
    script_dir = sys._MEIPASS
else:
    # Else we're running in normal Python environment
    script_dir = os.path.dirname(os.path.realpath(__file__))

asset_path = os.path.join(script_dir, 'assets', 'your_music.mp3')
