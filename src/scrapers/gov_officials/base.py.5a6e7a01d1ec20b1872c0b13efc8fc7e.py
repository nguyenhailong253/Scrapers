# author: long nguyen (nguyenhailong253@gmail.com)

import re
import json
import time
import requests
import psycopg2
import logging
import logging.handlers as handlers
from bs4 import BeautifulSoup
from src.base.base import Scraper
from datetime import datetime, timedelta
from .utils import SPECS, OFFICE_TERM, PARENT_DIV


class GovOfficialsScraperBase(Scraper):
    ''' Parent class for scraper for Government Officials '''

    def __init__(self):
        super().__init__()
        self.headers = self.get_headers()
        self.proxies = self.get_proxies()

        # set up logger
        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.DEBUG)
        logHandler = handlers.RotatingFileHandler(
            './src/scrapers/gov_officials/logs/gov_off_scrape_log.log',
            maxBytes=1500000,
            backupCount=0)

        formatter = logging.Formatter("%(levelname)s:%(message)s")
        logHandler.setFormatter(formatter)
        logHandler.setLevel(logging.DEBUG)

        if not self.log.handlers:
            self.log.addHandler(logHandler)

    # +  -  -  - QUERIES -  -  - +

    def save_data(self, name, title, extra, office_term):
        ''' Save data of gov officials to DB '''

        sql = """
            INSERT INTO name_entity.test_gov_officials
            (name, title, extra, office_term)
            VALUES(%s, %s, %s, %s);
        """

        values = [name, title, extra, office_term]

        with self.cursor() as cur:
            cur.execute(sql, values)

    def check_existed_data(self, name):
        ''' Query db to check if data existed '''

        sql = """
            SELECT EXISTS (
                SELECT * FROM name_entity.test_gov_officials
                WHERE name = %s
            );
        """

        values = [name]

        result = self.query_one(sql, values)

        if result[0]:
            return True
        return False

    # +  -  -  - REQUESTS -  -  - +

    def request_url(self, url):
        ''' Request url and returned parsed HTML (called soup) '''

        try:
            # get request
            print("\n----URL: {} --- \n".format(url))
            html_page = requests.get(url)
            status = html_page.status_code
            print("status code = {} \n".format(status))

            # check status code
            if 300 <= status < 400:
                self.log.debug(
                    "-- Being redirected, code: {} \n".format(status))
            elif status == 200:
                soup = BeautifulSoup(html_page.text, "html.parser")
                return soup

            return None

        except requests.exceptions.ProxyError as p:
            print("-ProxyError: {} \n".format(p))
            self.log.exception("-ProxyError: {} \n".format(p))
            return None

    def get_div_list(self, soup, site_key):
        ''' Return list of all children divs '''

        parent = PARENT_DIV[site_key]['parent']
        children = PARENT_DIV[site_key]['children']

        container_div = soup.find(parent['tag'], parent['attribute'])

        items = container_div.find_all(
            children['tag'], children['attribute'])
        if items:
            return items
        return []

    # +  -  -  - PROCESSING DATA -  -  - +

    def gather_data(self, raw_div, site_key):
        ''' Return (multiple) processed data item '''

        data = {}
        extra = {}  # extra data, i.e DOB, home town, etc
        current_div = raw_div

        try:
            for key, value in SPECS[site_key].items():

                # find tag and class name using find next and current div
                # as many have same tag but no attribute differences
                content = current_div.find_next(value['tag'],
                                                value['attribute'])
                # update current div
                current_div = content

                if content:

                    # if this is an unused div with described attributes, skip
                    try:
                        if content.find(value['unused']['tag'], value['unused']['attribute']):
                            continue
                    except:
                        pass

                    content = self.process_data(content, key, site_key)

                    if key == 'title' or key == 'name':
                        data[key] = content
                    else:
                        extra[key] = content

                    data['office_term'] = OFFICE_TERM

            if extra:
                data['extra'] = json.dumps(extra)
            else:
                data['extra'] = None
            return data

        except Exception as e:
            print("-Error when processing data: {} \n".format(e))
            self.log.exception("-Error when processing data: {} \n".format(e))
            return {}

    def process_data(self, content, key, site):
        ''' Strip certain characters to get plain text of data '''

        content = content.get_text()

        if site == 'public_security':
            content = content.split(':', 1)[-1]
            if key == 'name':
                content = " ".join(content.split()[2:])

        elif site == 'justice':
            if key == 'name':
                content = " ".join(content.split()[-3:])
            elif key == 'title':
                content = " ".join(content.split()[:2]) + " Bộ Tư Pháp"

        content = content.strip(" \n").replace(
            "'", "''").replace("\n", ", ")

        return content
