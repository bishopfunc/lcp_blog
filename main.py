from pathlib import Path
import os

os.path.exists("./test1/test1.txt")
BASE_DIR = Path(__file__).resolve().parent.parent
print(BASE_DIR)