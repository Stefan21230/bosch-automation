import random

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.touch_action import TouchAction
import subprocess
from selenium.webdriver.remote.errorhandler import InvalidSelectorException


class BaseMethods:
    def __init__(self, driver):
        self.driver = driver

    def click(self, locator, time_out=10):
        """
        Click on the WebElement.
        """
        self.wait_for_element_to_be_clickable(locator, time_out).click()

    def input(self, text: str, locator, time_out=10):
        """
        Input in the WebElement.
        """
        self.wait_for_element_to_be_presence(locator, time_out).send_keys(text)

    def input_with_clear(self, text: str, locator, time_out=10):
        """
        Input in the WebElement but select all text in input field before that.
        """
        self.wait_for_element_to_be_presence(locator, time_out).clear()
        self.wait_for_element_to_be_presence(locator, time_out).send_keys(text)

    def click_on_back_button(self):
        """
        Click on the device back button.
        """
        self.driver.back()

    def get_visible_element_text(self, locator, time_out=10):
        """
        Method get WebElement text.
        """
        return self.wait_for_element_to_be_visible(locator, time_out).text

    def wait_for_element_to_be_visible(self, locator, time_out=10):
        """
        Method check is WebElement visible.
        """
        try:
            return WebDriverWait(self.driver, time_out).until(EC.visibility_of_element_located(locator))
        except Exception:
            raise Exception(
                "Couldn't find element that has locator: {} , for time period of: {} seconds.".format(locator[1],
                                                                                                      time_out))

    def wait_for_element_to_be_clickable(self, locator, time_out=10):
        """
        Method check is WebElement clickable.
        """
        try:
            return WebDriverWait(self.driver, time_out).until(EC.element_to_be_clickable(locator))
        except Exception:
            raise Exception(
                "Couldn't find element that has locator: {} , for time period of: {} seconds.".format(locator[1],
                                                                                                      time_out))

    def wait_for_elements_to_be_visible(self, locator, time_out=10):
        """
        Method check is WebElement visible.
        """
        try:
            return WebDriverWait(self.driver, time_out).until(EC.visibility_of_all_elements_located(locator))
        except Exception:
            raise Exception(
                "Couldn't find element that has locator: {} , for time period of: {} seconds.".format(locator[1],
                                                                                                      time_out))

    def wait_for_element_to_be_presence(self, locator, time_out=10):
        """
        Method check if WebElement  is present on the DOM
        of a page. This does not necessarily mean that the element is visible.
        locator - used to find the element returns the WebElement once it is located
        """
        try:
            return WebDriverWait(self.driver, time_out).until(EC.presence_of_element_located(locator))
        except Exception:
            raise Exception(
                "Couldn't find element that has locator: {} , for time period of: {} seconds.".format(locator[1],
                                                                                                      time_out))

    def wait_for_elements_to_be_presence(self, locator, time_out=10):
        """
        Method check if WebElements are present on the DOM
        of a page. This does not necessarily mean that the elements is visible.
        locator - used to find the elements returns the WebElement once it is located
        """
        try:
            return WebDriverWait(self.driver, time_out).until(EC.presence_of_all_elements_located(locator))
        except Exception:
            raise Exception(
                "Couldn't find element that has locator: {} , for time period of: {} seconds.".format(locator[1],
                                                                                                      time_out))

    def unhandled_wait_for_element_to_be_visible(self, locator, time_out=0.5):
        """
        Method check is WebElement visible.
        """
        try:
            return WebDriverWait(self.driver, time_out).until(EC.visibility_of_element_located(locator))
        except Exception:
            pass

    def scroll_into_the_map(self, locator, element_found, viewport_value, time_out=10):
        """
        This method swiping into the map and with tap action trying to find the station on the current visible map size,
        if the station isn't found method will swiping again and repeats the search. It will swipe to the right until
        the end of the map size when it will swipe down for a 300px and starting swipe to left and search for a station
        and so it repeats the action until he finds the station.
        :param locator:
        :param element_found:
        :param viewport_value:
        :param time_out:
        :return: return the id of the station as a string
        """
        map_element = self.wait_for_element_to_be_clickable(locator, time_out)
        map_element_rec = map_element.rect
        map_element_height = map_element_rec['height']
        map_element_width = map_element_rec['width']
        device_screen_size = subprocess.getoutput("adb shell wm size")
        ds_splitted = device_screen_size.split("x")
        ds_x = int(ds_splitted[0].replace('Physical size: ', '')) / 2
        ds_y = int(ds_splitted[1]) / 2

        while True:
            self.swipe_to_down(viewport_value, ds_x, ds_y)
            element = self.swipe_to_right(viewport_value, element_found, ds_x, ds_y,
                                          map_element_height, map_element_width)
            if element:
                return element
            self.swipe_to_down(viewport_value, ds_x, ds_y)
            element = self.swipe_to_left(viewport_value, element_found, ds_x, ds_y,
                                         map_element_height, map_element_width)
            if element:
                return element
            self.swipe_to_down(viewport_value, ds_x, ds_y)

    def swipe_to_right(self, viewport_value, element_found, ds_x, ds_y, map_height, map_width):
        while True:
            element = self.tapping_into_the_map(element_found, map_height, map_width)
            if element:
                return element
            subprocess.getoutput("adb shell input touchscreen swipe {} {} {} {}".format(ds_x + 400, ds_y, ds_x, ds_y))  # swipe to right
            viewport_coordinates = self.get_visible_element_text(viewport_value)
            viewport_right_axis = int(viewport_coordinates.split(',')[2])
            if viewport_right_axis > 1950:
                return_back = viewport_right_axis - 1950
                subprocess.getoutput("adb shell input touchscreen swipe {} {} {} {}".
                                     format(ds_x, ds_y, ds_x + return_back, ds_y))  # return to left
                break

    def swipe_to_down(self, viewport_value, ds_x, ds_y, stop_swiping=True):
        while True:
            subprocess.getoutput("adb shell input touchscreen swipe {} {} {} {}".format(ds_x, ds_y + 600, ds_x, ds_y))  # swipe to down
            viewport_coordinates = self.get_visible_element_text(viewport_value)
            viewport_down_splitted = viewport_coordinates.split(',')[3]
            viewport_down_axis = int(viewport_down_splitted.replace(')', ''))
            if viewport_down_axis > 2150:
                return_back = viewport_down_axis - 2150
                subprocess.getoutput("adb shell input touchscreen swipe {} {} {} {}".
                                     format(ds_x, ds_y, ds_x, ds_y + return_back))  # return to up
                break
            if stop_swiping:
                break

    def swipe_to_left(self, viewport_value, element_found, ds_x, ds_y, map_height, map_width):
        while True:
            element = self.tapping_into_the_map(element_found, map_height, map_width)
            if element:
                return element

            subprocess.getoutput("adb shell input touchscreen swipe {} {} {} {}"
                                 .format(ds_x, ds_y, ds_x + 400, ds_y))  # swipe to left
            viewport_coordinates = self.get_visible_element_text(viewport_value)
            viewport_left_splitted = viewport_coordinates.split(',')[0]
            viewport_left_axis = int(viewport_left_splitted.replace('(', ''))
            if viewport_left_axis < -1:
                return_back = abs(viewport_left_axis)
                subprocess.getoutput("adb shell input touchscreen swipe {} {} {} {}".
                                     format(ds_x, ds_y, ds_x + return_back, ds_y))  # return to left
                break

    def tapping_into_the_map(self, element_found, map_height, map_width):
        devide_num = 5
        move_y = map_height / devide_num
        move_x = map_width / devide_num
        move_axis_y = move_y
        move_axis_x = move_x
        for i in range(devide_num):
            if move_axis_x == map_width:
                move_axis_x = move_axis_x - 50
            TouchAction(self.driver).tap(x=0 + move_axis_x, y=0).perform()
            element = self.unhandled_wait_for_element_to_be_visible(element_found)
            if element:
                return element.text
            for x in range(devide_num):
                TouchAction(self.driver).tap(x=0 + move_axis_x, y=0 + move_axis_y).perform()
                element = self.unhandled_wait_for_element_to_be_visible(element_found)
                if element:
                    return element.text
                move_axis_y += move_y
            move_axis_y = 0
            move_axis_x += move_x
