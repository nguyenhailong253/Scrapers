# author: long nguyen (nguyenhailong253@gmail.com)

from src.scrapers.gov_officials.scraper import GovOfficialsScraper


def main():
    s = GovOfficialsScraper()
    s.run()


if __name__ == "__main__":
    main()
