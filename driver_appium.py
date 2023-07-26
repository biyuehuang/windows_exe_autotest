import os
import time
from selenium.common.exceptions import NoSuchWindowException, WebDriverException
import wad
import logger
from typing import List, Optional, Tuple, Dict

try:
    from appium import webdriver as appium_webdriver
    from appium.webdriver.webelement import WebElement
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions
    from appium.webdriver.webdriver import MobileBy as By
    from selenium.common import exceptions
    from selenium.webdriver.common.keys import Keys
except Exception:
    raise


class AppiumDriver:
    __app_caps = None
    __driver = None
    __default_implicitly_wait = 10

    def __init__(self, app: str = None):
        self.__app_caps = r"C:\Users\huangya1\Downloads\idcc-20230504\idcc.exe" 
        self.initialize()

    def initialize(self) -> appium_webdriver:
        desired_caps = {"app": self.__app_caps,
                        'platformName': 'Windows',

                        }
        try:
            wad.start_wad()
            self.__driver = appium_webdriver \
                .Remote(command_executor='http://127.0.0.1:4723',
                        desired_capabilities=desired_caps)
            self.__driver.implicitly_wait(self.__default_implicitly_wait)

            return self.__driver
        except Exception as e:
            raise e

    def shut_down(self, close_wad: bool = True) -> None:
        try:
            self.__driver.close_app()
        except NoSuchWindowException:
            logger.error("App already closed", False)
        if close_wad:
            wad.stop_wad()

    def launch_app(self) -> None:
        self.__driver = self.__driver.launch_app()

    @staticmethod
    def __get_element_info_text(element: WebElement) -> str:
        if element:
            info_text = ""
            automation_id = element.get_attribute("AutomationId")
            name = element.get_attribute("Name")
            if automation_id:
                info_text += 'automation id: {} '.format(automation_id)
            if name:
                info_text += 'name: {} '.format(name.split("\n")[0])
            if element.tag_name:
                info_text += 'tag name: {} '.format(element.tag_name)
            if element.text:
                info_text += 'text: {} '.format(element.text.split("\n")[0])

            return info_text.strip()
        else:
            return 'None'

    def click_element(self, element: WebElement, retries_left: int = 1) -> bool:
        element_info_text = ""
        try:
            element_info_text = self.__get_element_info_text(element)
            element.click()
            return True
        except Exception as e:
            if retries_left > 0:
                logger.debug("Couldn't click element, trying again")
                return self.click_element(element, retries_left - 1)
            logger.error("Exception while clicking on element {}".format(element_info_text), False)
            logger.error(e, False)
            return False

    def right_click_element(self, element: WebElement) -> bool:
        element_info_text = ""
        try:
            element_info_text = self.__get_element_info_text(element)
            action = ActionChains(self.__driver)
            action.move_to_element(element) \
                .move_to_element(element)\
                .context_click().perform()
            return True
        except Exception as e:
            logger.error("Exception while clicking on element {}".format(element_info_text), False)
            logger.error(e, False)
            return False

    def wait_for_clickable_element_name(self, name: str, sleep_time: int = 60) -> Optional[WebElement]:
        return self.__wait_for_clickable_element_type(name, By.NAME, sleep_time=sleep_time)

    def wait_for_clickable_element_class_name(self, name: str, sleep_time: int = 60) -> Optional[WebElement]:
        return self.__wait_for_clickable_element_type(name, By.CLASS_NAME, sleep_time=sleep_time)

    def wait_for_clickable_element_id(self, name: str, sleep_time: int = 60) -> Optional[WebElement]:
        return self.__wait_for_clickable_element_type(name, By.ID, sleep_time=sleep_time)

    def __wait_for_clickable_element_type(self, name: str, by: By, sleep_time: int) -> Optional[WebElement]:
        element = None
        wait = WebDriverWait(self.__driver, sleep_time)
        try:
            logger.debug('Waiting for: element with {}: "{}"'.format(by, name))
            element = wait.until(expected_conditions.element_to_be_clickable((by, name)))
        except exceptions.TimeoutException:
            pass
        return element

    def wait_while_element_is_available(self, element: WebElement, sleep_time: int) -> bool:
        wait = WebDriverWait(self.__driver, sleep_time)
        try:
            logger.debug('Waiting while element is visible: {}'.format(self.__get_element_info_text(element)))
            element = wait.until(expected_conditions.invisibility_of_element_located(element))
        except exceptions.TimeoutException:
            pass
        return element

    def __find_element(self, value: str, by: By, throw_exception: bool, silent: bool) -> Optional[WebElement]:
        try:
            return self.__driver.find_element(by, value)
        except exceptions.NoSuchElementException as e:
            if silent:
                return None
            logger.error("Exception while looking for element by {}: '{}'".format(by, value), False)
            if throw_exception:
                raise e
            logger.error(e, False)

        return None

    def __find_elements(self, value: str, by: By, throw_exception: bool) -> List[WebElement]:
    #    logger.debug('Looking for elements with {}: "{}"'.format(by, value))
        elements = None
        try:
            elements = self.__driver.find_elements(by, value)
        except exceptions.NoSuchElementException as e:
            logger.error("Exception while looking for elements: '{}' by {}".format(value, by), False)
            if throw_exception:
                raise e
            logger.error(e, False)

        return elements

    @staticmethod
    def __find_child_element(element: WebElement, value: str, by: By, throw_exception: bool, silent: bool) -> \
            Optional[WebElement]:
        logger.debug('Looking for element with {}: "{}" in parent element'.format(by, value))
        child = None
        try:
            child = element.find_element(by, value)
        except exceptions.NoSuchElementException as e:
            if silent:
                return child
            logger.error("Exception while looking for child element: '{}'".format(value), False)
            if throw_exception:
                raise e
            logger.error(e, False)

        return child

    @staticmethod
    def __find_children_elements(
            element: WebElement, value: str, by: By, throw_exception: bool) -> List[WebElement]:
        logger.debug('Looking for elements with {}: "{}" in parent element'.format(by, value))
        children = None
        try:
            children = element.find_elements(by, value)
        except exceptions.NoSuchElementException as e:
            logger.error("Exception while looking for children elements: '{}'".format(value), False)
            if throw_exception:
                raise e
            logger.error(e)

        return children

    # Supported locator strategies for WAD available here:
    # https://github.com/Microsoft/WinAppDriver/tree/v1.0#supported-locators-to-find-ui-elements
    def find_element_by_id(self, name: str, throw_exception: bool = True, silent: bool = False) -> Optional[WebElement]:
        return self.__find_element(name, By.ACCESSIBILITY_ID, throw_exception, silent=silent)

    def find_element_by_class_name(self, name: str, throw_exception: bool = True) -> Optional[WebElement]:
        return self.__find_element(name, By.CLASS_NAME, throw_exception, silent=False)

    def find_element_by_name(self, name: str, throw_exception: bool = True, silent: bool = False
                             ) -> Optional[WebElement]:
        return self.__find_element(name, By.NAME, throw_exception, silent)

    def find_element_by_tag_name(self, name: str, throw_exception: bool = True) -> Optional[WebElement]:
        return self.__find_element(name, By.TAG_NAME, throw_exception, silent=False)

    def find_element_by_xpath(self, xpath: str, throw_exception: bool = True,
                              silent: bool = False) -> Optional[WebElement]:
        return self.__find_element(xpath, By.XPATH, throw_exception, silent=silent)

    def find_elements_by_class_name(self, name: str, throw_exception: bool = True) -> List[WebElement]:
        return self.__find_elements(name, By.CLASS_NAME, throw_exception)

    def find_elements_by_id(self, name: str, throw_exception: bool = True) -> List[WebElement]:
        return self.__find_elements(name, By.ACCESSIBILITY_ID, throw_exception)

    def find_elements_by_xpath(self, name: str, throw_exception: bool = True) -> List[WebElement]:
        return self.__find_elements(name, By.XPATH, throw_exception)

    def find_elements_by_name(self, name: str, throw_exception: bool = True) -> List[WebElement]:
        return self.__find_elements(name, By.NAME, throw_exception)

    def find_child_element_by_class_name(
            self, element: WebElement, name: str, throw_exception: bool = True) -> Optional[WebElement]:
        return self.__find_child_element(element, name, By.CLASS_NAME, throw_exception, silent=False)

    def find_child_element_by_name(self, element: WebElement, name: str, throw_exception: bool = True,
                                   silent: bool = False) -> Optional[WebElement]:
        return self.__find_child_element(element, name, By.NAME, throw_exception, silent)

    def find_child_element_by_control_type(
            self, element: WebElement, name: str, throw_exception: bool = True) -> Optional[WebElement]:
        return self.__find_child_element(element, name, By.TAG_NAME, throw_exception, silent=False)

    def find_child_element_by_id(
            self, element: WebElement, name: str, throw_exception: bool = True) -> Optional[WebElement]:
        return self.__find_child_element(element, name, By.ACCESSIBILITY_ID, throw_exception, silent=False)

    def find_child_element_by_xpath(
            self, element: WebElement, name: str, throw_exception: bool = True) -> Optional[WebElement]:
        return self.__find_child_element(element, name, By.XPATH, throw_exception, silent=False)

    def find_children_elements_by_name(
            self, element: WebElement, name: str, throw_exception: bool = True) -> List[WebElement]:
        return self.__find_children_elements(element, name, By.NAME, throw_exception)

    def find_children_elements_by_class_name(
            self, element: WebElement, name: str, throw_exception: bool = True) -> List[WebElement]:
        return self.__find_children_elements(element, name, By.CLASS_NAME, throw_exception)

    def find_children_elements_by_control_type(
            self, element: WebElement, name: str, throw_exception: bool = True) -> List[WebElement]:
        return self.__find_children_elements(element, name, By.TAG_NAME, throw_exception)

    def find_children_elements_by_xpath(
            self, element: WebElement, xpath: str, throw_exception: bool = True) -> List[WebElement]:
        return self.__find_children_elements(element, xpath, By.XPATH, throw_exception)

    def find_children_elements_by_id(
            self, element: WebElement, name: str, throw_exception: bool = True) -> List[WebElement]:
        return self.__find_children_elements(element, name, By.ACCESSIBILITY_ID, throw_exception)

    def find_element_ancestor(
            self, element: WebElement, ancestry_level: int, throw_exception: bool = True) -> Optional[WebElement]:

        ancestry = "/.." * ancestry_level
        element_runtimeid = element.get_attribute("RuntimeId")
        try:
            return \
                self.find_element_by_xpath("//*[@RuntimeId='{}']/{}".format(element_runtimeid, ancestry))
        except exceptions.NoSuchElementException as e:
            logger.debug("Element not found")
            if throw_exception:
                raise e
            logger.debug(str(e))
            return None

    def read_element_text(self, element: WebElement) -> str:
        try:
        #    logger.debug('Reading element ({}) text'.format(self.__get_element_info_text(element)))
            print("Reading element ")
            try:
                element.send_keys(Keys.NULL)
            except WebDriverException:
                pass
            return element.text
        except Exception as e:
            logger.error("Exception while reading element text", False)
            logger.error(e, False)

    def set_slider_value(self, slider: WebElement, name: str, value: str, vertical: bool = False) -> bool:
      #  logger.debug('Setting {} slider value to: {}'.format(name, value))
        current_value = slider.text.split('.')[0]

        if not self.is_element_enabled(slider):
            return False

        if current_value == str(value):
            return True

        if not vertical:
            key_add, key_sub = Keys.ARROW_RIGHT, Keys.ARROW_LEFT
        else:
            key_add, key_sub = Keys.ARROW_UP, Keys.ARROW_DOWN

        key = key_add if value == 'MAX' or int(value) > int(current_value) else key_sub
        if value == 'MAX':
            last_value = None
            while last_value != current_value:
                last_value = slider.text
                slider.send_keys(key)
                current_value = slider.text
        else:
            while current_value != str(value):
                slider.send_keys(key)
                current_value = slider.text.split('.')[0]

        time.sleep(2)
        return True

    def save_element_screenshot(self, element: WebElement, path: str) -> bool:
        try:
            logger.debug(
                'Saving element ({}) screenshot to temp location'.format(self.__get_element_info_text(element)))
            if not os.path.exists(os.path.dirname(path)):
                os.makedirs(os.path.dirname(path))
            return element.screenshot(path)
        except Exception as e:
            logger.error("Exception while reading element text", False)
            logger.error(e, False)

    def send_keys(self, element: WebElement, text: str) -> None:
        try:
            logger.debug('Sending "{}" text to element ({})'.format(text, self.__get_element_info_text(element)))
            element.send_keys(text)
        except Exception as e:
            logger.error("Exception while sending text to element", False)
            logger.error(e, False)

    def is_element_displayed(self, element: WebElement) -> bool:
        try:
            logger.debug('Checking if element: {} is displayed'.format(self.__get_element_info_text(element)))
            return element.is_displayed()
        except Exception as e:
            logger.error("Exception while checking if element is displayed", False)
            logger.error(e, False)

    def is_element_enabled(self, element: WebElement) -> bool:
        try:
         #   logger.debug('Checking if element: {} is enabled'.format(self.__get_element_info_text(element)))
            return element.is_enabled()
        except Exception as e:
         #   logger.error("Exception while checking if element is enabled", False)
         #   logger.error(e, False)
            print("Exception while checking if element is enabled")

    def is_element_selected(self, element: WebElement, retries: int = 3) -> bool:
        try:
        #    logger.debug('Checking if element: {} is selected'.format(self.__get_element_info_text(element)))
            return element.is_selected()
        except Exception as e:
            if retries > 0:
                return self.is_element_selected(element, retries - 1)
            logger.error(e, False)

    def has_keyboard_focus(self, element: WebElement) -> bool:
        try:
            logger.debug('Checking if element: {} has keyboard focus'.format(self.__get_element_info_text(element)))
            return element.get_attribute("HasKeyboardFocus") == 'true'
        except Exception as e:
            logger.error("Exception while checking if element has keyboard focus", False)
            logger.error(e, False)

    def get_element_location(self, element: WebElement) -> List[int]:
        logger.debug('Getting element: {} location'.format(self.__get_element_info_text(element)))
        try:
            element_rect = self.get_element_rect(element)
            return [element_rect['left'], element_rect['top'],
                    element_rect['width'], element_rect['height']]
        except Exception as e:
            logger.error("Exception while checking element location", False)
            logger.error(e, False)

    def get_element_rect(self, element: WebElement) -> Dict[str, int]:
        logger.debug("Getting element: {} bounding rectangle".format(self.__get_element_info_text(element)))
        try:
            rect = element.get_attribute("BoundingRectangle").split(" ")
            return {x.split(":")[0].lower(): int(x.split(":")[1]) for x in rect}
        except Exception as e:
            logger.error("Exception while getting element bounding rectangle", False)
            logger.error(e, False)

    def set_short_implicitly_wait(self) -> None:
        self.__driver.implicitly_wait(2)

    def set_default_wait(self) -> None:
        self.__driver.implicitly_wait(self.__default_implicitly_wait)

    def get_element_img_as_base64(self, element: WebElement) -> str:
        logger.debug('Getting element: {} as base 64 img'.format(self.__get_element_info_text(element)))
        try:
            return str(element.screenshot_as_base64)
        except Exception as e:
            logger.error("Exception while checking if element is selected", False)
            logger.error(e, False)

    def move_to_element(self, element: WebElement) -> bool:
        logger.debug("Moving cursor to element {}".format(self.__get_element_info_text(element)))
        action = ActionChains(self.__driver)
        action.move_to_element(element)
        action.perform()
        return True

    def drag_and_drop_element_by_offset(self, element: WebElement, offset: Tuple[int]) -> bool:
        logger.debug("Moving element {} by x: {} y: {}".
                     format(self.__get_element_info_text(element), offset[0], offset[1]))

        action = ActionChains(self.__driver)
        action.move_to_element(element)\
            .click_and_hold()\
            .pause(1)\
            .move_by_offset(*offset)\
            .pause(1)\
            .release()\
            .perform()
        return True

    def drag_and_drop_element_to_element_with_offset(self, element: WebElement, element2: WebElement,
                                                     offset: Tuple[int, int] = (0, 0)) -> bool:
        logger.debug("Moving element {} by x: {} y: {}".format(self.__get_element_info_text(element), offset[0], offset[1]))

        action = ActionChains(self.__driver)
        action.click_and_hold(element)
        action.pause(2)
        action.move_to_element_with_offset(element2, *offset)
        action.pause(2)
        action.release()
        action.perform()
        return True

    def set_window_position(self, x: int, y: int) -> bool:
        logger.debug("Setting window position to x:{} y:{}".format(x, y))
        self.__driver.set_window_position(x, y)
        return [x, y] == list(self.__driver.get_window_position().values())

    def get_window_position(self) -> Tuple[int, int]:
        return self.__driver.get_window_position().values()

    def set_window_size(self, x:int, y:int) -> bool:
        self.__driver.set_window_size(x,y)
        time.sleep(1)
        return self.__driver.get_window_size() == {'width': x, 'height': y}

    def is_maximized(self) -> bool:
        logger.debug("Checking if main IGCC window is maximized")
        main_window = self.find_element_by_class_name("ApplicationFrameWindow")
        return main_window.get_attribute("Window.WindowVisualState") == 'Maximized'

    def is_minimized(self) -> bool:
        logger.debug("Checking if main IGCC window is minimized")
        main_window = self.find_element_by_class_name("ApplicationFrameWindow")
        return main_window.get_attribute("Window.WindowVisualState") == 'Minimized'

    def get_page_source(self) -> str:
        logger.debug("Getting driver page source")
        return self.__driver.page_source

    @staticmethod
    def get_element_automation_id(element: WebElement) -> str:
      #  logger.debug("Getting element automation id")
        return element.get_attribute("AutomationId")

    @staticmethod
    def get_element_name(element: WebElement) -> str:
        logger.debug("Getting element automation id")
        return element.get_attribute("Name")

    def scroll_to_element(self, element: WebElement) -> bool:
    #    logger.debug("Scrolling to element {}".format(self.get_element_automation_id(element)))
        return self.__driver.scroll(None, element)

def click_button_by_id(driver: AppiumDriver, name: str, button_id: Optional[str] = None) -> bool:
    logger.debug('Clicking {} button'.format(name))
    if button_id is None:
        button_id = name
    button = driver.find_element_by_id(button_id)
    driver.click_element(button)
    return True
