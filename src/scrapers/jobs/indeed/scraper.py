# author: long nguyen (nguyenhailong253@gmail.com)

import sys
from .utils import LATEST_QUERY, POP_QUERY, INFO_SPECS, PARENT, CHILDREN, TAG, ATTRS, JD_SPECS
from src.scrapers.jobs.indeed.base import IndeedScraperBase


class IndeedScraper(IndeedScraperBase):
    ''' au.indeed.com scraper '''

    def __init__(self):
        super().__init__()

    def scrape_job_desc(self, soup):
        jd = self.get_single_div(soup, JD_SPECS[TAG], JD_SPECS[ATTRS])

    def scrape_job_info(self, div, specs):
        ''' Iterate through utils dict and scrape all keys '''
        # print(div)
        # print("\n")

        self.initialize_data()
        for key, value in specs.items():
            try:
                if value[TAG]:
                    result = self.get_single_div(div, value[TAG], value[ATTRS])
                    print(key)
                    print("\n")

                    print(result)
                    print("\n")
                else:
                    result = self.get_attributes(div, value[ATTRS])
                    self.data[key] = result
                    print(key)
                    print("\n")

                    print(result)
                    print("\n")
            except Exception as e:
                print(e)

    def iterate_job_articles(self, divs):
        ''' Iterate through list of job articles and call scrape func '''

        divs = divs[:1]  # test

        for div in divs:
            self.scrape_job_info(div, INFO_SPECS[CHILDREN])
            url = self.format_jd_url(self.data['src_id'])
            print(url)
            soup = self.request_url(url)

            self.scrape_job_desc(soup)

    def iterate_pages(self, url, islatest=0):
        ''' Format page url & get list of job articles '''

        if islatest:
            query = LATEST_QUERY
        else:
            query = POP_QUERY

        page = 0
        done = False
        # while not done:
        url_page = self.format_page_url(url, query, page)
        print(url_page)
        soup = self.request_url(url_page)
        divs = self.get_list_divs(
            soup, INFO_SPECS[PARENT][TAG], INFO_SPECS[PARENT][ATTRS])

        self.iterate_job_articles(divs)
        page += 1

    def iterate_subcategory(self, subcate):
        ''' Iterate through list of subcate and call iterate_pages '''

        # islatest = sys.argv[1]
        for name, url in subcate.items():
            self.iterate_pages(url)
            break

    def run(self):
        url = 'https://au.indeed.com/browsejobs/Accounting'
        s = self.get_subcategories(url)
        self.iterate_subcategory(s)
