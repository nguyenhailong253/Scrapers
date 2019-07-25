# author: long nguyen (nguyenhailong253@gmail.com)

import time
import json

from .base import ZingScraperBase
from .utils import (THUMBNAIL_SPECS, ARTICLE_SPECS,
                    PARENTS, CHILDREN, TAG, ATTRS, ATTRS_TAGS)


class ZingNewsScraper(ZingScraperBase):
    ''' Scraper for news.zing.vn '''

    def __init__(self):
        super().__init__()
        self.done = False
        self.total_news = 0
        self.set_up_logs()

    # +  -  -  - SCRAPING -  -  - +

    def scrape_attrs_tags(self, div, key, value):
        ''' Process content of html tag a, img, or None '''

        result = self.get_attributes(
            div, value[ATTRS])

        if result:
            result = self.process_data(key, result)
            self.data[key] = result

    def scrape_text(self, div, html_attrs):
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
                                self.data[key] = result
                else:
                    self.scrape_attrs_tags(div, key, value)
            except Exception as e:
                self.log.exception(
                    "-- {}: {}, {}, \n{}\n".format(e, key, value[TAG], div))
                print("-- Error when scraping: {}\n".format(e))

    def scrape_div(self, div):
        ''' Scrape content of a div, return True if scraped successfully '''

        self.initialize_data()
        # scrape general info of that div
        self.scrape_text(div, THUMBNAIL_SPECS[CHILDREN])

        # request url, get single div for full article
        soup = self.request_url(self.data['url'])
        if soup:
            full_article = self.get_single_div(
                soup, ARTICLE_SPECS[PARENTS][TAG], ARTICLE_SPECS[PARENTS][ATTRS])

            # scrape details of article in that div
            self.scrape_text(full_article, ARTICLE_SPECS[CHILDREN])
            # process extras data
            self.process_posted_at()

            # send details to db
            values = list(self.data.values())
            
            try:
                self.save_news(values)
                self.total_news += 1
                self.log.info(" {}: {}\n".format(
                    self.data['src_id'], self.data['url']))
                return True
            except Exception as e:
                # if existed, skip
                self.log.debug(
                    "--- Already scraped: {}\n{}\n".format(self.data['url'], e))
                return False
        else:
            self.log.exception(
                "--- Cannot request url {}\n".format(self.data['url']))
            return False

    def scrape_page(self, category, page_num):
        ''' Get list of article divs and call scrape each div '''

        # format general url
        url = self.format_page_url(category, page_num)
        # request url
        soup = self.request_url(url)
        already_scraped = 0

        # if request successfully
        if soup:
            # get all children divs
            divs = self.get_list_divs(
                soup, THUMBNAIL_SPECS[PARENTS][TAG], THUMBNAIL_SPECS[PARENTS][ATTRS])
            self.log.info(
                "NUMBER OF DIVS THIS PAGE: {} AT {}\n".format(len(divs), url))

            # if empty [], finish this category
            if not divs:
                self.done = True
                return

            # loop each children div
            for div in divs:
                has_been_scraped = self.scrape_div(div)

                if not has_been_scraped:
                    already_scraped += 1
                    if already_scraped >= 40:
                        self.done = True
                        break

        else:
            print("-- Cannot request url: {}\n".format(url))
            self.log.exception(
                "--- Cannot request url {}\n".format(url))

    def run(self, category):

        self.log.info("--- START: {} AT {}\n".format(category, self.NOW))
        print("--- START: {} AT {}\n".format(category, self.NOW))
        page_num = 1

        while not self.done and page_num <= 50:
            start = time.time()
            self.scrape_page(category, page_num)
            end = time.time()
            self.log.info("TIME: {} page{} = {}s\n".format(
                category, page_num, float(end-start)))
            page_num += 1

        self.log.info(
            "--- FINISHED: {} {} news AT {}\n".format(self.total_news, category, self.NOW))

# TODO:
# change news to lds_news
