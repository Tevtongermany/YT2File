import os
import shutil
import sys

os.system(f'pyinstaller --noconsole --windowed --add-data "{os.path.realpath("venv")}\Lib\site-packages\customtkinter;customtkinter" --icon="favicon.ico" "{os.path.realpath("main.py")}"')
shutil.copy("favicon.ico","dist/main")