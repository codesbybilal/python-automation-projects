import os
import time

os.system("cls")

frames = ["●", "◉", "○", "◉"]

while True:
    for frame in frames:
        print("\033[H", end="")
        print(frame)
        time.sleep(0.3)