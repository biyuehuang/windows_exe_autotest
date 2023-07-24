from time import sleep
from typing import Optional, Dict, Tuple

from appium.webdriver import WebElement
from selenium.common.exceptions import NoSuchElementException

from driver_appium import AppiumDriver
from driver_appium import click_button_by_id
from display_page import DisplayPage
from menu_actions import MenuActions
import logger

class Application:
    def __init__(self, accept_eula: bool = True, close_gcp_popup: bool = True, monitor_exit_code: bool = False) -> None:

        self.__driver = AppiumDriver()
        self.menu_actions = MenuActions(self.__driver)
        self.display_page = DisplayPage(self.__driver)


    def close_old_gcp_popup(self):
        find_gcp = self.gcp_popup.find_popup()
        if find_gcp:
            self.gcp_popup.click_do_not_show_checkbox()
            self.gcp_popup.click_close()
        else:
            logger.info("Uninstall old GCP popup not found")

    def accept_license(self):
        for _ in range(10):
            if self.eula_popup.find_popup():
                self.eula_popup.click_accept()
                sleep(2)
            else:
                logger.info("License popup not found")
                break

    def shut_down(self, close_wad: bool = True) -> None:
        self.__driver.shut_down(close_wad)
        sleep(2)

    def restart(self) -> bool:
        try:
            logger.info('Restarting the app!')
            self.__driver.shut_down(False)
            self.__driver.launch_app()
            self.wait_for_menu_panel()
        except Exception as e:
            logger.error(e, False)
            raise Exception('Unable to restart application')
        return True

    def start(self) -> bool:
        try:
            logger.info('Starting the app!')
            self.__driver.launch_app()
            self.wait_for_menu_panel()
        except Exception as e:
            logger.error(e, False)
            raise Exception('Unable to start the application')
        return True

    def minimize_igcc_window(self) -> bool:
        if not self.__driver.is_minimized():
            return click_button_by_id(self.__driver, "Minimize")

    def is_minimized(self) -> bool:
        return self.__driver.is_minimized()

    def maximize_igcc_window(self) -> bool:
        if not self.__driver.is_maximized():
            return click_button_by_id(self.__driver, 'Maximize')

    def is_maximized(self) -> bool:
        return self.__driver.is_maximized()

    def restore_down_igcc_window(self) -> bool:
        if self.__driver.is_maximized():
            return click_button_by_id(self.__driver, 'Maximize')

    def wait_for_menu_panel(self, wait_time=300) -> None:
        self.__driver.wait_for_clickable_element_class_name('SplitViewPane', sleep_time=wait_time)

    def close_application_by_exit_button(self) -> bool:
        logger.info('Closing app by Close button')
        return click_button_by_id(self.__driver, 'Close')

    def set_window_position(self, position: Dict) -> bool:
        logger.info(f'Moving IGCC window to position x: {position["x"]} y: {position["y"]}')
        return self.__driver.set_window_position(position['x'], position['y'])

    def get_window_position(self) -> Tuple[int, int]:
        return self.__driver.get_window_position()

    def set_window_size(self, x: int, y: int) -> bool:
        logger.info(f'Resizing window to {x}x{y}')
        return self.__driver.set_window_size(x, y)

    def set_window_minimum_size(self) -> bool:
        logger.info(f'Resizing window to {502}x{502}')
        return self.__driver.set_window_size(502, 502)

    def find_element_by_id(self, name: str) -> Optional[WebElement]:
        logger.info(f'finding element by id: {name}')
        return self.__driver.find_element_by_id(name, throw_exception=False)

    def get_exit_code(self) -> Optional[int]:
        logger.info("Getting IGCC exit code")

        if not self.__exit_code:
            logger.debug("Exit code monitoring must be turned on in test first")
            return None

        if not self.__exit_code.ready():
            logger.error("Couldn't retrieve exit code", False)
            return -1

        return self.__exit_code.get()