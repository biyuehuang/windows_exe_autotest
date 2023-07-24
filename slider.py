from typing import Callable, Optional, Tuple

from appium.webdriver import WebElement
from appium.webdriver.webdriver import MobileBy as By
from driver_appium import AppiumDriver
import logger
from mouse import scroll

class Slider:
    def __init__(self, driver: AppiumDriver, automation_id: Optional[str] = None, get_element: Optional[Callable] = None,
                 value_range: Tuple[int, int] = (-180, 180)) -> None:
        self.driver = driver
        self.automation_id = automation_id
        if get_element:
            self.get_element = get_element

        self.min_value, self.max_value = value_range

    def get_element(self) -> WebElement:
        return self.driver.find_element_by_id(self.automation_id,  throw_exception=False)

    def get_decrease_button_element(self) -> WebElement:
        return self.driver.find_element_by_id(f'Decrease_{self.automation_id}')

    def get_increase_button_element(self) -> WebElement:
        return self.driver.find_element_by_id(f'Increase_{self.automation_id}')

    def set_value(self, value: str) -> bool:
        if int(value) > self.max_value or int(value) < self.min_value:
            raise ValueError("Value for {} slider is out of range: {} - {}".format(
                self.automation_id, self.min_value, self.max_value))

        return self.driver.set_slider_value(self.get_element(), self.automation_id, value)

    def get_value(self) -> str:
        return read_slider_element_value(self.driver, self.get_element())

    def get_automation_id(self) -> str:
        return self.automation_id

    def is_enabled(self) -> bool:
        element = self.get_element()
        return self.driver.is_element_enabled(element) if element is not None else element



def set_slider_element_value(driver: AppiumDriver, element: WebElement, value: str) -> bool:
    slider_name = element.get_attribute("AutomationId")

    driver.click_element(element)
    value_set = driver.set_slider_value(element, slider_name, value)
    if value != 'MAX' and read_slider_element_value(driver, element) != str(value):
        raise Exception('Unexpected slider value after value set')

    return value_set

def read_slider_element_value(driver: AppiumDriver, element: WebElement) -> str:

    name = driver.get_element_automation_id(element)
    driver.scroll_to_element(driver.find_element_ancestor(element, 1))
    scroll(-2)

    print("Getting current",name)
    slider_value = driver.read_element_text(element)

    print('Current {} value: {}'.format(name, slider_value))
    return slider_value