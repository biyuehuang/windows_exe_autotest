import logging
import os
import sys
from time import strftime, gmtime
from typing import Optional, Union


def start_logger(test_name: str, log_level: Optional[str]) -> None:
    log_dir = '.\\logs'
    current_time = strftime("%Y-%m-%d_%H.%M.%S", gmtime())
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    try:
        global log
        log = logging.getLogger(test_name)
        level = logging.DEBUG
        if log_level == 'Info':
            level = logging.INFO
        log.setLevel(level)
        fh = logging.FileHandler('.\\logs\\{}.log'.format(current_time), mode='w', encoding='utf-8')
        fh.setLevel(level)
        ch = logging.StreamHandler()
        ch.setLevel(level)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)
        log.addHandler(ch)
        log.addHandler(fh)
    except Exception as e:
        print('Failed to initialize logging!')
        print(e)
        sys.exit(-1)


def error(message: Union[Exception, str] = '', stop: bool = True) -> None:
    log.critical(message)
    #grab_screen()
    if stop:
        sys.exit(-1)


def test_error(message: str) -> None:
    error(message, False)


def info(message: str) -> None:
    if log:
        log.info(message)
    else:
        print(5 * '*' + ' logger is not initialized and logging failed! ' + 5 * '*' + '\nMessage: {}\n'.format(message))


def debug(message: str) -> None:
    log.debug(message)


def shut_down_logger() -> None:
    logging.shutdown()
