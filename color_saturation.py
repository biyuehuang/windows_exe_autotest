from application import Application
from assumption import Assumption

class ColorSaturation():
    def __init__(self):
        super(ColorSaturation, self).__init__()
        self.valbin = None

    __go_to_display_page = None
    __set_three_different_saturation_values = None
    __verify_display_saturation_changes_appropriately = None
    __repeat_steps_for_second_display = None
    __button_reset_advance = None

    #expected_sat_vals = [i for i in range(100,-1,-1)]
    #expected_sat_vals = [i for i in range(0, 101)]
    expected_sat_vals = [48, 52, 50]

    #expected_hue_vals = [i for i in range(180,-181,-1)]
    #expected_hue_vals = [i for i in range(-180,181)]
    expected_hue_vals = [0, 4, 2]

    #expected_backlight_vals = [i for i in range(100, -1, -1)]
    #expected_backlight_vals = [i for i in range(0,101)] ##
    expected_backlight_vals = [10, 50, 30]

    #expected_brightness_vals = [i for i in range(100,-1,-1)] ##
    #expected_brightness_vals = [i for i in range(0, 101)]
    expected_brightness_vals = [46,58,51]

    #expected_contrast_vals = [i for i in range(100,-1,-1)] ##
    #expected_contrast_vals = [i for i in range(0, 101)]
    expected_contrast_vals = [45,52,49]  ##

    #expected_custome_red_vals = [i for i in range(100,-1,-1)] ##
    #expected_custome_red_vals = [i for i in range(0, 101)]  ##
    expected_custome_red_vals = [48, 52, 51]

   # expected_custome_green_vals = [i for i in range(100,-1,-1)] ##
    #expected_custome_green_vals = [i for i in range(0, 101)]
    expected_custome_green_vals = [49, 53, 52]

    #expected_custome_blue_vals = [i for i in range(100,-1,-1)] ##
    #expected_custome_blue_vals = [i for i in range(0, 101)]
    expected_custome_blue_vals = [47, 58, 55]
    assumptions = []

    def prepare_assumptions(self):
        #super(ColorSaturation, self).prepare_assumptions()
        self.assumptions.append(Assumption(1, 'Go to Advance Page'))
        self.assumptions.append(Assumption(2, 'Set three different Saturation values'))
        self.assumptions.append(Assumption(3, 'Verify Advance Saturation changes appropriately'))
        self.assumptions.append(Assumption(4, 'Set three different hue values'))
        self.assumptions.append(Assumption(5, 'Verify Advance hue changes appropriately'))
        self.assumptions.append(Assumption(6, 'Set three different backlight values'))
        self.assumptions.append(Assumption(7, 'Verify Advance backlight changes appropriately'))
        self.assumptions.append(Assumption(8, 'Click Button Reset advance'))

        self.assumptions.append(Assumption(9, 'Go to Brightness/Contrast Page'))
        self.assumptions.append(Assumption(10, 'Set three different Brightness values'))
        self.assumptions.append(Assumption(11, 'Verify Brightness changes appropriately'))

        self.assumptions.append(Assumption(12, 'Set three different Contrast values'))
        self.assumptions.append(Assumption(13, 'Verify Contrast changes appropriately'))
        self.assumptions.append(Assumption(14, 'Click Button Reset Brightness/Contrast'))

        self.assumptions.append(Assumption(15, 'Go to Display Page'))
        self.assumptions.append(Assumption(16, 'Set three different Custome Red values'))
        self.assumptions.append(Assumption(17, 'Verify display Custome Red changes appropriately'))
        self.assumptions.append(Assumption(18, 'Set three different Custome Green values'))
        self.assumptions.append(Assumption(19, 'Verify display Custome Green changes appropriately'))
        self.assumptions.append(Assumption(20, 'Set three different Custome Blue values'))
        self.assumptions.append(Assumption(21, 'Verify display Custome Blue changes appropriately'))
        self.assumptions.append(Assumption(22, 'Click Button Reset custome RGB'))
        self.assumptions.append(Assumption(23, 'Click Eye Checkbox'))
        self.assumptions.append(Assumption(24, 'Click Standard Checkbox'))
        self.assumptions.append(Assumption(25, 'Click Vivid Checkbox'))
        self.assumptions.append(Assumption(26, 'Click Minimize APP'))

    def set_up(self):
       # super(ColorSaturation, self).set_up()  # win app driver
        self.app = Application()  ##

    def execute(self):
        __button_monitor1 = self.app.menu_actions.go_to_button_monitor1()
        #__button_monitor2 = self.app.menu_actions.go_to_button_monitor2()
        #__button_monitor3 = self.app.menu_actions.go_to_button_monitor3()
        #__button_monitor4 = self.app.menu_actions.go_to_button_monitor4()

        display_page = self.app.display_page
        print("************************ Advance execute ***************************")
        # 1
        self.__go_to_advance_page = self.app.menu_actions.go_to_advance_page()
        # 2
        print("************************ saturation start ***************************")
        sat_set = []
        sat_vals = []
        for sat_val in self.expected_sat_vals:
            sat_set.append(self.set_sat_for_disp(sat_val, 1))
            sat_vals.append(display_page.get_saturation_slider_value())
        self.__set_three_different_saturation_values = all(sat_set)
        # 4
        self.__verify_display_saturation_changes_appropriately = self.verify_display_sat(sat_vals)

        print("********** saturation finished *****************")
        ##########################
        print("************************ hue start ***************************")
        hue_set = []
        hue_vals = []
        for hue_val in self.expected_hue_vals:
            hue_set.append(self.set_hue_for_disp(hue_val, 1))
            hue_vals.append(display_page.get_hue_slider_value())
        self.__set_three_different_hue_values = all(hue_set)
        # 4
        self.__verify_display_hue_changes_appropriately = self.verify_display_hue(hue_vals)
        print("********** hue finished *****************")

        ##############
        print("************************ backlight start ***************************")
        backlight_set = []
        backlight_vals = []
        for backlight_val in self.expected_backlight_vals:
            print(backlight_val)
            backlight_set.append(self.set_backlight_for_disp(backlight_val, 1))
            backlight_vals.append(display_page.get_backlight_slider_value())
        self.__set_three_different_backlight_values = all(backlight_set)
        # 4
        self.__verify_display_backlight_changes_appropriately = self.verify_display_backlight(backlight_vals)

        print("********** backlight finished *****************")
        ######### Reset Advance
        self.__button_reset_advance = self.app.menu_actions.go_to_button_advance_reset()

        print("************************ Brightness/Contrast execute ***************************")
        self.__go_to_setting_page = self.app.menu_actions.go_to_setting_page()

        print("************************ Brightness start ***************************")
        brightness_set = []
        brightness_vals = []
        for brightness_val in self.expected_brightness_vals:
            brightness_set.append(self.set_brightness_for_disp(brightness_val, 1))
            brightness_vals.append(display_page.get_brightness_slider_value())
        self.__set_three_different_brightness_values = all(brightness_set)
        # 4
        self.__verify_display_brightness_changes_appropriately = self.verify_display_brightness(brightness_vals)

        print("********** Brightness finished *****************")

        print("************************ contrast start ***************************")
        contrast_set = []
        contrast_vals = []
        for contrast_val in self.expected_contrast_vals:
            print(contrast_val)
            contrast_set.append(self.set_contrast_for_disp(contrast_val, 1))
            print("****** get_contrast_slider_value ***")
            contrast_vals.append(display_page.get_contrast_slider_value())
        self.__set_three_different_contrast_values = all(contrast_set)
        # 4
        self.__verify_display_contrast_changes_appropriately = self.verify_display_contrast(contrast_vals)

        print("********** contrast finished *****************")
        ######### Reset Brightness/Contrast
        self.__button_reset_BrightnessContrast = self.app.menu_actions.go_to_button_setting_reset()

        ##################
        print("************************ Display execute ***************************")
        # 1
        self.__go_to_display_page = self.app.menu_actions.go_to_display_page()
        print("************************ custome start ***************************")
        __button_custome = self.app.menu_actions.go_to_button_custome()
        print("********** custome Red testing *****************")
        custome_red_set = []
        custome_red_vals = []
        __button_red = self.app.menu_actions.go_to_button_red()
        for custome_red_val in self.expected_custome_red_vals:
            custome_red_set.append(self.set_custome_red_for_disp(custome_red_val, 1))
            custome_red_vals.append(display_page.get_custome_red_slider_value())
        self.__set_three_different_custome_red_values = all(custome_red_set)
        # 4
        self.__verify_display_custome_red_changes_appropriately = self.verify_display_custome_red(custome_red_vals)

        print("********** custome green testing *****************")
        custome_green_set = []
        custome_green_vals = []
        __button_green = self.app.menu_actions.go_to_button_green()
        for custome_green_val in self.expected_custome_green_vals:
            custome_green_set.append(self.set_custome_green_for_disp(custome_green_val, 1))
            custome_green_vals.append(display_page.get_custome_green_slider_value())
        self.__set_three_different_custome_green_values = all(custome_green_set)
        # 4
        self.__verify_display_custome_green_changes_appropriately = self.verify_display_custome_green(custome_green_vals)

        print("********** custome blue testing *****************")
        custome_blue_set = []
        custome_blue_vals = []
        __button_blue = self.app.menu_actions.go_to_button_blue()
        for custome_blue_val in self.expected_custome_blue_vals:
            custome_blue_set.append(self.set_custome_blue_for_disp(custome_blue_val, 1))
            custome_blue_vals.append(display_page.get_custome_blue_slider_value())
        self.__set_three_different_custome_blue_values = all(custome_blue_set)
        # 4
        self.__verify_display_custome_blue_changes_appropriately = self.verify_display_custome_blue(custome_blue_vals)
        self.__button_resetRGB = self.app.menu_actions.go_to_button_resetRGB()
        print("********** custome finished *****************")

        print("************************ eye start ***************************")
        __button_eye = self.app.menu_actions.go_to_button_eye()
        self.__checkbox_eye = self.app.menu_actions.go_to_checkbox_eye()

        print("************************ standard start ***************************")
        __button_standard = self.app.menu_actions.go_to_button_standard()
        self.__checkbox_standard = self.app.menu_actions.go_to_checkbox_standard()

        print("************************ vivid start ***************************")
        __button_vivid = self.app.menu_actions.go_to_button_vivid()
        self.__checkbox_vivid = self.app.menu_actions.go_to_checkbox_vivid()

        print("************************ minimize APP ***************************")
        self.__button_minmize_app = self.app.menu_actions.go_to_button_xmin()

    def process_results(self):
       # super(ColorSaturation, self).process_results()
        self.assumptions[0].set_result(self.__go_to_advance_page)
        self.assumptions[1].set_result(self.__set_three_different_saturation_values)
        self.assumptions[2].set_result(self.__verify_display_saturation_changes_appropriately)
        #self.assumptions[3].set_result(self.__repeat_steps_for_second_display)
        self.assumptions[3].set_result(self.__set_three_different_hue_values)
        self.assumptions[4].set_result(self.__verify_display_hue_changes_appropriately)
        #self.assumptions[3].set_result(self.__repeat_steps_for_second_display)
        self.assumptions[5].set_result(self.__set_three_different_backlight_values)
        self.assumptions[6].set_result(self.__verify_display_backlight_changes_appropriately)
        # self.assumptions[3].set_result(self.__repeat_steps_for_second_display)
        self.assumptions[7].set_result(self.__button_reset_advance)

        self.assumptions[8].set_result(self.__go_to_setting_page)
        self.assumptions[9].set_result(self.__set_three_different_brightness_values)
        self.assumptions[10].set_result(self.__verify_display_brightness_changes_appropriately)
        # self.assumptions[3].set_result(self.__repeat_steps_for_second_display)
        self.assumptions[11].set_result(self.__set_three_different_contrast_values)
        self.assumptions[12].set_result(self.__verify_display_contrast_changes_appropriately)
        # self.assumptions[3].set_result(self.__repeat_steps_for_second_display)
        self.assumptions[13].set_result(self.__button_reset_BrightnessContrast)
        self.assumptions[14].set_result(self.__go_to_display_page)
        self.assumptions[15].set_result(self.__set_three_different_custome_red_values)
        self.assumptions[16].set_result(self.__verify_display_custome_red_changes_appropriately)
        self.assumptions[17].set_result(self.__set_three_different_custome_green_values)
        self.assumptions[18].set_result(self.__verify_display_custome_green_changes_appropriately)
        self.assumptions[19].set_result(self.__set_three_different_custome_blue_values)
        self.assumptions[20].set_result(self.__verify_display_custome_blue_changes_appropriately)
        self.assumptions[21].set_result(self.__button_resetRGB)
        self.assumptions[22].set_result(self.__checkbox_eye)
        self.assumptions[23].set_result(self.__checkbox_standard)
        self.assumptions[24].set_result(self.__checkbox_vivid)
        self.assumptions[25].set_result(self.__button_minmize_app)

    def tear_down(self):
        self.app.shut_down()

    def set_sat_for_disp(self, sat_val, disp_num):
        display_page = self.app.display_page
        return display_page.set_saturation_slider(str(sat_val))

    def verify_display_sat(self, sat_vals) -> bool:
        are_sat_vals_equal = [self.expected_sat_vals[index] == sat_vals[index] for index in range(len(sat_vals))]
        print(are_sat_vals_equal,"***************************")
        return all(are_sat_vals_equal)

    def repeat_for_sec_disp(self):
        sat_set = []
        sat_vals = []
        for sat_val in self.expected_sat_vals:
            sat_set.append(self.set_sat_for_disp(sat_val, 2))
            sat_vals.append(self.app.display_page.color_tab.get_saturation_slider_value())

        _set_three_different_saturation_values = all(sat_set)

        _verify_display_saturation_changes_appropriately = self.verify_display_sat(sat_vals)

        return (
            _set_three_different_saturation_values and
            _verify_display_saturation_changes_appropriately
        )

