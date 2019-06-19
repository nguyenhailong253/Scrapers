# author: long nguyen (nguyenhailong253@gmail.com)

from src.base.base import Scraper


class NewsScraperBase(Scraper):
    ''' Parent class for all news scraper '''

    def __init__(self):
        super().__init__()
        self.headers = self.get_headers()
        self.proxies = self.get_proxies()

    # +  -  -  - REQUESTS -  -  - +

    def request_url(self, url):
        pass

    # +  -  -  - FIND HTML TAGS -  -  - +

    def get_parent_div(self, soup):
        pass

    def get_children_list(self):
        pass

    # +  -  -  - PROCESSING DATA -  -  - +

    def initialize_data(self):
        ''' Initialize 1 obj data with necessary keys and empty values '''
        pass

    def get_text_data(self):
        pass
