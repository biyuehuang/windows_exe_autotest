from typing import Union
import logger
import pywinauto.mouse as mouse
import time
try:
    import win32api
    import win32con
except Exception:
    raise


def scroll(delta: Union[int, float] = 1, x: int = 0, y: int = 0, silent: bool = False) -> None:
    if not silent:
         print("Scrolling mouse by")
    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, x, y, delta * 100, 0)


def move_and_click(x: int, y: int, button: str = 'left', skip_sleep: bool = False) -> bool:
    mouse.click(button=button, coords=(x, y))
    if not skip_sleep:
        time.sleep(2)
    return True


def move_cursor(x: int, y: int) -> bool:
    logger.info('Moving cursor by: {}x {}y'.format(x, y))
    mouse.move((x, y))
    time.sleep(1)
    return True


def click(button: str = 'left') -> bool:
    logger.info('Clicking mouse {} button'.format(button))
    mouse.click(button=button)
    time.sleep(1)
    return True


def double_click(button: str = 'left') -> bool:
    logger.info('Double clicking mouse {} button'.format(button))
    mouse.double_click(button=button)
    time.sleep(1)
    return True
