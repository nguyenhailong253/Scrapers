# author: long nguyen (nguyenhailong253@gmail.com)

import re
import json
import time
import requests
import psycopg2
from .utils import ROOT, PARENTS, CHILDREN, ATTRS_TAGS
from src.base.base import Scraper
from bs4 import BeautifulSoup


class NewsScraperBase(Scraper):
    ''' Parent class for all news scraper '''

    def __init__(self):
        super().__init__()
        self.headers = self.get_headers()
        self.proxies = self.get_proxies()

    # +  -  -  - REQUESTS -  -  - +

    def request_url(self, url):
        ''' Request URL and return soup object '''

        try:
            html_page = requests.get(url)
            status = html_page.status_code
            print("status code: {}\n".format(status))

            # check status code
            if 300 <= status < 400:
                print("-- Being redirected, code: {} \n".format(status))
            elif status == 200:
                soup = BeautifulSoup(html_page.text, "html.parser")
                return soup

            return None

        except Exception as e:
            print("-Error while requesting URL: {} \n".format(e))
            return None

    # +  -  -  - FIND HTML TAGS -  -  - +

    def get_list_divs(self, soup, tag, attribute):
        ''' Return list of divs using tags and classnames from utils '''

        if tag in ATTRS_TAGS:
            containers = soup.find_all(tag)
        else:
            containers = soup.find_all(tag, attribute)

        if containers:
            return containers
        return []

    def get_single_div(self, soup, tag, attribute):
        ''' Return single div using tags and classnames from utils '''

        if tag in ATTRS_TAGS:
            item = soup.find(tag)
        else:
            item = soup.find(tag, attribute)

        if item:
            return item
        return None

    def get_attributes(self, div, attrs):
        ''' Return single value from attribute given '''

        attribute = div.get(attrs)

        if attribute:
            return attribute
        return None
