# author: long nguyen (nguyenhailong253@gmail.com)

import time
import requests
import psycopg2
import logging
import logging.handlers as handlers
from src.base.base import Scraper
from bs4 import BeautifulSoup
from .utils.settings import SPECS_ORDER


ATTRS_TAGS = ['href']
NULL = '<missing>'


class JobScraperBase(Scraper):
    ''' Parent class for Australian jobs scraper '''

    def __init__(self):
        super().__init__()
        self.headers = self.get_headers()
        self.proxies = self.get_proxies()
        self.data = {}

    def set_up_logger(self, source):
        ''' Setup logging file named after source '''

        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.DEBUG)

        logHandler = handlers.RotatingFileHandler(
            './src/scrapers/jobs/{}/logs/scrape_log.log'.format(source),
            maxBytes=1500000,
            backupCount=0)

        formatter = logging.Formatter("%(levelname)s:%(message)s")
        logHandler.setFormatter(formatter)
        logHandler.setLevel(logging.DEBUG)

        if not self.log.handlers:
            self.log.addHandler(logHandler)

    def request_url(self, url):
        ''' Request URL and return soup object, try 3 times if fails '''

        done = False
        attempt = 0
        soup = None
        while not done:
            try:
                html_page = requests.get(url, headers=self.headers)
                status = html_page.status_code

                # check status code
                if 300 <= status < 400:
                    print("-- Being redirected, code: {} \n".format(status))
                    attempt += 1
                elif status == 200:
                    soup = BeautifulSoup(html_page.text, "html.parser")
                    done = True

            except Exception as e:
                print("-Error while requesting URL: {} \n".format(e))
                if attempt >= 3:
                    done = True
                attempt += 1
                time.sleep(0.2)
        return soup

    def initialize_data(self):
        ''' Initialize all key, value of data to null'''
        for key in SPECS_ORDER:
            self.data[key] = NULL

    # +  -  -  - GET HTML DIV -  -  - +

    def get_single_div(self, soup, tag, attribute):
        if attribute in ATTRS_TAGS:
            result = soup.find(tag)
        else:
            result = soup.find(tag, attribute)

        if result:
            return result
        return None

    def get_list_divs(self, soup, tag, attribute):
        results = soup.find_all(tag, attribute)
        if results:
            return results
        return None

    def get_attributes(self, div, attrs):
        attribute = div.get(attrs)

        if attribute:
            return attribute
        return None

    # +  -  -  - QUERIES -  -  - +

    def save_data(self, src, values):
        pass

    def check_existed_data(self, source):
        ''' For now, have to check from individual tables '''
        pass

    # +  -  -  - PROCESS DATA -  -  - +