####################### hue

    def set_hue_for_disp(self, hue_val, disp_num):
        display_page = self.app.display_page
        return display_page.set_hue_slider(str(hue_val))

    def verify_display_hue(self, hue_vals) -> bool:
        are_hue_vals_equal = [self.expected_hue_vals[index] == hue_vals[index] for index in range(len(hue_vals))]
        print(are_hue_vals_equal,"***************************")
        return all(are_hue_vals_equal)

################ backlight
    def set_backlight_for_disp(self, backlight_val, disp_num):
        display_page = self.app.display_page
        #display_page.click_display(disp_num)
        return display_page.set_backlight_slider(str(backlight_val))

    def verify_display_backlight(self, backlight_vals) -> bool:
        are_backlight_vals_equal = [self.expected_backlight_vals[index] == backlight_vals[index] for index in range(len(backlight_vals))]
        print(are_backlight_vals_equal,"***************************")
        return all(are_backlight_vals_equal)
######### brightness

    def set_brightness_for_disp(self, brightness_val, disp_num):
        display_page = self.app.display_page
        #display_page.click_display(disp_num)
        return display_page.set_brightness_slider(str(brightness_val))

    def verify_display_brightness(self, brightness_vals) -> bool:
        are_brightness_vals_equal = [self.expected_brightness_vals[index] == brightness_vals[index] for index in range(len(brightness_vals))]
        print(are_brightness_vals_equal,"***************************")
        return all(are_brightness_vals_equal)
