from pytest import fixture
from appium import webdriver
from pathlib import Path
from resources.path_data import resources_path, screen_recordings_path
import json
import os
import base64


@fixture(scope="function")
def setup(request, initialize_driver):
    driver = initialize_driver
    request.cls.driver = driver
    driver.start_recording_screen(videoType='libx264', forceRestart=True, videoQuality='low',
                                       pixelFormat='yuv420p', timeLimit=900, bugReport='true')
    yield
    stop_recording_screen(driver)
    driver.quit()


@fixture(scope="function")
def initialize_driver():
    desired_caps = {
        'platformName': 'Android',
        'automationName': 'UIAutomator2',
        'appPackage': 'com.bosch.test7',
        'appActivity': 'com.bosch.test7.MainActivity',
        'deviceName': 'device',
        'udid': 'R9AR60GQA6J',
        'platformVersion': '11.0',
    }
    driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_caps)

    return driver


def stop_recording_screen(driver):
    video_raw = driver.stop_recording_screen()
    video_name = driver.session_id
    is_exist = os.path.exists(screen_recordings_path)
    if not is_exist:
        os.makedirs(screen_recordings_path)
    filepath = os.path.join(str(screen_recordings_path), video_name + ".mp4")

    with open(filepath, "wb+") as vd:
        vd.write(base64.b64decode(video_raw))


def pytest_addoption(parser):
    parser.addoption(
        "--user",
        action="store",
        default="user_stefan",
        help="users: user_stefan"
    )


@fixture(scope='session')
def get_user(request):
    return request.config.getoption("--user")


@fixture(scope='function')
def user_config(get_user):
    def _json_param(string_of_json):
        json_input_file = Path(resources_path, 'user_parameters.json')
        with open(file=json_input_file, encoding="utf-8") as json_data:
            json_user_data = json.load(json_data)
            i = 0
            for i in range(len(json_user_data[get_user])):
                return json_user_data[get_user][i][string_of_json]

    return _json_param
