from tests.base_test import BaseTest
from methods import login_methods, main_page_methods


class LoginAndFindStationTest(BaseTest):
    def test_login_and_find_station(self, user_config):
        self.login_methods = login_methods.LoginMethods(self.driver)
        self.main_page_methods = main_page_methods.MainPageMethods(self.driver)

        self.login_methods.unsuccessful_login(user_config("username"), user_config("wrong_password"))

        self.login_methods.login_into_app(user_config("username"), user_config("password"))

        self.main_page_methods.find_station()