####### contrast

    def set_contrast_for_disp(self, contrast_val, disp_num):
        display_page = self.app.display_page
        #display_page.click_display(disp_num)
        return display_page.set_contrast_slider(str(contrast_val))

    def verify_display_contrast(self, contrast_vals) -> bool:
        are_contrast_vals_equal = [self.expected_contrast_vals[index] == contrast_vals[index] for index in range(len(contrast_vals))]
        print(are_contrast_vals_equal,"***************************")
        return all(are_contrast_vals_equal)
############### custome red
    def set_custome_red_for_disp(self, custome_red_val, disp_num):
        display_page = self.app.display_page
        return display_page.set_custome_red_slider(str(custome_red_val))

    def verify_display_custome_red(self, custome_red_vals) -> bool:
        are_custome_red_vals_equal = [self.expected_custome_red_vals[index] == custome_red_vals[index] for index in range(len(custome_red_vals))]
        print(are_custome_red_vals_equal,"***************************")
        return all(are_custome_red_vals_equal)

############### custome green
    def set_custome_green_for_disp(self, custome_green_val, disp_num):
        display_page = self.app.display_page
        return display_page.set_custome_green_slider(str(custome_green_val))

    def verify_display_custome_green(self, custome_green_vals) -> bool:
        are_custome_green_vals_equal = [self.expected_custome_green_vals[index] == custome_green_vals[index] for index in range(len(custome_green_vals))]
        print(are_custome_green_vals_equal,"***************************")
        return all(are_custome_green_vals_equal)

############### custome blue
    def set_custome_blue_for_disp(self, custome_blue_val, disp_num):
        display_page = self.app.display_page
        return display_page.set_custome_blue_slider(str(custome_blue_val))

    def verify_display_custome_blue(self, custome_blue_vals) -> bool:
        are_custome_blue_vals_equal = [self.expected_custome_blue_vals[index] == custome_blue_vals[index] for index in range(len(custome_blue_vals))]
        print(are_custome_blue_vals_equal,"***************************")
        return all(are_custome_blue_vals_equal)