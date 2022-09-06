import argparse
import os
import logging
import subprocess
import pyautogui

from configparser import ConfigParser
from time import sleep
from datetime import datetime


logger = logging.getLogger(__name__)


# processes stdin arguments
def get_args():
    parser = argparse.ArgumentParser(description="Performance measuring")
    parser.add_argument("file", help="path to executable file")
    parser.add_argument(
        "-o",
        default=os.path.join(
            os.getcwd(), f"stats_{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
        ),
        help="specify a directory to store results",
    )
    args = parser.parse_args()

    # checks if the file exists
    if not os.path.exists(args.file):
        raise FileNotFoundError("Check if you have passed a correct file path")

    # if the folder is not specified or does not exist, the default directory will be created
    if not os.path.exists(args.o):
        os.mkdir(args.o)

    logging.info(f"Get results here: {args.o}")

    return args.file, args.o


def launch_process(exec_file):
    process = subprocess.Popen([exec_file, "-f"])
    sleep(3)
    while pyautogui.pixelMatchesColor(300, 200, (0, 0, 0)):
        sleep(0.1)
    logging.info("The process is launched")
    return process


def press_key(key, time=0.1):
    pyautogui.keyDown(key)
    sleep(time)
    pyautogui.keyUp(key)
    sleep(1)


def make_screenshot(dir, name):
    scr = pyautogui.screenshot()
    path = os.path.join(dir, name)
    scr.save(path)
    logging.info(f"{name} was taken")
    sleep(1)


def kill_process(process):
    process.kill()
    sleep(1)
    logging.info("The process is killed")


def run_scenario(exec_file, output_dir):
    # launch
    process = launch_process(exec_file)

    # skip intro
    press_key("enter")

    # start game
    press_key("enter")

    # screenshot
    make_screenshot(output_dir, "start_screenshot.png")

    # move the character forward
    press_key("w", 5)

    # screenshot
    make_screenshot(output_dir, "end_screenshot.png")

    # terminate execution
    kill_process(process)


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s%(name)5s:%(lineno)3s:%(levelname)s >> %(message)s",
        level=logging.INFO,
    )
    exec_file, output_dir = get_args()
    run_scenario(exec_file, output_dir)
