from time import sleep
from typing import Optional

import logger
from driver_appium import AppiumDriver

class MenuActions:
    def __init__(self, driver: AppiumDriver) -> None:
        self.__driver = driver

    def go_to_home_page(self) -> bool:
        return self.go_to_display_page()

    def go_to_advance_page(self) -> bool:
        return self.__go_to_page('TabAdvance')

    def go_to_display_page(self) -> bool:
        return self.__go_to_page('TabDisplay')

    def go_to_setting_page(self) -> bool:
        return self.__go_to_page('TabSetting')

    def go_to_button_advance_reset(self) -> bool:
        return self.__go_to_button('Button_resetAdvanced')

    def go_to_button_setting_reset(self) -> bool:
        return self.__go_to_button('Button_resetBrightnessContrast')

    def go_to_button_monitor1(self) -> bool:
        return self.__go_to_button('Button_Monitor1')

    def go_to_button_monitor2(self) -> bool:
        return self.__go_to_button('Button_Monitor2')

    def go_to_button_monitor3(self) -> bool:
        return self.__go_to_button('Button_Monitor3')

    def go_to_button_monitor4(self) -> bool:
        return self.__go_to_button('Button_Monitor4')

    def go_to_button_custome(self) -> bool:
        return self.__go_to_button('Button_custome')

    def go_to_button_resetRGB(self) -> bool:
        return self.__go_to_button('Button_resetRGB')

    def go_to_button_red(self) -> bool:
        return self.__go_to_button('Button_red')

    def go_to_button_green(self) -> bool:
        return self.__go_to_button('Button_green')

    def go_to_button_blue(self) -> bool:
        return self.__go_to_button('Button_blue')

    def go_to_button_eye(self) -> bool:
        return self.__go_to_button('Button_eye')

    def go_to_button_standard(self) -> bool:
        return self.__go_to_button('Button_standard')

    def go_to_button_vivid(self) -> bool:
        return self.__go_to_button('Button_vivid')

    def go_to_checkbox_eye(self) -> bool:
        return self.__go_to_button('checkbox_eye')

    def go_to_checkbox_standard(self) -> bool:
        return self.__go_to_button('checkbox_default')

    def go_to_checkbox_vivid(self) -> bool:
        return self.__go_to_button('checkbox_vivid')

    def go_to_button_xmin(self) -> bool:
        return self.__go_to_button('xmin')

    def __go_to_page(self, name: str) -> bool:
        page_element = self.__driver.find_element_by_id(name)
        click_page_button = click_button_by_id(self.__driver, name)
        sleep(1)
        is_selected = self.__driver.is_element_selected(page_element)
        return click_page_button and is_selected

    def __go_to_button(self, name: str) -> bool:
        click_page_button = click_button_by_id(self.__driver, name)
        sleep(1)
        return click_page_button

def click_button_by_id(driver: AppiumDriver, name: str, button_id: Optional[str] = None) -> bool:
    if button_id is None:
        button_id = name
    button = driver.find_element_by_id(button_id)
    driver.click_element(button)
    return True