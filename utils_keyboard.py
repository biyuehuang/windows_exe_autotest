from typing import Iterable

try:
    import keyboard
    from pywinauto import keyboard as pywinauto_keyboard
except Exception:
    raise


def send_keys(text) -> bool:
    keyboard.write(text)
    return True


def send_key(key) -> bool:
    keyboard.send(key[0])
    return True


def send_enter() -> bool:
    keyboard.send('enter')
    return True


def send_esc() -> bool:

    keyboard.send('esc')
    return True


def send_down_arrow() -> bool:
    keyboard.send('down')
    return True


def send_up_arrow() -> bool:

    keyboard.send('up')
    return True


def send_left_arrow() -> bool:

    keyboard.send('left')
    return True


def send_right_arrow() -> bool:

    keyboard.send('right')
    return True


def send_backspace() -> bool:

    keyboard.send('backspace')
    return True


def send_delete() -> bool:

    keyboard.send('delete')
    return True


def send_special_keys(keys) -> bool:
    try:

        pywinauto_keyboard.send_keys(keys)
    except:
        return False
    return True


def send_home() -> bool:

    pywinauto_keyboard.send_keys("{VK_HOME}")
    return True


def send_tab() -> bool:
    pywinauto_keyboard.send_keys("{TAB}")
    return True


def send_pattern(*argv: Iterable) -> bool:
    try:
        keys = "+".join([str(x).lower() for x in argv])

        keyboard.send(keys)
    except:
        return False
    return True


def send_press_release_pattern(*argv: Iterable) -> bool:
    keys = "+".join([str(x).lower() for x in argv])
    try:
        for i in argv:
            keyboard.press(i)
        for j in argv[::-1]:
            keyboard.release(j)
    except Exception as e:

        return False
    return True


def close_active_window() -> bool:
    return send_pattern(*['alt', 'f4'])
