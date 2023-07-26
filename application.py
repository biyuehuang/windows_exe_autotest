from time import sleep
from driver_appium import AppiumDriver
from display_page import DisplayPage
from menu_actions import MenuActions


class Application:
    def __init__(self, accept_eula: bool = True, close_gcp_popup: bool = True, monitor_exit_code: bool = False) -> None:

        self.__driver = AppiumDriver()
        self.menu_actions = MenuActions(self.__driver)
        self.display_page = DisplayPage(self.__driver)
    def shut_down(self, close_wad: bool = True) -> None:
        self.__driver.shut_down(close_wad)
        sleep(2)
