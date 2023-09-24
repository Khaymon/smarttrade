import argparse

from smarttrade.data.scrappers.lib import InvestingSeleniumScrapper


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        "investing.com news scrapper",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("--driver-path", required=True, type=str, help="Path to the Selenium driver")
    parser.add_argument("--driver-timeout", required=False, default=6, type=int, help="Driver timout in seconds")
    parser.add_argument("--page-limit", required=False, default=100, type=int, help="Scrapped pages count limit")
    parser.add_argument("--news-limit", required=False, default=10_000, type=int, help="News limit")
    parser.add_argument("--base-link", required=True, type=str, help="Link to the base page with news")
    parser.add_argument("--start-page", required=False, default=1, type=int, help="Starting page number")

    return parser.parse_args()

def main():
    args = _parse_args()
    scrapper = InvestingSeleniumScrapper(args.driver_path, args.driver_timeout, args.page_limit)
    data = scrapper.get_data(args.base_link, args.news_limit, args.start_page)

    print(data)

if __name__ == "__main__":
    main()