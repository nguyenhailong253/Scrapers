# author: long nguyen (nguyenhailong253@gmail.com)

from .base import GovOfficialsScraperBase
from .utils import URLS

''' Scrape:
name,
title,
email,
dob,
term of office default = 2016-2021
'''


class GovOfficialsScraper(GovOfficialsScraperBase):
    ''' Government Officials Data Scraper '''

    def __init__(self):
        super().__init__()
        self.data = []

    def run(self):
        ''' Loop through URLS of each ministry and scrape '''

        for key, value in URLS.items():
            soup = self.request_url(value)

            if soup:
                div_list = self.get_div_list(soup, key)

                for div in div_list:
                    processed_data = self.gather_data(div, key)

                    if len(processed_data) > 1:
                        self.data.append(processed_data)

                    if not self.check_existed_data(processed_data['name']):
                        self.save_data(
                            processed_data['name'], processed_data['title'], processed_data['extra'], processed_data['office_term'])

        for item in self.data:
            print(item)
            print("\n")
