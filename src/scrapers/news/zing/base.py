# author: long nguyen (nguyenhailong253@gmail.com)

import logging
import logging.handlers as handlers
from src.scrapers.news.base import NewsScraperBase
from .utils import (ROOT, ATTRS_TAGS, PAGE, URL_TAIL, PARENTS, CHILDREN, TAG,
                    ATTRS, RAW_KEY, EXTRA_KEY, SUBCATE_SPECS, CATEGORIES,
                    ARTICLE_SPECS, THUMBNAIL_SPECS)

POSTED_AT = 'posted_at'
MISSING = "<missing>"
NULL = None


class ZingScraperBase(NewsScraperBase):
    ''' Parent class for news.zing.vn scraper '''

    def __init__(self):
        super().__init__()
        self.data = {}

    # +  -  -  - SET UP -  -  - +

    def set_up_logs(self):
        ''' Create log file and set formatter '''

        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.DEBUG)
        logHandler = handlers.RotatingFileHandler(
            './src/scrapers/news/zing/logs/zing_news.log',
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
        ''' Initialize all fields of data obj to null/missing '''

        for key in THUMBNAIL_SPECS[CHILDREN].keys():
            if key not in EXTRA_KEY:
                self.data[key] = MISSING

        for key in ARTICLE_SPECS[CHILDREN].keys():
            if key not in EXTRA_KEY:
                self.data[key] = MISSING

        for key in EXTRA_KEY:
            self.data[key] = NULL

        self.data[POSTED_AT] = MISSING

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

        text = text.strip(" \n").replace("'", "''")

        if text == '0':
            return None
        return text

    def process_article_body(self, raw_data):
        ''' Get only text, not caption of photos from article body '''
        raw_data = raw_data.find_all('p')
        result = ''
        for data in raw_data:
            result = result + "\n" + data.get_text()
        return self.process_text(result)

    def process_data(self, key, raw_data):
        ''' Based on key, call other process functions '''

        if key == 'article_type':
            return self.process_article_type(raw_data)
        elif key == 'content_text':
            return self.process_article_body(raw_data)
        elif key == 'url':
            return self.format_article_url(self.process_text(raw_data))
        elif key in RAW_KEY:
            return str(raw_data)
        else:
            return self.process_text(raw_data)

    def process_posted_at(self):
        ''' Call process time to cacl posted_at '''

        self.data[POSTED_AT] = self.process_time(
            self.data['publish_time'], self.data['publish_date'])

    # +  -  -  - QUERIES -  -  - +

    def save_news(self, values):
        ''' Insert data to DB '''

        sql = """
            INSERT INTO news.zing
            (src_id, article_type, url, img_src, title, publish_time, 
            publish_date, category, author, content_raw, content_text, tags_raw, 
            tags_text, summary, like_count, dislike_count, rating_count, 
            viral_count, comment_count, topic_id, posted_at)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """

        with self.cursor() as cur:
            cur.execute(sql, values)
