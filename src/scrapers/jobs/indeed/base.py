# author: long nguyen (nguyenhailong253@gmail.com)

import requests
from datetime import timedelta
from bs4 import BeautifulSoup
from src.scrapers.jobs.base import JobScraperBase
from .utils import SUBCATE_TAGS, PARENT, CHILDREN, TAG, ATTRS, ROOT, JD_QUERY, TIME_UNIT, PERIOD_UNIT, STATES

SOURCE = 'indeed'
NULL = '<missing>'


class IndeedScraperBase(JobScraperBase):
    ''' Parent class for au.indeed.com scraper '''

    def __init__(self):
        super().__init__()
        self.set_up_logger(SOURCE)
        self.is_latest_job = True

    def get_subcategories(self, url):
        ''' Return dict of subcategories with key = name, value = url '''

        result = {}

        soup = self.request_url(url)

        parents = SUBCATE_TAGS[PARENT]
        child_tags = SUBCATE_TAGS[CHILDREN]

        divs = self.get_list_divs(soup, parents[TAG], parents[ATTRS])

        for div in divs:
            target = self.get_single_div(
                div, child_tags[TAG], child_tags[ATTRS])
            # Get name
            name = target.attrs["title"]
            # Get link
            link = self.get_attributes(target, child_tags[ATTRS])
            # Assign key, value
            result[name] = link
        return result

    # +  -  -  - FORMAT URL -  -  - +

    def format_jd_url(self, jobid):
        ''' Format: https://au.indeed.com/viewjob?jk=addc4767450b0cc7 '''
        return '{}{}{}'.format(ROOT, JD_QUERY, jobid)

    def format_page_url(self, body_url, query, page):
        ''' Format: https://au.indeed.com/jobs?q=SUBCATE&sort=date&start=10 '''
        url = '{}{}{}{}'.format(ROOT, body_url[:-18], query, page)
        return url

    def format_category_url(self):
        pass

    # +  -  -  - PROCESS DATA -  -  - +

    def process_text(self, text):
        ''' Get text, strip, replace '''

        if not isinstance(text, str):
            text = text.get_text()

        text = text.strip(" \n").replace("'", "''")
        if text:
            return text
        return None

    def process_loc_state_area(self, loc):
        ''' Get state & area in given location, return state, area '''
        loc_list = loc.split()
        state = NULL
        area = NULL

        if len(loc_list) >= 2:
            # could be: New South Wales or Cabramatta NSW
            state = loc_list[-1]  # assume Cabramatta NSW
            area = " ".join(loc_list[:-1]).replace("'", "''")

            for s in STATES:
                if loc == s:
                    state = s
        elif len(loc_list) == 1:
            for s in STATES:
                if loc_list[0] == s:
                    state = s

        return state, area

    def process_summary(self, summary):
        summary = self.process_text(summary)
        return summary.strip(",...")

    def process_is_latest_job(self, delta_time, limit):
        ''' Compare time difference with limit difference. If time > limit, not latest job '''

        if delta_time > limit:
            self.is_latest_job = False
        else:
            self.is_latest_job = True

    def process_time_delta(self, time, limit):
        ''' Determine time difference from posted time and scraped time '''

        # if date = "Just posted" or "Today"
        if (time[0] == "Just") or (time[0] == "Today"):
            delta = timedelta(seconds=0)

        if (time[1] == "day") or (time[1] == "days"):
            if time[0] == "30+":
                delta = timedelta(days=30)
                self.process_is_latest_job(delta, int(float(limit)))
            else:
                delta = timedelta(days=int(time[0]))
                self.process_is_latest_job(
                    int(float(time[0])), int(float(limit)))

        elif (time[1] == "hours") or (time[1] == "hour"):
            delta = timedelta(hours=int(time[0]))

        elif (time[1] == "minutes") or (time[1] == "minute"):
            delta = timedelta(minutes=int(time[0]))

        elif (time[1] == "seconds") or (time[1] == "second"):
            delta = timedelta(seconds=int(time[0]))
        return delta

    def process_time(self, time, limit=1):
        ''' Calculate the original post time of a job by Seek

        # Arguments:
            time: the date(string) got from job ad
            limit: limit how many days ago when job ads were posted

        # Returns:
            original_time: Date and time of job post
        '''

        time = time.split()

        delta = self.process_time_delta(time, limit)
        original_time = (self.NOW - delta).strftime("%Y-%m-%d %H:%M:%S")

        return original_time

    def process_is_sponsored(self, issponsored):
        issponsored = self.process_text(issponsored)
        if isinstance(issponsored, str):
            return True
        return False

    def process_sponsored_by(self, sponsorid):
        pass

    def process_salary(self, salary):
        ''' Convert salary to format: $X - $Y yearly or $X yearly'''
        salary = salary.split()
        result = None

        for i in range(len(TIME_UNIT)):
            if len(salary) == 3:
                # eg: $24 an hour
                if salary[2] == TIME_UNIT[i]:
                    result = "{} {}".format(salary[0],
                                            PERIOD_UNIT[i])
            elif len(salary) == 5:
                # eg: $40,000 - $50,000 a year
                if salary[4] == TIME_UNIT[i]:
                    result = "{}-{} {}".format(salary[0],
                                               salary[2],
                                               PERIOD_UNIT[i])
        return result

    def process_data(self, key, raw_data):
        ''' Based on key, call other process functions '''

        if key == 'posted_at':
            raw_data = self.process_text(raw_data)
            return self.process_time(raw_data)
        elif key == 'salary':
            raw_data = self.process_text(raw_data)
            return self.process_salary(raw_data)
        elif key == 'sponsored':
            return self.process_is_sponsored(raw_data)
        elif key == 'short_desc':
            return self.process_summary(raw_data)
        else:
            return self.process_text(raw_data)

    def process_extras(self):
        pass
