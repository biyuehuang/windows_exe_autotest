import os
import subprocess
import logger
import utils_keyboard

wad = None


def start_wad():
    global wad
    wad_path = r'C:\Program Files (x86)\Windows Application Driver\WinAppDriver.exe'
    if os.path.exists(wad_path):
        wad = subprocess.Popen('{}'.format(wad_path), creationflags=subprocess.CREATE_NEW_CONSOLE)
        send_app_to_background()

    else:
        logger.error('WAD not found under path: {}'.format(wad_path))

def send_app_to_background() -> bool:
    return utils_keyboard.send_pattern(*['alt', 'esc'])

def stop_wad():
    if wad:
        os.system("taskkill /f /im WinAppDriver.exe")
