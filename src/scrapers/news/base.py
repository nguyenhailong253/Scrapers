# author: long nguyen (nguyenhailong253@gmail.com)

import re
import json
import time
import requests
import psycopg2
from .utils import ROOT, PARENTS, CHILDREN, ATTRS_TAGS
from src.base.base import Scraper
from datetime import datetime
from bs4 import BeautifulSoup


class NewsScraperBase(Scraper):
    ''' Parent class for all news scraper '''

    def __init__(self):
        super().__init__()
        self.headers = self.get_headers()
        self.proxies = self.get_proxies()

    # +  -  -  - REQUESTS -  -  - +

    def request_url(self, url):
        ''' Request URL and return soup object, try 3 times if fails '''

        done = False
        attempt = 0
        soup = None
        while not done:
            try:
                html_page = requests.get(url)
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
                time.sleep(0.5)
        return soup

    # +  -  -  - FIND HTML TAGS -  -  - +

    def get_list_divs(self, soup, tag, attribute):
        ''' Return list of divs using tags and classnames from utils '''

        try:
            if tag in ATTRS_TAGS:
                containers = soup.find_all(tag)
            else:
                containers = soup.find_all(tag, attribute)

            if containers:
                return containers
            return []
        except:
            return []

    def get_single_div(self, soup, tag, attribute):
        ''' Return single div using tags and classnames from utils '''

        try:
            if tag in ATTRS_TAGS:
                item = soup.find(tag)
            else:
                item = soup.find(tag, attribute)

            if item:
                return item
            return None
        except:
            return None

    def get_attributes(self, div, attrs):
        ''' Return single value from attribute given '''

        try:
            attribute = div.get(attrs)

            if attribute:
                return attribute
            return None
        except:
            return None
