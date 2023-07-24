from driver_appium import AppiumDriver
from slider import Slider


class DisplayPage:
    emulated_fhd_name = "DELL ST2220T"
    emulated_qhd_name = "DELL UP3214Q"

    def __init__(self, driver: AppiumDriver) -> None:
        self.__driver = driver
        self.__driver.find_element_by_id("TabAdvance")
        self.hue = DisplaySlider(self.__driver, 'Slider_hue')
        self.saturation = DisplaySlider(self.__driver, 'Slider_saturation')
        self.backlight = DisplaySlider(self.__driver, 'Slider_backlight')
        self.brightness = DisplaySlider(self.__driver, 'Slider_brightness')
        self.contrast = DisplaySlider(self.__driver, 'Slider_contrast')
        self.custome_red = DisplaySlider(self.__driver, 'Slider_red')
        self.custome_green = DisplaySlider(self.__driver, 'Slider_green')
        self.custome_blue = DisplaySlider(self.__driver, 'Slider_blue')

    def verify_hue_slider_is_visible(self) -> bool:
        return self.hue.get_element() is not None

    def get_hue_slider_value(self) -> int:
        return int(self.hue.get_value())

    def set_hue_slider(self, value: str) -> bool:
        return self.hue.set_value(value)

    def verify_saturation_slider_is_visible(self) -> bool:
        return self.saturation.get_element() is not None

    def get_saturation_slider_value(self) -> int:
        return int(self.saturation.get_value())

    def set_saturation_slider(self, value: str) -> bool:
        return self.saturation.set_value(value)

    def verify_backlight_slider_is_visible(self) -> bool:
        return self.backlight.get_element() is not None

    def get_backlight_slider_value(self) -> int:
        return int(self.backlight.get_value())

    def set_backlight_slider(self, value: str) -> bool:
        return self.backlight.set_value(value)

    def verify_brightness_slider_is_visible(self) -> bool:
        return self.brightness.get_element() is not None

    def get_brightness_slider_value(self) -> int:
        return int(self.brightness.get_value())

    def set_brightness_slider(self, value: str) -> bool:
        return self.brightness.set_value(value)

    def verify_contrast_slider_is_visible(self) -> bool:
        return self.contrast.get_element() is not None

    def get_contrast_slider_value(self) -> int:
        return int(self.contrast.get_value())

    def set_contrast_slider(self, value: str) -> bool:
        return self.contrast.set_value(value)

    def verify_custome_red_slider_is_visible(self) -> bool:
        return self.custome_red.get_element() is not None

    def get_custome_red_slider_value(self) -> int:
        return int(self.custome_red.get_value())

    def set_custome_red_slider(self, value: str) -> bool:
        return self.custome_red.set_value(value)

    def verify_custome_green_slider_is_visible(self) -> bool:
        return self.custome_green.get_element() is not None

    def get_custome_green_slider_value(self) -> int:
        return int(self.custome_green.get_value())

    def set_custome_green_slider(self, value: str) -> bool:
        return self.custome_green.set_value(value)

    def verify_custome_blue_slider_is_visible(self) -> bool:
        return self.custome_blue.get_element() is not None

    def get_custome_blue_slider_value(self) -> int:
        return int(self.custome_blue.get_value())

    def set_custome_blue_slider(self, value: str) -> bool:
        return self.custome_blue.set_value(value)


class DisplaySlider(Slider):
    def set_value(self, value: str) -> bool:
        print("[max, min]",self.max_value,self.min_value)
        print(value)
        if int(value) > self.max_value or int(value) < self.min_value:
            raise ValueError("Value for {} slider is out of range: {} - {}".format(
                self.automation_id, self.min_value, self.max_value))

        set_success = self.driver.set_slider_value(self.get_element(), self.automation_id, value)

        print(set_success)
        return set_success