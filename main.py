import argparse
import os
import logging
import subprocess
import pyautogui
from time import sleep
from datetime import datetime


logger = logging.getLogger(__name__)

# processes stdin arguments
def get_args():
    parser = argparse.ArgumentParser(description="Performance measuring")
    parser.add_argument("file", help="path to executable file")
    parser.add_argument(
        "-o",
        default=os.path.join(os.getcwd(), f"stats_{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"),
        help="specify a directory to store results",
    )
    args = parser.parse_args()

    # checks if the file exists
    if not os.path.exists(args.file):
        raise FileNotFoundError("Check if you have passed a correct file path")

    # if the folder is not specified or does not exist, the default directory will be created
    if not os.path.exists(args.o):
        os.mkdir(args.o)

    logging.info(f"Output directory: {args.o}")

    return args.file, args.o

def launch_process():
    # process = subprocess.Popen([exec_file, "-f"])
    # check if the proces is launched
    pass


def make_screenshot(dir, name):
    scr = pyautogui.screenshot()
    path = os.path.join(dir, name)
    scr.save(path)


def main():
    exec_file, output_dir = get_args()

    #process = launch_process()
    logging.info("The process is launched")

    make_screenshot(output_dir, 'start_screenshot.png')
    logging.info("Took screenshot")
    
    pyautogui.press('enter', presses=2)
    pyautogui.keyDown("w")
    sleep(5)
    pyautogui.keyUp("w")
    
    # process.kill()
    logging.info("The process is killed")


if __name__=='__main__':
    logging.basicConfig(
        format="logger >> %(message)s", level=logging.INFO
    )
    main()