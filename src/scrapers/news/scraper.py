# author: long nguyen (nguyenhailong253@gmail.com)

import time
import json
import logging
import logging.handlers as handlers

from .base import NewsScraperBase
from .utils import (ROOT, THUMBNAIL_SPECS, ARTICLE_SPECS,
                    PARENTS, CHILDREN, TAG, ATTRS, ATTRS_TAGS, PAGE, URL_TAIL,
                    RAW_KEY, EXTRA_KEY, SUBCATE_SPECS, CATEGORIES)

POSTED_AT = 'posted_at'
EXTRA = 'extra'
ZERO = "<missing>"


class ZingNewsScraper(NewsScraperBase):
    ''' Scraper for news.zing.vn '''

    def __init__(self):
        super().__init__()
        self.data = {}
        self.done = False
        self.total_news = 0
        self.set_up_logs()

    def set_up_logs(self):
        ''' Create log file and set formatter '''

        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.DEBUG)
        logHandler = handlers.RotatingFileHandler(
            './src/scrapers/news/logs/zing_news.log',
            maxBytes=1500000,
            backupCount=0)

        formatter = logging.Formatter("%(levelname)s:%(message)s")
        logHandler.setFormatter(formatter)
        logHandler.setLevel(logging.DEBUG)

        if not self.log.handlers:
            self.log.addHandler(logHandler)

    def get_categories_dict(self):
        ''' Get dict with category name as key, url as value '''

        categories_dict = {}
        soup = self.request_url(ROOT)

        parent_sets = SUBCATE_SPECS[PARENTS]

        divs = self.get_list_divs(soup, parent_sets[TAG], parent_sets[ATTRS])

        children_sets = SUBCATE_SPECS[CHILDREN]

        for div in divs:
            results = self.get_list_divs(
                div, children_sets[TAG], children_sets[ATTRS])

            for res in results:
                name = res.get_text()
                url = self.get_attributes(res, children_sets[ATTRS])[
                    :-4].replace(".", "/")
                categories_dict[name] = url
        return categories_dict

    # +  -  -  - FORMAT URL -  -  - +

    def format_article_url(self, tail):
        ''' Format URL with 2 components: root and tail '''
        return "{}{}".format(ROOT, tail)

    def format_page_url(self, name, page_num):
        ''' Format URL with page number '''
        return "{}{}{}{}{}".format(ROOT, name, PAGE, page_num, URL_TAIL)

    # +  -  -  - PROCESS DATA -  -  - +

    def initialize_data(self):
        ''' Initialize all fields of data obj to null '''

        extra_data = {}
        for key in EXTRA_KEY:
            extra_data[key] = ZERO

        for key, value in THUMBNAIL_SPECS[CHILDREN].items():
            if key not in EXTRA_KEY:
                self.data[key] = ZERO

        for key, value in ARTICLE_SPECS[CHILDREN].items():
            if key not in EXTRA_KEY:
                self.data[key] = ZERO

        self.data[EXTRA] = extra_data
        self.data[POSTED_AT] = ZERO

    def process_article_type(self, article_type):
        ''' Get second item in list of article type and strip 'type-' '''

        return article_type[1][5:]

    def process_time(self, time, date):
        ''' Convert to standard time format %Y-%m-%d %H:%M:%S'''

        date = date.split('/')
        date = reversed(date)
        date = "-".join(date)
        time = time + ":00"
        return "{} {}".format(date, time)

    def process_text(self, text):
        ''' Strip, replace newline or spaces neccessary '''

        if not isinstance(text, str):
            text = text.get_text()

        return text.strip(" \n").replace(
            "'", "''")

    def process_data(self, key, raw_data):
        ''' Based on key, call other process functions '''

        if key == 'article_type':
            return self.process_article_type(raw_data)
        elif key == 'url':
            return self.format_article_url(self.process_text(raw_data))
        elif key in RAW_KEY:
            return str(raw_data)
        else:
            return self.process_text(raw_data)

    def process_extras(self):
        ''' Convert extras to json and call process time to cacl posted_at '''

        self.data[POSTED_AT] = self.process_time(
            self.data['publish_time'], self.data['publish_date'])

        self.data[EXTRA] = json.dumps(self.data[EXTRA])

    # +  -  -  - QUERIES -  -  - +

    def save_news(self, values):
        ''' Insert data to DB '''

        sql = """
            INSERT INTO news.test_zingnews
            (src_id, article_type, topic_id, url, img_src, 
            title, publish_time, publish_date, category, author, 
            article_body, tags, summary, extra, posted_at)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s);
        """

        with self.cursor() as cur:
            cur.execute(sql, values)

    def check_news_existed(self, news_id):
        ''' Query if news already existed '''

        sql = """
            SELECT EXISTS (
                SELECT * FROM news.test_zingnews
                WHERE src_id = %s
            );
        """
        values = [news_id]
        result = self.query_one(sql, values)

        if result[0]:
            return True
        return False

    # +  -  -  - SCRAPING -  -  - +

    def scrape_attrs_tags(self, div, key, value):
        ''' Process content of html tag a, img, or None '''

        result = self.get_attributes(
            div, value[ATTRS])

        if result:
            result = self.process_data(key, result)
            self.data[key] = result
        else:
            self.data[key] = ZERO

    def scrape_extras(self, key, result=ZERO):
        ''' Check if key in EXTRA_KEY and assign result to value based on key '''

        if key in EXTRA_KEY:
            self.data[EXTRA][key] = result
        else:
            self.data[key] = result

    def scrape(self, div, html_attrs):
        ''' Scrape article details, given its html div and set of attributes '''

        for key, value in html_attrs.items():
            try:
                if value[TAG]:
                    result = self.get_single_div(div, value[TAG], value[ATTRS])
                    # if div exists
                    if result:
                        # if one of attribute tags
                        if value[TAG] in ATTRS_TAGS:
                            self.scrape_attrs_tags(result, key, value)
                        # if normal tag
                        else:
                            result = self.process_data(key, result)

                            if result:
                                self.scrape_extras(key, result)
                            else:
                                self.scrape_extras(key)
                    else:
                        self.log.debug(
                            "--- NoneType: {}, {}\n".format(key, value[TAG]))
                        self.scrape_extras(key)
                else:
                    self.scrape_attrs_tags(div, key, value)
            except Exception as e:
                self.log.exception(
                    "-- {}: {}, {}, \n{}\n".format(e, key, value[TAG], div))
                print("-- Error when scraping: {}\n".format(e))

    def scrape_pages(self, category, page_num):
        ''' Iterate through all articles in 1 page and call scrape func '''

        already_scraped = 0
        # format general url
        url = self.format_page_url(category, page_num)
        # request url
        soup = self.request_url(url)

        # if request successfully
        if soup:
            # get all children divs
            divs = self.get_list_divs(
                soup, THUMBNAIL_SPECS[PARENTS][TAG], THUMBNAIL_SPECS[PARENTS][ATTRS])
            self.log.info("NUMBER OF DIVS THIS PAGE: {} AT {}\n".format(len(divs), url))

            # if empty [], finish this category
            if not divs:
                self.done = True
                return

            # loop each children div
            for div in divs:
                self.initialize_data()

                # scrape general info of that div
                self.scrape(div, THUMBNAIL_SPECS[CHILDREN])

                # check news existed after got src_id
                # if existed, for now, skip this news
                if self.check_news_existed(self.data['src_id']):
                    self.log.debug(
                        "--- {} - {}. Already scraped: {} at {}\n".format(already_scraped, category, self.data['url'], url))

                    already_scraped += 1
                    # if already_scraped >= 25:
                    #     self.done = True
                    #     break
                    continue
                    # self.done = True
                    # break

                # request url, get single div for full article
                soup = self.request_url(self.data['url'])
                if soup:
                    full_article = self.get_single_div(
                        soup, ARTICLE_SPECS[PARENTS][TAG], ARTICLE_SPECS[PARENTS][ATTRS])

                    # scrape details of article in that div
                    self.scrape(full_article, ARTICLE_SPECS[CHILDREN])
                    # process extras data
                    self.process_extras()

                    # send details to db
                    values = list(self.data.values())
                    self.save_news(values)
                    self.total_news += 1
                    # already_scraped = 0

                    self.log.info(" {}: {}\n".format(
                        self.data['src_id'], self.data['url']))

                # skip if request fails
                else:
                    self.log.exception(
                        "--- ERROR: Cannot request url {}\n".format(self.data['url']))
                    continue
        else:
            print("-- Cannot request url: {}\n".format(url))
            self.log.exception(
                "--- ERROR: Cannot request url {}\n".format(url))

    def run(self, category):

        self.log.info("--- START: {} AT {}\n".format(category, self.NOW))
        print("--- START: {} AT {}\n".format(category, self.NOW))
        page_num = 16

        while not self.done and page_num <= 50:
            self.scrape_pages(category, page_num)
            page_num += 1

        self.log.info(
            "--- FINISHED: {} {} news AT {}\n".format(self.total_news, category, self.NOW))


''' 
    #TODOS:
        - for first run, use check_existed to avoid duplicate
        - after that, check_existed will be used as condition to stop scraping
        (since they organize news chronologically, as soon as we encounter an
        already scraped news, we stop)
        - add logging

'''
