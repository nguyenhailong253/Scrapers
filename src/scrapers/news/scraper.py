# author: long nguyen (nguyenhailong253@gmail.com)

from .base import NewsScraperBase


class ZingNewsScraper(NewsScraperBase):
    ''' Scraper for news.zing.vn '''

    def __init__(self):
        super().__init__()
        self.data = {}

    def get_categories_dict(self):
        ''' Get dict with category name as key, url as value '''
        pass

    # +  -  -  - PROCESS DATA -  -  - +

    def process_text(self):
        ''' Strip, replace newline or spaces neccessary '''
        pass

    def process_time(self):
        ''' Convert to standard time format '''
        pass

    # +  -  -  - QUERIES -  -  - +

    def save_news(self):
        pass

    def check_news_existed(self):
        pass
