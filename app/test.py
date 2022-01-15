import os
from pathlib import Path

from app.utils.utilities import get_file_icon

get_file_icon("res/app/tab.exe")

print(str(Path(__file__).resolve().parent))