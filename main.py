import argparse
import os
import subprocess
import pyautogui
from time import sleep
from datetime import datetime
from pathlib import Path

# import psutil


# processes stdin arguments
parser = argparse.ArgumentParser(description="Performance measuring")
parser.add_argument("file_path", help="path to executable file")
parser.add_argument(
    "-o",
    default=os.path.join(os.getcwd(), f"stats_{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"),
    help="specify a directory to store results",
)
args = parser.parse_args()

print(f"file path {args.file_path}")
print(f"output {args.o}")

# checks if the file exists
if not os.path.exists(args.file_path):
    raise FileNotFoundError("Check if you have passed a correct file path")

# if the path to the output directory is not specified, the default directory will be created
if not os.path.exists(args.o):
    os.mkdir(args.o)

# checks if the output directory exists
# if not os.path.exists(args.o):
#     raise FileNotFoundError("Check if you have passed a correct output directory path")


print(f"file path {args.file_path}")
print(f"output {args.o}")

# def launch_process():
# launch
# process = subprocess.Popen([args.file_path, "-f"])
# sleep(3)
# check if the process is active
# if os.path.basename(args.file_path) in (p.name() for p in psutil.process_iter()):
#     print('WORKING!')
# return process


# def press_btn(btn: str, interval=0.0, times=0):
#     for _ in range(times + 1):
#         pyautogui.btnDown(btn)
#         sleep(interval)
#         pyautogui.btnUp(btn)
#         sleep(0.5)


def main():
    process = subprocess.Popen(["runas", "/user:eegor", args.file_path, "-f"])
    # os.startfile(args.file_path)
    sleep(15)
    pyautogui.press("enter", presses=2)
    prtsc = pyautogui.screenshot()
    prtsc.save(args.o, "scr_start.png")
    pyautogui.hold("w")
    sleep(3)
    prtsc = pyautogui.screenshot()
    prtsc.save(args.o, "scr_start.png")
    process.kill()


# if __name__=='__main__':
#     main()
