# author: long nguyen (nguyenhailong253@gmail.com)

import smtplib
import pandas as pd
from itertools import cycle
from contextlib import contextmanager
from datetime import datetime, timedelta
from psycopg2.pool import ThreadedConnectionPool
from src.utils.utils import download_free_proxies


class Scraper(object):
    ''' Parent class of all scrapers '''

    def __init__(self):
        self.NOW = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.connect_db()
        proxies = self.load_proxies()
        headers = self.load_user_headers()
        self.proxy_pool = cycle(proxies)
        self.header_pool = cycle(headers)

    # +  -  -  - PROXIES & HEADERS -  -  - +

    def load_proxies(self):
        ''' Load proxies from csv file and return a set of proxies'''
        proxies = set()
        try:
            df = pd.read_csv("./src/utils/proxy_files/proxies.csv")
            for i, r in df.iterrows():
                proxy = ':'.join([r['IP Address'], str(r['Port'])[:-2]])
                proxies.add(proxy)
        except Exception as e:
            print(e)

        return proxies

    def load_user_headers(self):
        ''' Load headers from csv file and return a set of headers'''
        headers = set()
        df = pd.read_csv("./src/utils/proxy_files/user_agents.csv")
        for i, r in df.iterrows():
            headers.add(r['User agent'])
        return headers

    def get_proxies(self):
        ''' Get the next proxy in proxy pool'''
        proxy = next(self.proxy_pool)
        return {"http": proxy, "https": proxy}

    def get_headers(self):
        ''' Get the next header in header pool'''
        headers = next(self.header_pool)
        return {"User-Agent": headers}

    def reset_proxy_pool(self):
        ''' Download new proxies, save to csv and load csv'''
        download_free_proxies()
        proxies = self.load_proxies()
        self.proxy_pool = cycle(proxies)

    # +  -  -  - DATABASE -  -  - +

    def connect_db(self):
        ''' Connect to db on cloud '''

        host_name = "bitko.czflnkl5jbgy.ap-southeast-2.rds.amazonaws.com"

        self._connpool = ThreadedConnectionPool(1, 2,
                                                database="bitko",
                                                user="bitko_admin",
                                                password="B1tk0adm1n$",
                                                host=host_name,
                                                port="5432")

    @contextmanager
    def cursor(self):
        ''' Get a cursor from the conn pool '''

        # Get available connection from pool
        conn = self._connpool.getconn()
        conn.autocommit = True
        try:
            # Return a generator cursor() created on the fly
            yield conn.cursor()
        finally:
            # Return the connection back to connection pool
            self._connpool.putconn(conn)

    def query_list(self, sql, values):
        with self.cursor() as cur:
            cur.execute(sql, values)
            results = [i for i in cur.fetchall()]
        return results

    def query_one(self, sql, values):
        with self.cursor() as cur:
            cur.execute(sql, values)
            result = cur.fetchone()
        return result

    def execute(self, sql, values):
        ''' Execute sql command'''
        with self.cursor() as cur:
            cur.execute(sql, values)
