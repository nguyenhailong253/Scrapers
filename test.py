# author: long nguyen (nguyenhailong253@gmail.com)

from src.scrapers.jobs.indeed.scraper import IndeedScraper


def main():
    s = IndeedScraper()
    s.run()


if __name__ == "__main__":
    main()
