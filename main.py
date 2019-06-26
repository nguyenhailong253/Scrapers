# author: long nguyen (nguyenhailong253@gmail.com)

import time
import multiprocessing
from datetime import datetime
from src.scrapers.news.zing.scraper import ZingNewsScraper
from src.scrapers.news.zing.utils import CATEGORIES


def run(category):
    s = ZingNewsScraper()
    s.run(category)


def main():
    p = multiprocessing.Pool(processes=4)
    p.map(run, CATEGORIES)
    p.close()
    p.join()

    print("\nFinished at: {}\n".format(
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")))


if __name__ == "__main__":
    main()
