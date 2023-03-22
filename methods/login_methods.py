from methods.base_methods import BaseMethods
from pages import login_page, main_page


class LoginMethods(BaseMethods):
    def login_into_app(self, username, password):
        self.input_with_clear(username, login_page.username_input_field)
        self.input_with_clear(password, login_page.password_input_field)
        self.click(login_page.login_button)
        self.wait_for_element_to_be_visible(main_page.view_map)

    def unsuccessful_login(self, username, wrong_password):
        self.input(username, login_page.username_input_field)
        self.input(wrong_password, login_page.password_input_field)
        self.click(login_page.login_button)
        login_error_message = self.get_login_error_message()
        assert login_error_message.text == "Login error"
        self.click_on_back_button()

    def get_login_error_message(self):
        elements = self.wait_for_elements_to_be_visible(login_page.login_error_message)
        for element in elements:
            if element.text == "Login error":
                return element



