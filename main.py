import argparse
import os
import logging
import subprocess
import pyautogui
import re
import csv
import statistics

from configparser import ConfigParser
from glob import glob
from time import sleep
from datetime import datetime


logger = logging.getLogger(__name__)


# processes cmd line arguments
def get_args() -> tuple:
    parser = argparse.ArgumentParser(description="Performance measuring")
    parser.add_argument("path", help="path to executable file")
    parser.add_argument(
        "-o",
        default=os.path.join(
            os.getcwd(), f"stats_{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
        ),
        help="specify a directory to store results",
    )
    args = parser.parse_args()

    # checks if the file exists
    if not os.path.exists(args.path):
        raise FileNotFoundError("Check if you have passed a correct file path")

    # if the folder is not specified or does not exist, the default directory will be created
    if not os.path.exists(args.o):
        os.mkdir(args.o)

    logging.info(f"Get results here: {args.o}")

    return args.path, args.o


def get_config() -> tuple:
    config = ConfigParser()
    config.read("config.ini")

    fraps_exe_path = config["fraps"]["exec_file"]
    fraps_output = config["fraps"]["output"]
    fraps_hotkey = config["fraps"]["hotkey"]

    return fraps_exe_path, fraps_output, fraps_hotkey


def launch_fraps(exec_file: str) -> subprocess.Popen:
    process = subprocess.Popen([exec_file, "-f"])
    sleep(1)
    logging.info("Fraps is launched")
    return process


def launch_game(exec_file: str) -> subprocess.Popen:
    process = subprocess.Popen([exec_file, "-f"])
    sleep(3)
    # check the background colors to understand when the game will load
    while pyautogui.pixelMatchesColor(300, 200, (0, 0, 0)):
        sleep(0.1)
    logging.info("The game is launched")
    return process


def press_key(key: str, time: float = 0.1) -> None:
    pyautogui.keyDown(key)
    sleep(time)
    pyautogui.keyUp(key)
    sleep(1)


def make_screenshot(output_folder: str, file_name: str) -> None:
    scr = pyautogui.screenshot()
    path = os.path.join(output_folder, file_name)
    scr.save(path)
    logging.info(f"{file_name} was taken")
    sleep(1)


def get_stat(output_folder: str, fraps_output: str) -> None:
    fraps_files = glob(fraps_output + "\*.csv")
    latest_stat = max(fraps_files, key=os.path.getctime)

    read_stat = []
    with open(latest_stat, "r", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=" ", quotechar="|")
        for row in reader:
            try:
                row = int(row[0])
            except ValueError:
                continue
            read_stat.append(row)

    median_fps = statistics.median(read_stat)
    with open(os.path.join(output_folder, "median_fps.txt"), "w") as file:
        file.write(str(median_fps))
    logging.info("FPS stat is written to median_fps.txt")


def kill_process(process: subprocess.Popen) -> None:
    process.kill()
    sleep(1)
    logging.info(f"{os.path.basename(process.args[0])} is killed")


def run_scenario(
    game_exe_path: str,
    output_folder: str,
    fraps_exe_path: str,
    fraps_output: str,
    fraps_hotkey: str,
) -> None:
    # launch fraps
    process_1 = launch_fraps(fraps_exe_path)

    # launch game
    process_2 = launch_game(game_exe_path)

    # skip intro
    press_key("enter")

    # start game
    press_key("enter")

    # screenshot
    make_screenshot(output_folder, "start_screenshot.png")

    # start measure fps
    press_key(fraps_hotkey)

    # move the character forward
    press_key("w", 5)

    # screenshot
    make_screenshot(output_folder, "end_screenshot.png")

    # stop measure fps
    press_key(fraps_hotkey)

    # close game
    kill_process(process_2)

    # close fraps
    kill_process(process_1)

    # save stat
    get_stat(output_folder, fraps_output)


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s%(name)5s:%(lineno)3s:%(levelname)s >> %(message)s",
        level=logging.INFO,
    )

    fraps_exe_path, fraps_output, fraps_hotkey = get_config()
    game_exe_path, output_folder = get_args()

    run_scenario(
        game_exe_path, output_folder, fraps_exe_path, fraps_output, fraps_hotkey
    )
