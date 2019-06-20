# author: long nguyen (nguyenhailong253@gmail.com)

import time
import multiprocessing
from datetime import datetime
from src.scrapers.gov_officials.scraper import GovOfficialsScraper
from src.scrapers.news.scraper import ZingNewsScraper
from src.scrapers.news.utils import CATEGORIES


def run(category):
    s = ZingNewsScraper()
    s.run(category)


def main():
    # s = GovOfficialsScraper()
    # s.run()
    start = time.time()

    p = multiprocessing.Pool(processes=4)
    p.map(run, CATEGORIES)
    p.close()
    p.join()

    end = time.time() - start
    print("\nFinished at: {}\n".format(
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    print("Finished scraping after {}s".format(end-start))


if __name__ == "__main__":
    main()
