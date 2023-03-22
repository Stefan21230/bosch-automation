from methods.base_methods import BaseMethods
from pages import main_page


class MainPageMethods(BaseMethods):
    def find_station(self):
        station = self.scroll_into_the_map(locator=main_page.view_map, element_found=main_page.station_id_text,
                                           viewport_value=main_page.viewport_text)
        assert station == "123*fgh*789"
