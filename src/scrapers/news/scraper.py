# author: long nguyen (nguyenhailong253@gmail.com)

import json
from .base import NewsScraperBase
from .utils import ROOT, THUMBNAIL_SPECS, ARTICLE_SPECS, PARENTS, CHILDREN, TAG, ATTRS, ATTRS_TAGS, PAGE, URL_TAIL, RAW_KEY, EXTRA_KEY, SUBCATE_SPECS, CATEGORIES

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
            (src_id, article_type, topic_id, url, img_src, title,
            publish_time, publish_date, category, author, article_body,
            tags, summary, extra, posted_at)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
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

    def scrape_general(self, div, children_sets):
        ''' Scrape general information of article from page url '''

        for key, value in children_sets.items():
            # print("==== GETTING KEY: {} ==== \n".format(key))

            if value[TAG]:
                result = self.get_single_div(div, value[TAG], value[ATTRS])

                # if div exists
                if result:
                    # if one of attribute tags
                    if value[TAG] in ATTRS_TAGS:
                        result = self.get_attributes(
                            result, value[ATTRS])
                        result = self.process_data(key, result)
                        self.data[key] = result

                    # if normal tag
                    else:
                        result = self.process_data(key, result)

                        if result:
                            if key in EXTRA_KEY:
                                self.data[EXTRA][key] = result
                            else:
                                self.data[key] = result
                        else:
                            if key in EXTRA_KEY:
                                self.data[EXTRA][key] = ZERO
                            else:
                                self.data[key] = ZERO
                else:
                    print(
                        "--- NoneType: {}, {} --- \n".format(key, value[TAG]))
                    if key in EXTRA_KEY:
                        self.data[EXTRA][key] = ZERO
                    else:
                        self.data[key] = ZERO

            else:
                result = self.get_attributes(
                    div, value[ATTRS])
                if result:
                    result = self.process_data(key, result)
                    self.data[key] = result
                else:
                    self.data[key] = ZERO

            # print(self.data[key])

    def scrape_details(self, div, children_sets):
        ''' Scrape article details from article url '''

        for key, value in children_sets.items():
            # print("==== GETTING KEY: {} ==== \n".format(key))
            if value[TAG]:
                result = self.get_single_div(div, value[TAG], value[ATTRS])

                if result:
                    if value[TAG] in ATTRS_TAGS:
                        result = self.get_attributes(
                            result, value[ATTRS])
                        if result:
                            result = self.process_data(key, result)
                            self.data[key] = result
                        else:
                            self.data[key] = ZERO
                    else:
                        result = self.process_data(key, result)

                        if result:
                            if key in EXTRA_KEY:
                                self.data[EXTRA][key] = result
                            else:
                                self.data[key] = result
                        else:
                            if key in EXTRA_KEY:
                                self.data[EXTRA][key] = ZERO
                            else:
                                self.data[key] = ZERO
                else:
                    print(
                        "--- NoneType: {}, {} --- \n".format(key, value[TAG]))
                    if key in EXTRA_KEY:
                        self.data[EXTRA][key] = ZERO
                    else:
                        self.data[key] = ZERO

            else:
                result = self.get_attributes(
                    div, value[ATTRS])
                if result:
                    result = self.process_data(key, result)
                    self.data[key] = result
                else:
                    self.data[key] = ZERO

            # print(self.data[key])

    def scrape(self, category, page_num):
        ''' SCRAPE GENERAL INFO '''

        # format general url

        url = self.format_page_url(category, page_num)
        print(url)

        # url = "https://news.zing.vn/chinh-tri/trang5.html"

        # request url

        soup = self.request_url(url)

        # if status code weird, finish scraping or try again

        # if status good,

        # get all children divs

        divs = self.get_list_divs(
            soup, THUMBNAIL_SPECS[PARENTS][TAG], THUMBNAIL_SPECS[PARENTS][ATTRS])

        # if NULL or [], finish scraping, setting self.done, break

        if not divs:
            print("END OF NEWS")
            self.done = True
            return

        # loop each children div
        self.total_news += len(divs)

        print("NUMBER OF NEWS: {}\n\n".format(len(divs)))

        for div in divs:
            # initialize data

            self.initialize_data()

            # scrape general of that div

            self.scrape_general(div, THUMBNAIL_SPECS[CHILDREN])

            # check news existed after got src_id
            # if existed, for now, skip this news

            if self.check_news_existed(self.data['src_id']):
                continue

            # get new url for full article

            url = self.format_article_url(self.data['url'])
            print(url)

            # request url, get single div for full article

            soup = self.request_url(url)

            full_article = self.get_single_div(
                soup, ARTICLE_SPECS[PARENTS][TAG], ARTICLE_SPECS[PARENTS][ATTRS])

            # scrape details of that div

            self.scrape_details(full_article, ARTICLE_SPECS[CHILDREN])

            # process extras data

            self.process_extras()

            # send details to db

            values = list(self.data.values())
            self.save_news(values)
            print("SUCCESSFULLY SCRAPED\n\n")

        # url = ROOT + "/kinh-doanh-tai-chinh/trang1.html"
        # self.scrape_general(url)

        # ''' SCRAPE DETAILS ARTICLE '''

        # # url = self.format_article_url()
        # url = ROOT + self.data['url']
        # self.scrape_details(url)

        # self.process_extras()
        # print(self.data)
        # print("\n")

        # values = list(self.data.values())
        # if not self.check_news_existed(self.data['src_id']):
        #     self.save_news(values)
        #     print("not existed")

    def run(self, category='/chinh-tri/'):

        page_num = 0

        while not self.done:
            page_num += 1
            self.scrape(category, page_num)

        print("=== TOTAL NEWS: {} ===\n\n".format(self.total_news))


''' 
    #TODOS:
        - break scrape_general and details to smaller functions
        - add conditions: if not found parents div => end of page, stop scraping
        and start with new category
        - for first run, use check_existed to avoid duplicate
        - after that, check_existed will be used as condition to stop scraping
        (since they organize news chronologically, as soon as we encounter an
        already scraped news, we stop)
        - multiprocessing
        - Handling error if missing URL for full article

'''
